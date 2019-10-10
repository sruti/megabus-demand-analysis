import json
import requests
from bs4 import BeautifulSoup
import time


def pull_data(dep_date, num_tix, start_rt, end_rt):
    megabus_url = "https://uk.megabus.com/journey-planner/journeys"

    params = {
        "departureDate": dep_date,  # format 2019-10-10
        "originId": start_rt,  # 56 Edinburgh
        "destinationId": end_rt,  # 34 London
        "totalPassengers": num_tix
    }
    resp = requests.get(megabus_url, params)
    return parse_data(resp.text)


def parse_data(text):
    soup = BeautifulSoup(text, "html.parser")
    journey_text = soup.find_all('script')[-1].text
    journey_data = journey_text.strip()[len("window.SEARCH_RESULTS = "): -1]
    journeys = json.loads(journey_data)['journeys']
    if len(journeys) == 0:
        return None
    prices = []
    for journey in journeys:
        prices.append(journey['price'])
    return prices


def get_ticket_price_by_capacity(dep_date, start_rt, end_rt):
    # print("Date: {} Route: {}-{}".format(dep_date, start_rt, end_rt))
    all_prices = []
    for i in range(1, 75):
        prices = pull_data(dep_date, i, start_rt, end_rt)
        if prices != None:
            prices = [total/i for total in prices]
            all_prices.append(prices)
            # print("{}:{}".format(i, prices))
        else:
            print("{}: None".format(i))
        time.sleep(.5)  # to prevent getting blocked
    return all_prices
