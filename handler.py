import json
import scraper


def scrape_megabus(event, context):
    route_info = event
    date = route_info["date"]
    origin = route_info["origin"]
    destination = route_info["destination"]

    data = scraper.get_prices(date, origin, destination)

    return data
