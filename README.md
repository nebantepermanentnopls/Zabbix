# FreeBSD zabbix-server install

## Подготовка

Ищем через pkg search версии пакетов: nginx, mysql, zabbix. Устанавливаем:
```
pkg install nginx-1.18.0_49,2 mysql57-server-5.7.33 zabbix52-server-5.2.5 zabbix52-frontend-5.2.5 zabbix52-agent-5.2.5
```

Добавляем в rc:
```
sysrc php_fpm_ebable=YES nginx_enable=YES mysql_enable=YES zabbix_server_enable=YES zabbix_agentd_enable=YES
```

## Настройка mysql

Скрипт первоначальной настройки:
```
/usr/local/bin/mysql_secure_installation
```

Настраиваем БД для Zabbix:
```
mysql -u root -p
password
mysql> create database zabbix character set utf8 collate utf8_bin;
mysql> create user zabbix@localhost identified by 'password';
mysql> grant all privileges on zabbix.* to zabbix@localhost;
mysql> quit;
```

Создаем таблицы в БД:
```
cd /usr/local/share/zabbix52/server/database/mysql
cat schema.sql images.sql data.sql | mysql -u zabbix -p
```

Создаем таблицы в БД(должно быть много табличек):
```
mysql -u zabbix -p
password
mysql> use zabbix
mysql> show tables;
```

## Настройка zabbix-server

Копируем пример конфига в настоящий конфиг:
```
cp /usr/local/etc/zabbix52/zabbix_server.conf.sample /usr/local/etc/zabbix52/zabbix_server.conf
```

Редактируем `/usr/local/etc/zabbix52/zabbix_server.conf`:
```
...
DBHost=localhost
...
DBName=zabbix
...
DBUser=zabbix
...
DBPassword=password
```

Презапускаем(или запускаем) zabbix:
```
service zabbix_server start
```

## Настройка nginx

Создаем отдельный конфиг, или редактируем nginx.conf(заменяем пути к Zabbix на нашу версию):
```
user www;
worker_processes  1;
error_log /var/log/nginx/error.log info;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    access_log /var/log/nginx/access.log;

    sendfile        on;
    keepalive_timeout  65;

    server {
        listen 3000;
        server_name server_ip;

        root /usr/local/www/zabbix52;
        index index.php index.html;

        location / {
                root   /usr/local/www/zabbix52;
                index  index.php index.html;
        }

        location ~ \.php$ {
                fastcgi_pass 127.0.0.1:9000;
                fastcgi_index index.php;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                try_files $uri =404;
                include fastcgi_params;
        }
    }
}
```

Перезапускаем сервер:
```
service nginx restart
```

Выдаем веб пользователю права на веб Zabbix:
```
chown -R www:www /usr/local/www/zabbix52
```

## Настройка php:

Копируем конфиг:
```
cp /usr/local/etc/php.ini-production /usr/local/etc/php.ini
```

Редактируем ```/usr/local/etc/php.ini```(если на 2 экране Zabbix, там где много "OK", что-то не окей, то меняй параметр в этом файле):
```
...
post_max_size = 16M
...
max_execution_time = 300
...
max_input_time = 300
...
date.timezone = Europe/Moscow
```

Перезапускаем php:
```
service php-fpm restart
```

## Настройка zabbix-agent

```
cp /usr/local/etc/zabbix52/zabbix_agentd.conf.sample /usr/local/etc/zabbix52/zabbix_agentd.conf
```

```
service zabbix_agentd start
```

### Дальше подключаемся к нашему серверу через браузер по указанным в nginx порам и ip.



