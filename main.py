#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from pprint import pprint
from flight_search import FlightSearch

data_manager = DataManager()


sheety_data = data_manager.get_data()

flight_search = FlightSearch()
# print(flight_search.get_iataCode("Paris"))

for data in sheety_data:
    if data["iataCode"] == '':
        data["iataCode"] = flight_search.get_iataCode(data["city"])

pprint(sheety_data)
data_manager.update_data(sheety_data)

