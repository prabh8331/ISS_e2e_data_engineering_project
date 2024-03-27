import requests

import datetime

class RequestData:
    def get_data(self):
        response = requests.get("http://api.open-notify.org/iss-now.json")
        data_json = response.json()
        data = {}
        data['timestamp'] = datetime.datetime.fromtimestamp(data_json['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        data['longitude'] = data_json['iss_position']['longitude']
        data['latitude'] = data_json['iss_position']['latitude']
        
        return data

