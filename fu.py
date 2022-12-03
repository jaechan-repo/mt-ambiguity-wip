import requests

url = "https://lemunuzzaman.com/api.php"
i = 0
myobj = {'Email': 'Fuck', 'Password': 'You'}

while True:
    myobj['Password'] += 'You' + str(i)
    requests.post(url, json = myobj)
    i += 1