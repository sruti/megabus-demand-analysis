import json
import os
from datetime import datetime
from decimal import Decimal
import scraper
import database
import notification
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

sentry_key = os.environ.get("SENTRY_KEY")
sentry_project = os.environ.get("SENTRY_PROJECT")

sentry_sdk.init(
    dsn="https://{}@sentry.io/{}".format(sentry_key, sentry_project),
    integrations=[AwsLambdaIntegration()]
)


def scrape_megabus(event, context):
    route_info = json.loads(event['Records'][0]['Sns']['Message'])
    date = route_info["date"]
    origin = route_info["origin"]
    destination = route_info["destination"]

    journeys_prices = scraper.get_prices(date, origin, destination)

    # boto3 float to decimal hack
    journeys_prices_dump = json.dumps(journeys_prices)
    journeys_prices = json.loads(journeys_prices_dump, parse_float=Decimal)

    for journey_id, prices in journeys_prices.items():
        journey = database.get_journey(journey_id)
        if journey != None:
            price_by_numtix = journey.get("price_by_numtix")
            price_by_numtix[datetime.utcnow().isoformat()] = prices
            database.update_journey(journey_id, price_by_numtix)
        else:
            price_by_numtix = {}
            price_by_numtix[datetime.utcnow().isoformat()] = prices
            database.put_journey({
                "journey_id": journey_id,
                "price_by_numtix": price_by_numtix,
                "date": date,
                "origin": origin,
                "destination": destination})

    return "Success"


def trigger_scrape_megabus(event, context):
    origin = 56  # Edinburgh
    destination = 34  # London

    dates = scraper.travel_dates(origin, destination)
    if dates != None:
        for date in dates:
            notification.send_scrape_params(json.dumps({
                "origin": origin,
                "destination": destination,
                "date": date
            }))
    return "Success"


def get_journey_data(event, context):
    # TODO: setup as endpoint, takes journeyid as parameter
    # returns all price data
    journey_id = json.loads(event)['queryParameters']['journey_id']
    journey = database.get_journey(journey_id)
    return {
        "status": 200,
        "msg": journey
    }
