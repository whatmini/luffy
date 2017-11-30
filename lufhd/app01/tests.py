import requests


ret = requests.post(
    url='http://127.0.0.1:8000/login/',
    data={
        'username':'gangdan',
        'password':'123'
    }
)
print(ret.text)