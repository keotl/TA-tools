import requests

url = "https://gitlab.com/api/v4/users/1234567890/projects"

querystring = {"per_page":"100"}

headers = {
    'private-token': "TOKEN"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text);
