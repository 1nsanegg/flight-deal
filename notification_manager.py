import smtplib
from email.message import EmailMessage
from flight_data import FlightData
import os
from dotenv import load_dotenv


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self, flight_info: FlightData):
        load_dotenv()
        self.PASSWORD = os.getenv("PASSWORD")
        self.flight_info = flight_info

    def send_email(self):
        msg = EmailMessage()
        msg.set_content(
            f"Low price alert! Only ${self.flight_info.price} to fly from {self.flight_info.original_location_code} to {self.flight_info.destination_location_code}, on {self.flight_info.departure_date}")
        msg["Subject"] = "Let's go"
        msg["From"] = "trevorkhuat@gmail.com"
        msg["To"] = "tuan1214502@gmail.com"

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user="trevorkhuat@gmail.com", password=self.PASSWORD)
            connection.send_message(msg)
