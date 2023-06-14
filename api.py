import requests
url = "https://api-football-v1.p.rapidapi.com/v3/teams/league/128"
headers = {
    'x-apisports-host': "v3.football.api-sports.io",
    'x-apisports-key': "d0b3d415d1b1ae06f1698e7fcb0a3943"
    }
response = requests.request("GET", url, headers=headers)
print(response.text)