import json
import requests
import time
from http import HTTPStatus
import database
from datetime import datetime as dt


def pull_data(dep_date, num_tix, start_rt, end_rt):
    megabus_url = "https://uk.megabus.com/journey-planner/api/journeys"

    params = {
        "departureDate": dep_date,  # format 2019-10-10
        "originId": start_rt,
        "destinationId": end_rt,
        "totalPassengers": num_tix
    }
    resp = requests.get(megabus_url, params)
    if resp.status_code != HTTPStatus.OK:
        return None
    journeys = resp.json().get('journeys')
    if journeys == None or len(journeys) == 0:
        return None
    return journeys


def get_prices(dep_date, start_rt, end_rt):
    # print("Date: {} Route: {}-{}".format(dep_date, start_rt, end_rt)) #DEBUG
    prices = {}
    bus_capacity = 75  # assume max bus capacity is 74
    for i in range(1, bus_capacity):
        journeys = pull_data(dep_date, i, start_rt, end_rt)
        if journeys != None:
            for journey in journeys:
                if i == 1:
                    prices[journey['journeyId']] = [0]*bus_capacity
                prices[journey['journeyId']][i] = journey['price']/i
            # print(prices) #DEBUG
    return prices
