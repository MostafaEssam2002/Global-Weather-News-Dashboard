# Global Weather and News Dashboard Project

## Project Overview
Create a Python application that fetches weather data and news headlines for multiple cities around the world, processes this information, and presents it in a user-friendly format. This project will help you practice working with different APIs, handling JSON data, and performing basic data analysis.

---

## Learning Objectives

1. Interact with multiple APIs (both simple and REST).
2. Handle API authentication and parameters.
3. Process and analyze JSON data.
4. Perform error handling in API requests.
5. Create a simple data visualization.
6. Write data to files for persistent storage.

---

## Required Libraries

- `requests`
- `json`
- `pandas`
- `matplotlib`
- `dotenv` (for securing API keys)

---

## APIs to be used

1. **OpenWeatherMap API** (for weather data): [https://openweathermap.org/api](https://openweathermap.org/api)
2. **NewsAPI** (for news headlines): [https://newsapi.org/](https://newsapi.org/)

> Both APIs require free registration to obtain API keys.

---

## Project Requirements

1. Fetch weather data for at least 5 major cities around the world.
2. Fetch top headlines for each city's country.
3. Process and combine the weather and news data.
4. Create a summary report with the following:
   - Current weather conditions for each city.
   - 5-day weather forecast for each city.
   - Top 3 news headlines for each country.
5. Generate a simple visualization (e.g., a bar chart of temperatures across cities).
6. Save the raw data and the summary report to files.
7. Implement proper error handling and API key security.

---

## Starter Code

```python
import os
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys (store these in a .env file in your project directory)
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# List of cities to analyze
cities = ['New York', 'London', 'Tokyo', 'Sydney', 'Mumbai']

def get_weather_data(city):
    """Fetch weather data for a given city using OpenWeatherMap API"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_news_headlines(country_code):
    """Fetch top headlines for a given country code using NewsAPI"""
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': country_code,
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

def process_data(weather_data, news_data):
    """Process and combine weather and news data"""
    # TODO: Implement data processing logic
    pass

def create_visualization(data):
    """Create a visualization of the processed data"""
    # TODO: Implement visualization logic
    pass

def save_data(data, filename):
    """Save data to a file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    all_data = []
    for city in cities:
        try:
            weather = get_weather_data(city)

            # Note: You'll need to map city to country code for news API
            news = get_news_headlines('us')  # Placeholder, replace with actual country code
            processed_data = process_data(weather, news)
            all_data.append(processed_data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {city}: {e}")

    # TODO: Create summary report
    # TODO: Generate visualization
    # TODO: Save data and report to files

if __name__ == "__main__":
    main()
```

---

## Instructions for Students

1. Sign up for free API keys from OpenWeatherMap and NewsAPI.
2. Create a `.env` file in your project directory and add your API keys:

   ```
   OPENWEATHER_API_KEY=your_key_here
   NEWS_API_KEY=your_key_here
   ```

3. Implement the TODO sections in the starter code.
4. Extend the project by adding more cities, additional data points, or more complex visualizations.
5. Write a brief report discussing your findings and any challenges you encountered.

---

## Bonus Challenges

1. Implement caching to reduce API calls for repeated requests.
2. Create a simple web interface to display your dashboard using a framework like Flask.
3. Add historical data analysis by fetching and storing data over several days.

---

## Submission Guidelines

1. Submit your Python script(s) with all TODOs implemented.
2. Include any generated data files and visualizations.
3. Write a brief (1-2 page) report on your approach, findings, and reflections on the project.

---

This project will help you apply your API knowledge in a real-world scenario while also practicing data processing, visualization, and analysis skills.
