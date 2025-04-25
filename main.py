import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import requests
from datetime import datetime, timezone
import smtplib

MY_LAT = "" # Your latitude
MY_LONG = "" # Your longitude
MY_EMAIL = "<YOUR EMAIL>"
PASSWORD = "<YOUR APP PASSOWRD>"  # Replace with your App Password
TO_EMAIL = "<YOUR TEST EMAIL>"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
def check_pos(my_lat, my_long, iss_lat, iss_long):
    if (int(my_lat-iss_lat) in range(-5,6)) and (my_long-iss_long in range(-5,5)):
        return True
    else:
        return False
def check_time(srise, sset, now):

    if now in range(sset,srise):
        return True
    else:
        return False




parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data['results']["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
time_now = datetime.now(timezone.utc)

message = MIMEMultipart()
message['From'] = MY_EMAIL
message['To'] = TO_EMAIL
message['Subject'] = "ISS Above YOU "
cleaned_message = "LOOK UP 👁️👁️☝️🛰️"
message.attach(MIMEText(cleaned_message,'plain'))

filename = "ISS.jpg"
# Read and encode image as base64
with open(filename, "rb") as img_file:
    encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

    # Create HTML content with embedded image
    html = f"""
    <html>
      <body>
        <img src="data:image/jpeg;base64,{encoded_string}" alt="ISS IMAGE" style="width:400px;">
      </body>
    </html>
"""

message.attach(MIMEText(html,"html"))



for i in range(2):
    if check_pos(MY_LAT, MY_LONG, iss_latitude, iss_longitude):
        if check_time(sunrise,sunset,time_now.hour):


            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL,
                                    to_addrs=TO_EMAIL,
                                    msg=message.as_string())
    time.sleep(5)




