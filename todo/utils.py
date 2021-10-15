import requests

from Cybersmart import settings


def get_weather(location):
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?units=metric&q={}&APPID={}".format(location,
                                                                                                settings.API_KEY)
        )
        return response.json()["main"]["temp"]
    except Exception as error:
        # Log Error message
        print("Error returning the temperature for city {} - Error Message: {}".format(location, error))
