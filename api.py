import requests
url = "https://api-football-v1.p.rapidapi.com/v3/teams/league/128"
headers = {
    'x-apisports-host': "v3.football.api-sports.io",
    'x-apisports-key': "09d1ab5e3cf7f087a82915004a769d76"
    }
response = requests.request("GET", url, headers=headers)
print(response.text)