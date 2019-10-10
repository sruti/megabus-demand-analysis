import json
import requests
from bs4 import BeautifulSoup
import time
from http import HTTPStatus
import database
import datetime


def pull_data(dep_date, num_tix, start_rt, end_rt):
    megabus_url = "https://uk.megabus.com/journey-planner/journeys"

    params = {
        "departureDate": dep_date,  # format 2019-10-10
        "originId": start_rt,
        "destinationId": end_rt,
        "totalPassengers": num_tix
    }
    resp = requests.get(megabus_url, params)
    if resp.status_code != HTTPStatus.OK:
        return None
    return resp.text


def parse_data(text):
    soup = BeautifulSoup(text, "html.parser")
    journey_text = soup.find_all('script')[-1].text
    journey_data = journey_text.strip()[len("window.SEARCH_RESULTS = "): -1]
    journeys = json.loads(journey_data).get('journeys')
    if journeys == None or len(journeys) == 0:
        return None
    return journeys


def get_price_by_capacity(dep_date, start_rt, end_rt):
    # print("Date: {} Route: {}-{}".format(dep_date, start_rt, end_rt)) #DEBUG
    all_prices = []
    for i in range(1, 75):  # assume max bus capacity is 74
        data_text = pull_data(dep_date, i, start_rt, end_rt)
        if data_text != None:
            journeys = parse_data(data_text)
            prices = [journey['price'] for journey in journeys]
            # TODO: Separate price lists by service
            if prices != None:
                prices = [total/i for total in prices]
                all_prices.append(prices)
                # print("{}:{}".format(i, prices)) #DEBUG
            # else:
                # print("{}: None".format(i)) #DEBUG
    return all_prices


def map_journey_data(journey):
    origin = journey['origin']['cityId']
    destination = journey['destination']['cityId']
    depart_datetime = datetime.datetime.fromisoformat(
        journey['departureDateTime'])
    trip_date = depart_datetime.date().isoformat
    start_time = depart_datetime.time().isoformat
    end_time = journey['arrivalDateTime'].time().isoformat
    duration = journey['duration']
    service = {
        "service_id": database.set_service_id(origin, destination, start_time, end_time),
        "origin": origin,
        "destination": destination,
        "trip_date": trip_date,
        "start_time": start_time,
        "end_time": end_time,
        "duration": duration,
        "price_by_capacity": {}
    }
    return service


def load_new_services():
    data_text = pull_data("2019-10-13", 1, 56, 34)
    journeys = parse_data(data_text)
    services = [map_journey_data(journey) for journey in journeys]
    db_responses = [database.put_data(service) for service in services]
    # TODO: Check responses for failure
    return
