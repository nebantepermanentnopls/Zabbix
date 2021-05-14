from pyzabbix import ZabbixAPI

zapi = ZabbixAPI(url='http://172.20.10.5:3000', user='Admin', password='zabbix')

templates = zapi.template.get(output='extend')

zapi.user.logout()

for i in templates:
    print(i['name'])