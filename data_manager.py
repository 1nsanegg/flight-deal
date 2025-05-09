import os
from dotenv import load_dotenv
import requests


class DataManager:
    load_dotenv()

    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_token = os.getenv("SHEETY_BEAR_TOKEN")
        self.sheety_header = {"Authorization": f"Bearer {self.sheety_token}"}

    # This function get data from Google sheet
    def get_data(self):
        sheety_get_endpoint = "https://api.sheety.co/cc92f9f277a3d6e4ad5f0c900edfbf73/bảnSaoCủaFlightDeals/prices"
        response = requests.get(url=sheety_get_endpoint, headers=self.sheety_header)
        # Handle exception when API call fail or price key not found
        if response.status_code == 200:
            try:
                data = response.json()["prices"]
                return data
            except KeyError:
                print("Error: prices key not found in the response.")
                return []
        else:
            print(f"Received status code {response.status_code} from {sheety_get_endpoint}")
            return []

    # This function update data in Google sheet
    def update_data(self, data):
        object_id = int(data["id"])
        sheety_put_endpoint = f"https://api.sheety.co/cc92f9f277a3d6e4ad5f0c900edfbf73/bảnSaoCủaFlightDeals/prices/{object_id}"
        request_param = {
            "price": data
        }
        response = requests.put(url=sheety_put_endpoint, headers=self.sheety_header, json=request_param)

        # handle exception when API call failed
        if response.status_code == 200:
            print("Data updated successfully")
        else:
            print(f"Failed to update data from . Status code {response.status_code}")
            print(response.text)
