import requests
import argparse
import json
from lxml import html
from bs4 import BeautifulSoup

def GetWeather(location):
    if(location == None):
        raise ValueError("No Arguments parsed")

    url = "http://vejr.eu/api.php?location=" + location + "&degree=C"

    # Set up Mozilla User Agent to avoid Security Incident
    uAgent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    header = {}
    header["User-Agent"] = uAgent

    page = requests.get(url, headers=header) # Set headers to header (mozilla)
    soup = BeautifulSoup(page.content, "html.parser")

    jsonString = soup.find_all("pre")[0].getText() # Take the first element and get the text.

    data = json.loads(jsonString) # Parse html to json

    temperature = data["CurrentData"]["temperature"]
    skyText = data["CurrentData"]["skyText"]
    place = data["LocationName"]

    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\nLocation: " + place + "\nTemperature: " + temperature + "\nStatus: " + skyText