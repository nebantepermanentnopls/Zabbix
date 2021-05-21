 # Настройка автоматического backup`а для mysql
 
 Создаем файл ```~/.my.cnf``` с данными пользователя, он позволит нам не вводить пароль при запуске команд mysql:
 
 ```
[mysqldump]
user=root
password=03012001
 ```
 
 Устанавливаем права:
 ```
 chmod 600 ~/.my.cnf
 ```
 
 Создаем скрипт для создания бэкапов и ограничения их количества:
 
 ```
#!/bin/sh

DIRPATH='/var/backups/zabbix'
DATE=`date +"%Y-%m-%d_%H-%M"`
MAX_BACKUPS=5


mysqldump --set-gtid-purged=off --no-tablespaces zabbix > ${DIRPATH}/backup_${DATE}.sql

cd $DIRPATH
num_backups=`ls backup* | wc | awk '{print $2}'`
oldest_backup=`find backup* -type f -print0 | xargs -0 ls -lt | tail -n 1 | awk '{print $9}'`

if [ $num_backups > $MAX_BACKUPS ]
then
        rm $oldest_backup
fi
 ```
 
 Добавляем строку в crontab(выставив нужные тайминги):
 
 ```
 *       *       *       *       *       root    /root/backup_script.sh 
 ```
 
 ## Восстановление 
 
 Бэкап:
 ```
 mysql db1 < dump.sql
 ```
 
 Бинарные логи(полезные команды: --start-datetime, --stop-datetime, --start-position, --stop-position):
 ```
 mysqlbinlog bin-log | mysql -u root -p
 ```
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
