import requests

class ISSoverhead:
    def get_data(self):
        my_latitude = 18.5894739
        my_longitude = 74.0105505
        response = requests.get("http://api.open-notify.org/iss-now.json")
        data_json = response.json()
        iss_longitude = float(data_json['iss_position']['longitude'])
        iss_latitude = float(data_json['iss_position']['latitude'])
        
        #Check if ISS position is within +5 or -5 degrees of my position to verify if ISS is present to my visible sky
        if (my_latitude-5 <= iss_latitude <= my_latitude+5) and ( my_longitude-5 <= iss_longitude <= my_longitude+5):
            return True
        else:
            return False

