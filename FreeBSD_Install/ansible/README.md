# Автоматизация установки Zabbix-server

## Подготовка 

На свежеустановленных FreeBDS требуется разрешить подключение через ssh к root-пользователю или пользователь с правами sudo.

Заходим на клиентов и редактируем ```/etc/sshd_config```:
```
PermitRootLogin yes
```

Устанавливаем python на клиента:
```
pkg install -y python37-3.7.10
```

Генерируем ssh ключи(```ssh-keygen```) на сервере и переносим на клиентов:
```
ssh root@<ip> 'mkdir -p /root/.ssh'
scp /root/.ssh/id_rsa.pub root@<ip>:/root/.ssh/authorized_keys
```

