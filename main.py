# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData

from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()

amadeus_access_token = flight_search.get_new_token()
sheety_data = data_manager.get_data()
# Update the iata_code with actual value if it's empty
for data in sheety_data:
    if data["iataCode"] == '':
        data["iataCode"] = flight_search.get_iataCode(data["city"], amadeus_access_token)
        data_manager.update_data(data)
sheety_data_after_updated = data_manager.get_data()

for data in sheety_data_after_updated:
    city = data["city"]
    city_iata_code = data["iataCode"]
    all_city_available_flight = flight_search.search_fight_offers(city_iata_code, amadeus_access_token)

    cheapest_flight = FlightData.find_cheapest_flight(all_city_available_flight)
    print(f"Getting flights for {city} .....")
    if cheapest_flight is None:
        print(f"No direct flights found for {city}. Trying with stopovers...")
        stopover_flight = flight_search.search_fight_offers(city_iata_code, amadeus_access_token,
                                                                      is_direct=False)
        cheapest_flight = FlightData.find_cheapest_flight(stopover_flight)

    if cheapest_flight is None:
        print(f"{city} : N/A")
    else:
        try:
            print(f"{city}: {cheapest_flight.price}")
            if float(cheapest_flight.price) < float(data["lowestPrice"]):
                notification_manager = NotificationManager(cheapest_flight)
                notification_manager.send_email()
        except ValueError:
            print(f"Invalid lowest price for {city}: {data['lowestPrice']}")
