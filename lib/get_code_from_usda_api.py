import requests
import urllib.parse
import os

def get_code_from_usda_api(query):
    """
    get_code_from_usda_api: Queries the USDA Database API with free text
        associated with the BMR File's description of the food.
        Returns the 5-digit code
    """
    # Send request to the API
    url = "http://api.nal.usda.gov/ndb/search/?api_key=" + os.getenv("API_KEY") + "&format=json&"
    url += urllib.parse.urlencode({"q":query})
    try:
        res = requests.get(url).json()
    except:
        print(requests.get(url).text)

    # Check for errors. If there's no match, return an "UNKNOWN" result
    if ("errors" in res) or ("error" in res):
        if ('error' in res and res['error']['code'] == "OVER_RATE_LIMIT"):
            print("RATE LIMIT ERROR!!!!")
            exit(1)
        return ("UNKNOWN", "UNKNOWN")

    number = res['list']['item'][0]['ndbno']
    usda_description = res['list']['item'][0]['name']

    # Returns the 5-digit code associated with the closest match and text description from database
    return (number, usda_description)
