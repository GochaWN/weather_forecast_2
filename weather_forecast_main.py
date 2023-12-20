from weather_forecast import WeatherForecast
from datetime import datetime, timedelta
import json
import requests
from geopy.geocoders import Nominatim

def main():
    print("Witaj w programie prognozy pogody.")
    weather_forecast = WeatherForecast()
    weather_forecast.load_from_file("opady.json")
    weather_forecast.read_file()


    city = input("Podaj miasto: ").strip()

    latitude, longitude = weather_forecast.get_coordinates(city)
    if latitude is None or longitude is None:
        return

    user_date_input = input("Podaj date w formacie YYYY-MM-DD: ").strip()

    if not user_date_input:
        search_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        search_date = user_date_input
    print(weather_forecast[city, search_date])

    filename = "opady.json"

    stored_data = weather_forecast.load_from_file("opady.json")
    if stored_data is not None:
        if city in stored_data and search_date in stored_data[city]:
            result = stored_data[city][search_date]
            print(f'{city},{search_date}')
    else:
        weather_data = weather_forecast.get_weather_data(latitude, longitude, "Europe%2FLondon", search_date)

        if weather_data:
            result = weather_forecast.check_rainfall(weather_data)
            if stored_data is not None:
                if city not in stored_data:
                    stored_data[city] = {}
                stored_data[city][search_date] = result
                weather_forecast.save_to_file(filename)

    print(f"Prognoza opadow na {search_date} w {city}: {result}")

    print(weather_forecast[city,search_date])

    weather_forecast.write_data_to_file()

    for info in weather_forecast.items():
        print(info)

    for info in weather_forecast:
        print(info)






if __name__ == "__main__":
    main()