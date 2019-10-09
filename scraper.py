import json
import requests
from bs4 import BeautifulSoup


def pull_data(dep_date, num_tix, start_rt, end_rt):
    megabus_url = "https://uk.megabus.com/journey-planner/journeys"

    params = {
        "departureDate": dep_date,  # format 2019-10-10
        "originId": start_rt,  # 56 Edinburgh
        "destinationId": end_rt,  # 34 London
        "totalPassengers": num_tix
    }
    resp = requests.get(megabus_url, params)
    parse_data(resp.text)


def parse_data(text):
    soup = BeautifulSoup(text, "html.parser")
    journey_text = soup.find_all('script')[-1].text
    journey_data = journey_text.strip()[len("window.SEARCH_RESULTS = "): -1]
    journeys = json.loads(journey_data)['journeys']
    for journey in journeys:
        print(journey['price'])


pull_data("2019-10-13", 10, 56, 34)
