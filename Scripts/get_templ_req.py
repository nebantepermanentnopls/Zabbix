import requests
import json

URL = 'http://172.20.10.5:3000/api_jsonrpc.php'
HEADER = {'content-type': 'application/json'}

# auth token
auth_data = {'jsonrpc': '2.0',
             'method': 'user.login',
             'params': {'user': 'Admin',
                        'password': 'zabbix'},
             'auth': None,
             'id': 0}
auth = requests.post(URL, data=json.dumps(auth_data), headers=HEADER)

# get templates
template_data = {'jsonrpc': '2.0',
                 'method': 'template.get',
                 'params': {'output': 'extend'},
                 'auth': auth.json()['result'],
                 'id': 1}
templates = requests.post(URL, json=template_data, headers=HEADER)

# logout token
noauth_data = {'jsonrpc': '2.0',
               'method': 'user.logout',
               'params': [],
               'auth': auth.json()['result'],
               'id': 2}
noauth = requests.post(URL, json=noauth_data, headers=HEADER)

for i in templates.json()['result']:
    print(i['name'])


