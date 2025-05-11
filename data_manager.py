import os
from dotenv import load_dotenv
import requests


class DataManager:
    load_dotenv()

    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_token = os.getenv("SHEETY_BEAR_TOKEN")
        self.sheety_prices_endpoint = os.getenv("SHEETY_PRICES_ENDPOINT")
        self.sheety_users_endpoint = os.getenv("SHEETY_USERS_ENDPOINT")
        self.sheety_header = {"Authorization": f"Bearer {self.sheety_token}"}

    # This function get data from Google sheet
    def get_prices_sheet_data(self):
        sheety_get_endpoint = self.sheety_prices_endpoint
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
    def update_price_sheet_data(self, data):
        object_id = int(data["id"])
        sheety_put_endpoint = f"{self.sheety_prices_endpoint}/{object_id}"
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

    # This function get user's email from users sheet
    def get_user_email(self):
        sheety_get_users_endpoint = self.sheety_users_endpoint
        response = requests.get(url=sheety_get_users_endpoint, headers=self.sheety_header)
        users_list = []
        if response.status_code == 200:
            try:
                data = response.json()["users"]
                for user in data:
                    users_list.append(user["whatIsYourEmailCom"])
                return users_list
            except KeyError:
                print("Users key not found in the response")
                return []
        else:
            print(f"Received status code {response.status_code} from {sheety_get_users_endpoint}")
            return []

