import requests

class SimpleWeatherApiClient:

    BASE_URL = "http://api.weatherapi.com/v1"

    def __init__(self, api_key):

        if not api_key or not isinstance(api_key, str):
            print("Error: API key is required and must be a string.")
            self.api_key = None
        else:
            self.api_key = api_key
            print("SimpleWeatherApiClient initialized.")

    def get_current_temperature(self, city):

        if not self.api_key:
             print("Error: API client not initialized with a valid key.")
             return None

        endpoint = "current.json"
        url = f"{self.BASE_URL}/{endpoint}"
        request_params = {'key': self.api_key, 'q': city}

        try:
            print(f"Requesting current weather for {city}...")
            response = requests.get(url, params=request_params)
            response.raise_for_status()

            data = response.json()

            temperature = data.get('current', {}).get('temp_c')

            if temperature is not None:
                return float(temperature)
            else:
                print(f"Could not find temperature data for '{city}'.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Network or request error for {city}: {e}")
            return None
        except Exception as e:
            print(f"An error occurred processing data for {city}: {e}")
            return None

    def get_temperature_after(self, city, days, hour=None):

        if not self.api_key:
             print("Error: API client not initialized with a valid key.")
             return None
        if not isinstance(days, int) or days <= 0:
            print("Error: 'days' must be a positive integer.")
            return None

        endpoint = "forecast.json"
        url = f"{self.BASE_URL}/{endpoint}"
        request_params = {'key': self.api_key, 'q': city, 'days': days}

        try:
            print(f"Requesting forecast for {city} ({days} days out)...")
            response = requests.get(url, params=request_params)
            response.raise_for_status()

            data = response.json()

            forecast_days_list = data.get('forecast', {}).get('forecastday', [])


            target_day_index = days - 1
            if target_day_index < 0 or target_day_index >= len(forecast_days_list):
                print(f"Forecast data for day {days} not available (Index {target_day_index} invalid).")
                return None

            target_day_data = forecast_days_list[target_day_index]

            if hour is not None:
                if not isinstance(hour, int) or not (0 <= hour <= 23):
                    print("Error: 'hour' must be an integer between 0 and 23.")
                    return None

                hourly_list = target_day_data.get('hour', [])
                if hour >= len(hourly_list):
                     print(f"Hourly data for hour {hour} not available.")
                     return None
                temperature = hourly_list[hour].get('temp_c')
                if temperature is None:
                     print(f"Temperature missing for hour {hour}.")
                     return None
                return float(temperature)
            # If no specific hour, return daily average
            else:
                avg_temperature = target_day_data.get('day', {}).get('avgtemp_c')
                if avg_temperature is None:
                    print(f"Average daily temperature missing for day {days}.")
                    return None
                return float(avg_temperature)

        except requests.exceptions.RequestException as e:
            print(f"Network or request error for forecast {city}: {e}")
            return None
        except Exception as e:
            print(f"An error occurred processing forecast data for {city}: {e}")
            return None

    def get_lat_and_long(self, city):

        if not self.api_key:
            print("Error: API client not initialized with a valid key.")
            return None, None

        endpoint = "current.json"
        url = f"{self.BASE_URL}/{endpoint}"
        request_params = {'key': self.api_key, 'q': city}

        try:
            print(f"Requesting location data for {city}...")
            response = requests.get(url, params=request_params)
            response.raise_for_status()

            data = response.json()
            location_data = data.get('location', {})
            lat = location_data.get('lat')
            lon = location_data.get('lon')

            if lat is not None and lon is not None:
                return float(lat), float(lon)
            else:
                print(f"Could not find coordinate data for '{city}'.")
                return None, None

        except requests.exceptions.RequestException as e:
            print(f"Network or request error getting coordinates for {city}: {e}")
            return None, None
        except Exception as e:
            print(f"An error occurred processing location data for {city}: {e}")
            return None, None


print("\n--- Testing SimpleWeatherApiClient ---")

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
API_KEY = "should put your own key here , not gonna leave mine 👀👀👀" #
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

client = SimpleWeatherApiClient(api_key=API_KEY)

if client.api_key:
    city = "London"
    print(f"\n--- Weather for {city} ---")

    current_temp = client.get_current_temperature(city)
    if current_temp is not None:
        print(f"Current temperature in {city}: {current_temp}°C")

    lat, lon = client.get_lat_and_long(city)
    if lat is not None and lon is not None:
        print(f"Coordinates for {city}: Latitude={lat}, Longitude={lon}")

    forecast_avg_temp = client.get_temperature_after(city, days=1)
    if forecast_avg_temp is not None:
        print(f"Forecast avg temp for {city} tomorrow (Day 1): {forecast_avg_temp}°C")

    forecast_specific_temp = client.get_temperature_after(city, days=2, hour=15)
    if forecast_specific_temp is not None:
        print(f"Forecast temp for {city} on Day 2 at 15:00: {forecast_specific_temp}°C")

    # Test an invalid city (optional, shows error handling)
    # print("\n--- Testing Invalid City ---")
    # invalid_city = "NotARealCityName123"
    # invalid_temp = client.get_current_temperature(invalid_city)
    # print(f"Current temperature for '{invalid_city}': {invalid_temp}")

else:
    print("\nSkipping API calls because the client could not be initialized (check API key).")

print("-" * 25)