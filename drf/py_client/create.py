import requests

headers = {
    'Authorization': 'Bearer d0b5a6a1a7e6ae48f20577f20d14feeb79fb4a70'
}
endpoint = "http://localhost:8000/api/products/"

data = {
    'title':'this field is done',
    'price':'32.99' 
}
get_response = requests.post(endpoint,data,headers=headers)

print(get_response.json())