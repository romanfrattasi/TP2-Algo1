import requests
url = "https://api-football-v1.p.rapidapi.com/v2/teams/league/128"
headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "ea4550b62906e6b4a627ad666d52394f"
    }
response = requests.request("GET", url, headers=headers)
print(response.text)