#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from pprint import pprint
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

data_manager = DataManager()
sheety_data = data_manager.get_data()
flight_search = FlightSearch()


# print(flight_search.get_iataCode("Paris"))
token = flight_search.get_new_token()
for data in sheety_data:
    if data["iataCode"] == '':
        data["iataCode"] = flight_search.get_iataCode(data["city"])
        data_manager.update_data(data)

sheety_data_after_updated = data_manager.get_data()
print(sheety_data_after_updated)
for data in sheety_data_after_updated:
    iata_Code = data["iataCode"]
    all_flight = flight_search.search_fight_offers(iata_Code, token)
    city = data["city"]
    cheapest_flight = flight_search.find_cheapest_flight(all_flight)
    print(f"Getting flights for {city} .....")
    if cheapest_flight is None:
        print(f"{city} : N/A")
    else:
        print(f"{city} : {cheapest_flight.price}")
        if float(cheapest_flight.price) < float(data["lowestPrice"]):
            notification_manager = NotificationManager(cheapest_flight)
            notification_manager.send_email()

# pprint(flight_data.search_fight_offers("PAR"))
# data = flight_data.search_fight_offers("PAR")
# print(flight_data.find_cheapest_flight(data))


