import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE+ 'storygen/Samarth likes/50')
print(response)
print(response.json())
