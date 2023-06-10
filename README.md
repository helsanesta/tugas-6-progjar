# TUGAS 6 PROGJAR 2023
Nama : Helsa Nesta Dhaifullah <br>
NRP : 5025201005 <br>
Kelas : Progjar A  <br>


## Fungsionalitas
A. Autentikasi
  - Autentikasi user <br>
  ```auth <username> <password>``` <br>
  ```auth messi surabaya```
  - Daftar User Password :
    - messi surabaya
    - henderson surabaya
    - lineker surabaya
   
B. Komunikasi dalam satu server
  - send private message <br>
   ```send <user_dest> <message>``` <br>
    ```send henderson apa kabar son```
  - send group message <br>
  ```sendgroup <user_dest 1>,<user_dest 2>,...,<user_dest n> <message>``` <br>
  ```sendgroup henderson,lineker halo gaiss apa kabar```
  - send file + simpan file <br>
  ```sendfile <user_dest> <file_path>``` <br>
  ```sendfile henderson pokijan.jpg```
  - send group file (banyak user) + simpan file <br>
  ```sendgroupfile <user_dest 1>,<user_dest 2>,...,<user_dest n> <file path>``` <br>
  ```sendgroup henderson,lineker pokijan.jpg```
  - inbox <br>
  ```inbox```

C. Komunikasi dengan server lain
  - addrealm <br>
  ```addrealm <nama_realm> <ip_dest> <port_dest>``` <br>
  ```addrealm realm1 172.16.16.102 8890```
  - send private message realm
  ```sendprivaterealm <nama_realm> <user_dest> <message>``` <br>
  ```sendprivaterealm realm1 henderson bagaimana son di mesin 2```
  - send group message realm <br>
   ```sendgrouprealm <nama_realm> <user_dest 1>,<user_dest 2>,...,<user_dest n> <message>``` <br>
   ```sendgrouprealm realm1 henderson,lineker bagaimana kalian di mesin 2```
  - send file realm + simpan file <br>
  ```sendfilerealm <nama_realm> <user_dest> <file_path>``` <br>
  ```sendfilerealm realm1 henderson pokijan.jpg```
  - send group file realm (banyak user) + simpan file <br>
  ```sendgroupfilerealm <nama_realm> <user_dest 1>,<user_dest 2>,...,<user_dest n> <file_path>``` <br>
  ```sendgroupfilerealm realm1 henderson,lineker pokijan.jpg```
  - inbox realm <br>
  ```inbox <nama_realm> <username>``` <br>
  ```inbox realm1 henderson```
