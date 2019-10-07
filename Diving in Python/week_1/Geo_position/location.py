import requests
import pprint

def get_location_info():
    return requests.get("http://ip-api.com/json/").json()

if __name__ == "__main__":
    pprint.pprint(get_location_info())