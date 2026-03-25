# Weeeather Widget — worker.py
# Fetche la meteo via Open-Meteo (gratuit, pas d'API key)
# Geolocalisation par IP via ip-api.com

import js
import asyncio
import json


async def get_location():
    """Recupere lat/lon/ville via IP geolocation."""
    try:
        resp = await js.fetch("http://ip-api.com/json/?fields=lat,lon,city")
        data = (await resp.json()).to_py()
        return {
            "lat": data["lat"],
            "lon": data["lon"],
            "city": data.get("city", ""),
        }
    except Exception as e:
        log("[weather] geoloc error: " + str(e))
        return None


async def get_weather(lat, lon):
    """Fetche la meteo actuelle + forecast du jour via Open-Meteo."""
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude={}&longitude={}"
            "&current=temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m"
            "&daily=temperature_2m_max,temperature_2m_min,weather_code"
            "&timezone=auto"
            "&forecast_days=3"
        ).format(lat, lon)

        resp = await js.fetch(url)
        data = (await resp.json()).to_py()
        return data
    except Exception as e:
        log("[weather] weather API error: " + str(e))
        return None


def weather_label(code):
    """Convertit un code meteo Open-Meteo en texte."""
    code = int(code)
    if code == 0:
        return "Clair"
    elif code in (1, 2, 3):
        return ("Degage", "Nuageux", "Couvert")[code - 1]
    elif code in (45, 48):
        return "Brouillard"
    elif code in (51, 53, 55):
        return "Bruine"
    elif code in (56, 57):
        return "Bruine gelee"
    elif code in (61, 63, 65):
        return ("Pluie leg.", "Pluie", "Forte pluie")[code // 2 - 30]
    elif code in (66, 67):
        return "Pluie verglas"
    elif code in (71, 73, 75):
        return "Neige"
    elif code == 77:
        return "Grains"
    elif code in (80, 81, 82):
        return "Averses"
    elif code in (85, 86):
        return "Averses neige"
    elif code in (95, 96, 99):
        return "Orage"
    return "?"


def weather_icon(code):
    """Retourne un symbole texte pour le code meteo."""
    code = int(code)
    if code == 0:
        return "*"
    elif code in (1, 2):
        return "~"
    elif code == 3:
        return "="
    elif code in (45, 48):
        return "%"
    elif code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
        return "'"
    elif code in (71, 73, 75, 77, 85, 86):
        return "."
    elif code in (95, 96, 99):
        return "!"
    return "?"


async def fetch_and_send():
    """Pipeline complet : geoloc -> meteo -> envoi au device."""
    log("[weather] fetching location...")
    loc = await get_location()
    if not loc:
        send_rpc("weather.data", {"found": False, "error": "geoloc"})
        return

    log("[weather] location: " + loc["city"] + " (" + str(loc["lat"]) + ", " + str(loc["lon"]) + ")")

    weather = await get_weather(loc["lat"], loc["lon"])
    if not weather:
        send_rpc("weather.data", {"found": False, "error": "api"})
        return

    current = weather.get("current", {})
    daily = weather.get("daily", {})

    # Aujourd'hui
    temp = current.get("temperature_2m", 0)
    code = current.get("weather_code", 0)
    wind = current.get("wind_speed_10m", 0)
    humidity = current.get("relative_humidity_2m", 0)

    temp_max = daily.get("temperature_2m_max", [0])[0]
    temp_min = daily.get("temperature_2m_min", [0])[0]

    # Forecast J+1, J+2
    forecast = []
    dates = daily.get("time", [])
    maxs = daily.get("temperature_2m_max", [])
    mins = daily.get("temperature_2m_min", [])
    codes = daily.get("weather_code", [])

    for i in range(1, min(3, len(dates))):
        forecast.append({
            "date": dates[i],
            "max": maxs[i] if i < len(maxs) else 0,
            "min": mins[i] if i < len(mins) else 0,
            "code": codes[i] if i < len(codes) else 0,
            "label": weather_label(codes[i] if i < len(codes) else 0),
            "icon": weather_icon(codes[i] if i < len(codes) else 0),
        })

    payload = {
        "found": True,
        "city": loc["city"],
        "temp": round(temp, 1),
        "temp_max": round(temp_max, 1),
        "temp_min": round(temp_min, 1),
        "code": code,
        "label": weather_label(code),
        "icon": weather_icon(code),
        "wind": round(wind, 1),
        "humidity": int(humidity),
        "forecast": forecast,
    }

    log("[weather] sending: " + str(payload))
    send_rpc("weather.data", payload)


def handle_notify(method, params):
    if method == "weather.fetch":
        asyncio.ensure_future(fetch_and_send())


register_notify("weather.fetch")
log("[weather] Weeeather worker started")
