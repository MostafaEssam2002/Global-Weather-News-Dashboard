import os
import requests
import json
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
if not OPENWEATHER_API_KEY or not NEWS_API_KEY:
    raise ValueError("API keys for OpenWeatherMap and NewsAPI must be set in the .env file.")
cities_info = [
    {'city': 'New York', 'country_code': 'us'},
    {'city': 'Cairo', 'country_code': 'eg'},   
    {'city': 'Tokyo', 'country_code': 'jp'},
    {'city': 'Sydney', 'country_code': 'au'},
    {'city': 'Mumbai', 'country_code': 'in'}
]
def get_weather_data(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
    weather_params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    try:
        current_weather_response = requests.get(base_url, params=weather_params, timeout=10)
        current_weather_response.raise_for_status()
        current_weather_data = current_weather_response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current weather for {city}: {e}")
        return None, None
    forecast_params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    try:
        forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast for {city}: {e}")
        return current_weather_data, None
    return current_weather_data, forecast_data
 
def get_news_headlines(city):
    base_url = "https://newsapi.org/v2/everything"
    params = {
        'q': city,
        'apiKey': NEWS_API_KEY,
        'language': 'en',
        'sortBy': 'relevancy',
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news for {city}: {e}")
        return None
def process_data(city, weather_data, forecast_data, news_data):
    if not weather_data or not forecast_data:
        print(f"Missing weather or forecast data for city: {city}. Skipping processing.")
        return None
    current_weather = {
        'city': city,
        'temperature': weather_data['main']['temp'],
        'description': weather_data['weather'][0]['description']
    }
    forecast = []
    for i, entry in enumerate(forecast_data['list']):
        if i % 8 == 0:
            forecast.append({
                'date': entry['dt_txt'],
                'temperature': entry['main']['temp'],
                'description': entry['weather'][0]['description']
            })
    if news_data and 'articles' in news_data and news_data['articles']:
        top_headlines = [article['title'] for article in news_data['articles'][:3]]
    else:
        top_headlines = ["No news available"]
    return {
        'city': city,
        'current_weather': current_weather,
        'forecast': forecast,
        'news_headlines': top_headlines
    }
def create_visualization(data):
    cities = [item['city'] for item in data if item]
    temperatures = [item['current_weather']['temperature'] for item in data if item]
    plt.figure(figsize=(10, 6))
    plt.bar(cities, temperatures, color='skyblue')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.title('Current Temperatures in Various Cities')
    plt.tight_layout()
    plt.show()
def create_report(data):
    report = []
    for city_data in data:
        if not city_data:
            continue
        city_report = f"City: {city_data['city']}\n"
        city_report += f"Current Weather: {city_data['current_weather']['temperature']}°C, {city_data['current_weather']['description']}\n"
        city_report += "5-Day Forecast:\n"
        for day in city_data['forecast']:
            city_report += f"Date: {day['date']}, Temp: {day['temperature']}°C, Description: {day['description']}\n"
        city_report += "Top 3 News Headlines:\n"
        for headline in city_data['news_headlines']:
            city_report += f"- {headline}\n"
        city_report += "=" * 50 + "\n"
        report.append(city_report)
    with open('summary_report.txt', 'w') as f:
        f.writelines(report)
    print("Report saved to summary_report.txt")
def save_data(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error saving data to {filename}: {e}")
all_data = []
for city_info in cities_info:
    city = city_info['city']
    weather_data, forecast_data = get_weather_data(city)
    news_data = get_news_headlines(city)
    processed_data = process_data(city, weather_data, forecast_data, news_data)
    if processed_data:
        all_data.append(processed_data)
    else:
        print(f"Skipping city {city} due to missing data.")
if all_data:
    create_visualization(all_data)
    create_report(all_data)
    save_data(all_data, 'weather_news_data.json')
else:
    print("No data available to generate report or visualization.")
