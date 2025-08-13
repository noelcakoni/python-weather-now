#!/usr/bin/env python3
"""
Weather Now (Python CLI)

Fetch current weather for a city using the OpenWeatherMap API.

Usage:
  python weather_now.py "Boston" --units imperial
  python weather_now.py "Tirana" --units metric
  python weather_now.py "London,UK" --units metric --lang en
  # Or set your API key as an env var and omit --api-key:
  #   setx OPENWEATHER_API_KEY your_key_here   (Windows, new terminal)
  #   export OPENWEATHER_API_KEY=your_key_here (macOS/Linux)
"""
import os, sys, argparse, json
from datetime import datetime

API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Try to use requests if available; otherwise fall back to urllib
try:
    import requests
    def http_get(url, params):
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.text
except Exception:
    import urllib.request, urllib.parse
    def http_get(url, params):
        qs = urllib.parse.urlencode(params)
        with urllib.request.urlopen(url + "?" + qs, timeout=10) as resp:
            return resp.read().decode("utf-8")

def parse_args(argv):
    p = argparse.ArgumentParser(description="Get current weather from OpenWeatherMap.")
    p.add_argument("city", help='City name (e.g., "Boston", "London,UK", "Tirana,AL")')
    p.add_argument("--units", choices=["standard","metric","imperial"], default="metric",
                   help="Units for temperature/wind (metric=°C, m/s; imperial=°F, mph)")
    p.add_argument("--lang", default="en", help="Language for weather description")
    p.add_argument("--api-key", default=None, help="OpenWeatherMap API key (or set OPENWEATHER_API_KEY env var)")
    return p.parse_args(argv)

def get_api_key(cli_key):
    key = cli_key or os.environ.get("OPENWEATHER_API_KEY")
    if not key:
        sys.exit("Missing API key. Pass --api-key YOUR_KEY or set OPENWEATHER_API_KEY environment variable.")
    return key

def fetch_weather(city, units, lang, api_key):
    params = {"q": city, "appid": api_key, "units": units, "lang": lang}
    raw = http_get(API_URL, params)
    data = json.loads(raw)
    # Handle API errors
    if str(data.get("cod")) != "200":
        msg = data.get("message", "Unknown error")
        sys.exit(f"API error: {msg}")
    return data

def format_weather(data, units):
    name = data.get("name", "")
    sys_country = data.get("sys", {}).get("country", "")
    weather = (data.get("weather") or [{}])[0]
    main = data.get("main", {})
    wind = data.get("wind", {})
    dt = data.get("dt")
    ts = datetime.utcfromtimestamp(dt).strftime("%Y-%m-%d %H:%M UTC") if dt else ""

    unit_temp = "°C" if units == "metric" else ("°F" if units == "imperial" else "K")
    unit_wind = "m/s" if units != "imperial" else "mph"

    lines = [
        f"{name}, {sys_country} — {weather.get('description','').capitalize()}",
        f"Temp: {main.get('temp','?')}{unit_temp}  (feels like {main.get('feels_like','?')}{unit_temp})",
        f"Min/Max: {main.get('temp_min','?')}{unit_temp} / {main.get('temp_max','?')}{unit_temp}",
        f"Humidity: {main.get('humidity','?')}%   Pressure: {main.get('pressure','?')} hPa",
        f"Wind: {wind.get('speed','?')} {unit_wind}",
        f"Updated: {ts}",
    ]
    return "\n".join(lines)

def main(argv):
    args = parse_args(argv)
    key = get_api_key(args.api_key)
    data = fetch_weather(args.city, args.units, args.lang, key)
    print(format_weather(data, args.units))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
