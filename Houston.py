import requests 

# URL for where the api is stored.
url = "https://api.weather.gov"
# Set up the headers required by the API.
# The User-Agent header identifies your application. Including contact info is recommended.
headers = {
    "User-Agent": "MyWeatherScript/1.0 (kimatthew1258@gmail.com)"

}
# Send a GET request to the API URL with the specified headers.
response = requests.get(url, headers=headers)

# Print the HTTP status code of the response to see if the request was successful.
print("Status Code:", response.status_code)

try:
    # Attempt to parse the response content as JSON.     
    data = response.json()
    print("Response JSON:")
    # Print the parsed JSON data.
    print(data)
except Exception as e:
    # If there's an error during JSON parsing, print the error message.
    print("Error parsing JSON:", e)

# Get Houston weather metadata
houston_url = "https://api.weather.gov/points/29.7604,-95.3698"
houston_response = requests.get(houston_url, headers = headers)
houston_data = houston_response.json()

# Extract the 7-day forecast URL from the Houston data
houston_forecast_url = houston_data["properties"]["forecast"]

# Request the actual forecast
forecast_response = requests.get(houston_forecast_url, headers = headers)
forecast_data = forecast_response.json()

#Print 7-day forecast
try:
    print("🌤️ 7-Day Forecast for Houston, TX 🌤️")
    print("========================================")
    
    for period in forecast_data["properties"]["periods"]:
        if "night" not in period["name"].lower():  # Filter out night forecasts
            name = period["name"]  
            temperature = period["temperature"]
            unit = period["temperatureUnit"]
            short_forecast = period["shortForecast"]
            
            print(f"📅 {name}: {short_forecast}, High: {temperature}°{unit}")
except KeyError:
    print("Error: 'periods' key not found in forecast response.")