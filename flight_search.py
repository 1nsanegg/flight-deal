import os
import datetime
from flight_data import FlightData
import requests
from dotenv import load_dotenv



class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        load_dotenv()
        self.amadues_api_key = os.getenv("amadeus_api_key")
        self.amadues_api_secret = os.getenv("amadeus_api_secret")
        self._get_new_token = self.get_new_token()


    def get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        get_token_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.amadues_api_key,
            'client_secret': self.amadues_api_secret
        }
        response = requests.post(url=get_token_endpoint, headers=header, data=body)
        return response.json()["access_token"]

    def get_iataCode(self, city_name):
        get_city_iata_code_enpoint = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        param = {
            "keyword" : city_name
        }
        header = {"Authorization": f"Bearer {self._get_new_token}"}

        try:
            response = requests.get(url=get_city_iata_code_enpoint, headers=header,params=param )
            response.raise_for_status()
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                iata_code = data["data"][0]["iataCode"]
                if iata_code:
                    return iata_code
                else:
                    print(f"No IATA code found for {city_name}")
                    return None
            else:
                print(f"NO city data return for: {city_name}")
                return None
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print("Likely cause: API rate limit or bad request.")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"Request failed: {req_err}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def search_fight_offers(self, destination_location_code, token):
        fight_offers_endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        param = {
            "originLocationCode" : "LON",
            "destinationLocationCode" : destination_location_code,
            "departureDate": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            # "returnDate": (datetime.datetime.now() + datetime.timedelta(weeks=52)).strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP"
        }
        header = {"Authorization": f"Bearer {token}"}
        response = requests.get(url=fight_offers_endpoint, params=param, headers=header)
        all_flight = response.json()["data"]
        return all_flight

    def find_cheapest_flight(self, all_flight):
        if not all_flight:
            return None

        cheapest_flight = None
        lowest_price = float('inf')

        for data in all_flight:
            try:
                price = float(data["price"]["total"])
                segments = data['itineraries'][0]['segments']
                original_location_code = segments[0]['departure']['iataCode']
                destination_location_code = segments[0]['arrival']['iataCode']
                departure_date = segments[0]['departure']['at'].split("T")[0]

                # Optional return date (if round-trip)
                return_date = None
                if len(data['itineraries']) > 1:
                    return_segments = data['itineraries'][1]['segments']
                    return_date = return_segments[0]['departure']['at'].split("T")[0]

                if price < lowest_price:
                    lowest_price = price
                    cheapest_flight = FlightData(
                        original_location_code,
                        destination_location_code,
                        departure_date,
                        return_date,
                        price
                    )
            except (KeyError, IndexError, ValueError) as e:
                print(f"Skipped a flight due to error: {e}")
                continue

        return cheapest_flight