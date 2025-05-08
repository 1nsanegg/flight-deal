import os

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
        header = {"Authorization": f"Bearer {self.get_new_token()}"}

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

