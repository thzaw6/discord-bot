import requests
import json
import os

# def dadjoke():
#     url = "https://dad-jokes.p.rapidapi.com/random/joke"
#     headers = {
#         "X-RapidAPI-Key": "83da7047dcmsha159618d209dc07p198031jsn3cb742305818",
#         "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com",
#     }

#     response = requests.get(url, headers=headers)
#     json_data = json.loads(response.text)
#     setup = json_data["body"][0]["setup"]
#     punchline = json_data["body"][0]["punchline"]

def ip():
    url = "https://api.ipgeolocation.io/ipgeo?apiKey=" + "a6e78a9634784668ba9f6bff910b6b89"
    response = requests.get(url)
    json_data = json.loads(response.text)
    ip = json_data["ip"]
    time = json_data["time_zone"]["current_time"]
    print("your ip is: " + ip)
    print("current time: " + time[:19])


ip()