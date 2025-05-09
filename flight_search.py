import os
import datetime
from flight_data import FlightData
import requests
from dotenv import load_dotenv


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    load_dotenv()

    def __init__(self):
        self.amadeus_api_key = os.getenv("amadeus_api_key")
        self.amadeus_api_secret = os.getenv("amadeus_api_secret")

    def get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        get_token_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.amadeus_api_key,
            'client_secret': self.amadeus_api_secret
        }
        response = requests.post(url=get_token_endpoint, headers=header, data=body)
        if response.status_code == 200:
            try:
                access_token = response.json()["access_token"]
                return access_token
            except KeyError:
                print("Error: access_token key not found in the response.")
                return []
        else:
            print(f"Received status code {response.status_code}")
            return []

    @staticmethod
    def get_iataCode(city_name, token):
        get_city_iata_code_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        param = {
            "keyword": city_name
        }
        header = {"Authorization": f"Bearer {token}"}
        response = requests.get(url=get_city_iata_code_endpoint, headers=header, params=param)
        if response.status_code == 200:
            try:
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

    @staticmethod
    def search_fight_offers(destination_location_code, token):
        fight_offers_endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        departure_date = datetime.datetime.now() + datetime.timedelta(days=1)
        return_date = datetime.datetime.now() + datetime.timedelta(weeks=26)
        param = {
            "originLocationCode": "LON",
            "destinationLocationCode": destination_location_code,
            "departureDate": departure_date.strftime("%Y-%m-%d"),
            "returnDate": return_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP"
        }
        header = {"Authorization": f"Bearer {token}"}
        response = requests.get(url=fight_offers_endpoint, params=param, headers=header)
        if response.status_code == 200:
            try:
                all_flight = response.json()["data"]
                return all_flight
            except KeyError:
                print("data key not found.")
                return []
        else:
            print(f"Received status code {response.status_code}")
            return []


