from dotenv import load_dotenv


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, original_location_code, destination_location_code, departure_date, return_date, price):
        load_dotenv()
        self.original_location_code = original_location_code
        self.destination_location_code = destination_location_code
        self.departure_date = departure_date
        self.return_date = return_date
        self.price = price

    @staticmethod
    def find_cheapest_flight(data):
        if not data:
            return None
        cheapest_flight = None
        lowest_price = float('inf')

        for flight in data:
            try:
                price = float(flight["price"]["total"])
                segments = flight['itineraries'][0]['segments']
                original_location_code = segments[0]['departure']['iataCode']
                destination_location_code = segments[0]['arrival']['iataCode']
                departure_date = segments[0]['departure']['at'].split("T")[0]

                # Optional return date (if round-trip)
                return_date = None
                if len(flight['itineraries']) > 1:
                    return_segments = flight['itineraries'][1]['segments']
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
