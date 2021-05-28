#!/bin/sh

DIRPATH='/var/backups/zabbix'
DATE=`date +"%Y-%m-%d_%H-%M"`
MAX_BACKUPS=5


mysqldump --set-gtid-purged=off --no-tablespaces zabbix > ${DIRPATH}/backup_${DATE}.sql

cd $DIRPATH
num_backups=`ls backup* | wc | awk '{print $2}'`
oldest_backup=`find backup* -type f -print0 | xargs -0 ls -lt | tail -n 1 | awk '{print $9}'`

if [ $num_backups -gt $MAX_BACKUPS ]
then
       rm $oldest_backup
fi
