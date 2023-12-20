from typing import Optional
import requests
import json
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim


class WeatherForecast:
    def __init__(self):
        self.file="opady.json"
        self.data : Optional[dict]=None

    def read_file(self):
        with open(self.file) as file:
            self.data=json.loads(file.read())

    def write_data_to_file(self):
        with open(self.file, mode= "w") as file:
            file.write(json.dumps(self.data))

    def get_coordinates(self, city):
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)
        if location:
            return location.latitude, location.longitude
        else:
            print("Podane miasto nie istnieje. Spróbuj ponownie.")
            return None, None

    def check_rainfall(self, weather_data):
        if "hourly" in weather_data and "rain" in weather_data["hourly"]:
            rainfall_sum = sum(weather_data["hourly"]["rain"])
            if rainfall_sum > 0.0:
                return "Będzie padać"
            elif rainfall_sum == 0.0:
                return "Nie będzie padać"
        return "Nie wiem"

    def get_weather_data(self, latitude, longitude, timezone, searched_date):
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone={timezone}&start_date={searched_date}&end_date={searched_date}"
        response = requests.get(api_url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Nie udało się pobrać danych. Kod błędu: {response.status_code}")
            return None

    def __getitem__(self, item):
        search_city, search_data= item

        for city_key, city_data in self.data.items():
            if search_city==city_key:
                for data, information in city_data.items():
                    if search_data==data:
                        return f'{information} w dniu {search_data} w {search_city}'


        return None

    def __setitem__(self, key, value):
        city,search_data = key
        self.data[city][search_data] = value
        self.save_to_file()
        print(self.data)


    def items(self):
        for city,city_data in self.data.items():
            for data, result in city_data.items():
                yield f"{city},{data}:{result}"

    def __iter__(self):

        return iter(self.data)

    def save_to_file(self, filename):
        with open(filename, "w") as file:
            json.dump(self.data, file, indent=2)

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}