import json
import scraper
import database
from datetime import datetime
from decimal import Decimal


def scrape_megabus(event, context):
    route_info = event
    date = route_info["date"]
    origin = route_info["origin"]
    destination = route_info["destination"]

    journeys_prices = scraper.get_prices(date, origin, destination)

    # boto3 float to decimal hack
    journeys_prices_dump = json.dumps(journeys_prices)
    journeys_prices = json.loads(journeys_prices_dump, parse_float=Decimal)

    # For now, assuming, journey aready exists in table
    for journey_id, prices in journeys_prices.items():
        price_by_numtix = database.get_journey(
            journey_id).get("price_by_numtix")
        price_by_numtix[datetime.utcnow().isoformat()] = prices
        database.update_journey(journey_id, price_by_numtix)

    return journeys_prices
