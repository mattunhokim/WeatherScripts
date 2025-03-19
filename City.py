import requests

def get_coordinates(city, state):
    """ Get latitude and longitude for a given city/state using OpenStreetMap's API. """
    geo_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "city": city,
        "state": state,
        "country": "USA",
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "MyWeatherScript/1.0 (kimatthew1258@gmail.com)"}

    response = requests.get(geo_url, params=params, headers=headers)

    if response.status_code == 200 and response.json():
        location = response.json()[0]
        return location["lat"], location["lon"]
    
    print("❌ Error: Unable to get coordinates. Check city and state spelling.")
    return None, None

def get_weather_forecast(city, state, latitude, longitude):
    """ Fetch 7-day weather forecast using National Weather Service API. """
    headers = {"User-Agent": "MyWeatherScript/1.0 (kimatthew1258@gmail.com)"}
    
    # Get weather metadata for location
    weather_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(weather_url, headers=headers)

    if response.status_code != 200:
        print("❌ Error: Unable to fetch weather data.")
        return

    weather_data = response.json()
    forecast_url = weather_data.get("properties", {}).get("forecast")

    if not forecast_url:
        print("❌ Error: Forecast data not available.")
        return

    # Get 7-day forecast
    forecast_response = requests.get(forecast_url, headers=headers)
    forecast_data = forecast_response.json()

    # Print forecast
    try:
        print(f"\n🌤️ 7-Day Forecast for {city.title()}, {state.upper()} 🌤️")
        print("========================================")

        for period in forecast_data["properties"]["periods"]:
            if "night" not in period["name"].lower():
                name = period["name"]
                temperature = period["temperature"]
                unit = period["temperatureUnit"]
                short_forecast = period["shortForecast"].replace(" then ", ", ")

                print(f"📅 {name}: {short_forecast}, High: {temperature}°{unit}")
    except KeyError:
        print("❌ Error: 'periods' key not found in forecast response.")

# Get user input
city = input("Enter city name: ").strip()
state = input("Enter state abbreviation (e.g., TX, CA): ").strip().upper()

# Tuple unpacking
lat, lon = get_coordinates(city, state)

if lat and lon:
    get_weather_forecast(city, state, lat, lon)
