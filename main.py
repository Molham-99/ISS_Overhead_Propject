import requests
from datetime import datetime
import smtplib

MY_EMAIL = "Example@****.com"
MY_PASSWORD = "************"
MY_LAT = 50.075539   # Your latitude
MY_LONG = 14.437800  # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
time_now = datetime.now()
is_on = True
while is_on:
    if int(iss_longitude) in range(int(MY_LONG)-5, int(MY_LONG)+5) and\
            int(iss_latitude) in range(int(MY_LAT)-5, int(MY_LAT)+5):
        if time_now.hour not in range(4, 17):
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL,
                                    to_addrs="Example@*****.com",
                                    msg="Subject: Hello,\n\nLook up! ")
                is_on = False
