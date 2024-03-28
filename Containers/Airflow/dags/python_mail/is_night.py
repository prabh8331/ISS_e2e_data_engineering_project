import requests
import pytz
from datetime import datetime, timedelta

class IsNight:
    def get_data(self):
        my_latitude = 18.5894739
        my_longitude = 74.0105505
        parameters = {
            "lat" : my_latitude, 
            "lng" : my_longitude, 
            "formatted" : 0,
        }

        response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
        
        data = response.json()

        timezone_utc = pytz.timezone('UTC') 
        timezone_ist = pytz.timezone('Asia/Kolkata')

        sunset =  datetime.fromisoformat(data["results"]["sunset"]).replace(tzinfo=timezone_utc).astimezone(timezone_ist)
        sunrise =  datetime.fromisoformat(data["results"]["sunrise"]).replace(tzinfo=timezone_utc).astimezone(timezone_ist) + timedelta(days=1)

        time_now = datetime.now(timezone_ist)
        
        if time_now > sunset and time_now < sunrise:
            return True
        else:
            return False