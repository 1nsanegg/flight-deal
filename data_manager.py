import os
from dotenv import load_dotenv
import requests
from pprint import pprint

class DataManager:

    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        load_dotenv()
        self.sheety_token = os.getenv("sheety_bearer_token")
        self.header = {"Authorization" : f"{self.sheety_token}"}



    def get_data(self):
        sheety_get_endpoint = "https://api.sheety.co/cc92f9f277a3d6e4ad5f0c900edfbf73/bảnSaoCủaFlightDeals/prices"
        response = requests.get(url=sheety_get_endpoint, headers=self.header)
        data = response.json()["prices"]
        return data

    def update_data(self, update_data):

        for data in update_data:
            object_id = int(data["id"])
            sheety_put_endpoint = f"https://api.sheety.co/cc92f9f277a3d6e4ad5f0c900edfbf73/bảnSaoCủaFlightDeals/prices/{object_id}"
            request_param = {
                "price": data
            }
            response = requests.put(url=sheety_put_endpoint,headers=self.header, json=request_param)
