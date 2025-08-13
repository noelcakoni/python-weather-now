# Weather Now

A simple Python script that shows the current weather for any city using live data from the OpenWeatherMap API.  
It’s quick to run in the terminal and works with both metric and imperial units.

## How to run
1. Get a free API key from https://openweathermap.org/api.
2. Save your API key as an environment variable:
   - Windows: setx OPENWEATHER_API_KEY your_key_here
   - macOS/Linux: export OPENWEATHER_API_KEY=your_key_here
3. From the project folder, run:
   python weather_now.py "Boston" --units imperial
   python weather_now.py "Tirana" --units metric

## Features
- Real-time weather for any city
- Choose metric or imperial
- Works straight from the terminal

## Tech
Python, Requests, Argparse, OpenWeatherMap API
