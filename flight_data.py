

from dotenv import load_dotenv



class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, original_location_code, destination_location_code, departure_date, return_date, price):
        load_dotenv()
        self.original_location_code = original_location_code
        self.destination_location_code = destination_location_code
        self.departure_date = departure_date
        self.return_date = return_date
        self.price = price




