# import requests
import requests

# Sending the request
requests = requests.get('http://api.open-notify.org/astros.json')
data = requests.json()

# check status code
print(requests.status_code)

# For the people in space print out their names and what space craft they are on
for p in data['people']:
    print(p['name'])
    print(p['craft'])


