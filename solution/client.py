import requests

url = "http://localhost:8000/"

# POST /guess
response = requests.request(
    method="POST", url=url + "guess", json={"player": "Julian"}
)
print(response.text)

# GET /guess
response = requests.request(method="GET", url=url + "guess")
print(response.text)

# GET /guess
response = requests.request(method="GET", url=url + "guess/?player=Julian")
print(response.text)
