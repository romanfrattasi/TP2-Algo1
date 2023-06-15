import requests

#PRE:
#POST:
def llamado_api(url: str, payload: dict):
    headers = {
        "x-rapidapi-key": "ea4550b62906e6b4a627ad666d52394f",
        "x-rapidapi-host": "v3.football.api-sports.io"
    }

    response = requests.get(url, headers=headers, params=payload)
    return response

