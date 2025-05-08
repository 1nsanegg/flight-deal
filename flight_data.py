from operator import truediv

import requests
from dotenv import load_dotenv
import os
class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, token):
        load_dotenv()
        self.amadues_api_key = os.getenv("amadeus_api_key")
        self.amadues_api_secret = os.getenv("amadeus_api_secret")
        self.token = token

    def search_fight_offers(self, destination_location_code, departure_date, return_date):
        fight_offers_endpoint = "test.api.amadeus.com/v2/shopping/fight-offers"
        param = {
            "originLocationCode" : "LON",
            "destinationLocationCode" : destination_location_code,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": 1,
            "nonStop": True,
            "currencyCode": "GBP"
        }
        header = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url=fight_offers_endpoint, params=param, headers=header)
        data = response.json()
        return data
