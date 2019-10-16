import json
import requests
import time
from http import HTTPStatus
from requests.exceptions import HTTPError
import database
from datetime import datetime as dt
from sentry_sdk import capture_exception, capture_message


def megabus_api(path, params):
    megabus_api_url = "https://uk.megabus.com/journey-planner/api/"
    url = megabus_api_url + path
    try:
        resp = requests.get(url, params)
        resp.raise_for_status()
    except HTTPError as http_err:
        capture_exception(http_err)
    except Exception as err:
        capture_exception(err)
    return resp


def travel_dates(start_rt, end_rt):
    path = "journeys/travel-dates"
    params = {
        "originCityId": start_rt,
        "destinationCityId": end_rt,
    }
    resp = megabus_api(path, params)
    dates = resp.json().get('availableDates')
    if dates == None or len(dates) == 0:
        return None
    return dates


def get_journeys(dep_date, num_tix, start_rt, end_rt):
    path = "journeys"
    params = {
        "departureDate": dep_date,  # format 2019-10-10
        "originId": start_rt,
        "destinationId": end_rt,
        "totalPassengers": num_tix
    }
    resp = megabus_api(path, params)
    journeys = resp.json().get('journeys')
    if journeys == None or len(journeys) == 0:
        return None
    return journeys


def get_prices(dep_date, start_rt, end_rt):
    prices = {}
    bus_capacity = 75  # assume max bus capacity is 74
    for i in range(1, bus_capacity):
        journeys = get_journeys(dep_date, i, start_rt, end_rt)
        if journeys != None:
            for journey in journeys:
                if i == 1:
                    prices[journey['journeyId']] = [0]*bus_capacity
                prices[journey['journeyId']][i] = journey['price']/i
    return prices
