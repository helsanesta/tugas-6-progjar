import sys
import os
import json
import uuid
import logging
from queue import Queue

class Chat:
    def __init__(self):
        self.sessions = {}
        self.users = {}
        self.users['messi'] = {'nama': 'Lionel Messi', 'negara': 'Argentina', 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
        self.users['henderson'] = {'nama': 'Jordan Henderson', 'negara': 'Inggris', 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
        self.users['lineker'] = {'nama': 'Gary Lineker', 'negara': 'Inggris', 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
        self.groups = {}

    def proses(self, data):
        j = data.split(" ")
        try:
            command = j[0].strip()
            if command == 'auth':
                username = j[1].strip()
                password = j[2].strip()
                logging.warning("AUTH: auth {} {}".format(username, password))
                return self.autentikasi_user(username, password)
            elif command == 'send':
                sessionid = j[1].strip()
                recipient = j[2].strip()  # Nama penerima (bisa username atau nama grup)
                message = " ".join(j[3:])
                username_from = self.sessions[sessionid]['username']
                logging.warning("SEND: session {} send message from {} to {}" . format(sessionid, username_from, recipient))
                return self.send_message(sessionid, username_from, recipient, message)
            elif command == 'inbox':
                sessionid = j[1].strip()
                username = self.sessions[sessionid]['username']
                logging.warning("INBOX: {}".format(sessionid))
                return self.get_inbox(username)
            elif command == 'addgroup':  # Tambahkan command 'addgroup'
                sessionid = j[1].strip()
                groupname = j[2].strip()
                usernames = j[3:]  # Ambil semua username yang diberikan
                username_creator = self.sessions[sessionid]['username']
                logging.warning("ADDGROUP: session {} create group {} with members {}" . format(sessionid, groupname, usernames))
                return self.add_group(sessionid, username_creator, groupname, usernames)
            elif command == 'joingroup':
                group_name = j[1].strip()
                sessionid = j[2].strip()
                username = self.sessions[sessionid]['username']
                return self.join_group(group_name, username)
            elif command == 'sendgroupmessage':
                group_name = j[1].strip()
                sessionid = j[2].strip()
                username = self.sessions[sessionid]['username']
                message = " ".join(j[3:])
                return self.send_group_message(group_name, username, message)
            elif command == 'inboxgroupmessage':
                group_name = j[1].strip()
                username = j[2].strip()
                return self.get_group_inbox(group_name, username)
            else:
                return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
        except KeyError:
            return {'status': 'ERROR', 'message': 'Informasi tidak ditemukan'}
        except IndexError:
            return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}

    def autentikasi_user(self, username, password):
        if username not in self.users:
            return {'status': 'ERROR', 'message': 'User Tidak Ada'}
        if self.users[username]['password'] != password:
            return {'status': 'ERROR', 'message': 'Password Salah'}
        tokenid = str(uuid.uuid4())
        self.sessions[tokenid] = {'username': username, 'userdetail': self.users[username]}
        return {'status': 'OK', 'tokenid': tokenid}

    def get_user(self, username):
        if username not in self.users:
            return False
        return self.users[username]

    def send_message(self, sessionid, username_from, recipient, message):
        if sessionid not in self.sessions:
			return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}

		sender = self.get_user(username_from)
		if sender is False:
			return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

		if recipient in self.users:
			recipient_type = 'user'
			recipient_user = self.get_user(recipient)
			if recipient_user is False:
				return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}
		elif recipient in self.groups:
			recipient_type = 'group'
			recipient_group = self.groups[recipient]
		else:
			return {'status': 'ERROR', 'message': 'Penerima Tidak Ditemukan'}

		message = {'msg_from': sender['nama'], 'msg': message}

		if recipient_type == 'user':
			# Mengirim pesan ke pengguna
			outqueue_sender = sender['outgoing']
			inqueue_receiver = recipient_user['incoming']

			try:
				outqueue_sender[username_from].put(message)
			except KeyError:
				outqueue_sender[username_from] = Queue()
				outqueue_sender[username_from].put(message)
			try:
				inqueue_receiver[username_from].put(message)
			except KeyError:
				inqueue_receiver[username_from] = Queue()
				inqueue_receiver[username_from].put(message)

			return {'status': 'OK', 'message': 'Message Sent'}
		elif recipient_type == 'group':
			# Mengirim pesan ke grup
			members = recipient_group['members']

			for member_username in members:
				member = self.get_user(member_username)
				if member is False:
					continue
				
				outqueue_sender = sender['outgoing']
				inqueue_receiver = member['incoming']

				try:
					outqueue_sender[username_from].put(message)
				except KeyError:
					outqueue_sender[username_from] = Queue()
					outqueue_sender[username_from].put(message)
				try:
					inqueue_receiver[username_from].put(message)
				except KeyError:
					inqueue_receiver[username_from] = Queue()
					inqueue_receiver[username_from].put(message)

			return {'status': 'OK', 'message': 'Message Sent to Group'}


    def get_inbox(self, username):
        s_fr = self.get_user(username)
        incoming = s_fr['incoming']
        msgs = {}
        for users in incoming:
            msgs[users] = []
            while not incoming[users].empty():
                msgs[users].append(s_fr['incoming'][users].get_nowait())

        return {'status': 'OK', 'messages': msgs}

    def add_group(self, sessionid, username_creator, groupname, members):
        if sessionid not in self.sessions:
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}

        # Periksa apakah pengguna yang membuat grup adalah pengguna yang valid
		
        creator = self.get_user(username_creator)
        if creator is False:
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        # Periksa apakah semua anggota grup adalah pengguna yang valid
        # members = []
        # for username in usernames:
        #     user = self.get_user(username)
        #     if user is False:
        #         return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}
        #     members.append(user)

        # Buat grup baru dan tambahkan anggota ke dalam grup
        group_id = str(uuid.uuid4())
        self.groups[group_id] = {
            'groupname': groupname,
            'creator': creator,
            'members': members
        }

        return {'status': 'OK', 'message': 'Group Created', 'group_id': group_id}

    def join_group(self, group_name, username):
        if group_name not in self.groups:
            return {'status': 'ERROR', 'message': 'Grup tidak ditemukan'}
        s_fr = self.get_user(username)
        if s_fr == False:
            return {'status': 'ERROR', 'message': 'User tidak ditemukan'}
        self.groups[group_name].append(username)
        return {'status': 'OK', 'message': 'Bergabung ke grup berhasil'}

    def send_group_message(self, group_name, username, message):
        if group_name not in self.groups:
            return {'status': 'ERROR', 'message': 'Grup tidak ditemukan'}
        if username not in self.users:
            return {'status': 'ERROR', 'message': 'User tidak ditemukan'}
        members = self.groups[group_name]
        for member in members:
            if member != username:
                self.send_message(None, username, member, message)
        return {'status': 'OK', 'message': 'Pesan grup berhasil dikirim'}

    def get_group_inbox(self, group_name, username):
        if group_name not in self.groups:
            return {'status': 'ERROR', 'message': 'Grup tidak ditemukan'}
        if username not in self.users:
            return {'status': 'ERROR', 'message': 'User tidak ditemukan'}
        messages = []
        for member in self.groups[group_name]:
            if member != username:
                inbox = self.users[member]['incoming'].get(username, Queue())
                while not inbox.empty():
                    messages.append(inbox.get_nowait())
        return {'status': 'OK', 'messages': messages}


if __name__ == "__main__":
    j = Chat()
    sesi = j.proses("auth messi surabaya")
    tokenid = sesi['tokenid']
    print(j.proses("addgroup {} mygroup henderson lineker" . format(tokenid)))
    # Mengirim pesan ke grup 'mygroup'
    print(j.proses("send {} mygroup hello semua!" . format(tokenid)))
