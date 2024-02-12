import time

import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd


def meteo_data(latitude, longitude, params):
    # Установки и запрос данных
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"

    responses = openmeteo.weather_api(url, params=params)
    if "current" in params.keys():
        # Получение первой подходящей локации
        response = responses[0]
        result = [[f"Координаты", f"{response.Latitude()}°E {response.Longitude()}°N"]]
        # result += f"Elevation {response.Elevation()} m asl" + "\n"	# result += f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}" + "\n"	# result += f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s" + "\n"
        current = response.Current()

        result.append([f"Текущее время", f"{time.gmtime(float(current.Time()))}"])
        result.append([f"Текущая температура 2м", f"{round(current.Variables(0).Value())}"])
        result.append([f"Текущая относительная влажность 2м", f"{round(current.Variables(1).Value())}"])
        result.append([f"Текущая температура", f"{round(current.Variables(2).Value())}"])
        result.append([f"Осадки", f"{round(current.Variables(3).Value())}"])
        result.append([f"Дождь", f"{round(current.Variables(4).Value())}"])
        result.append([f"Ливни", f"{round(current.Variables(5).Value())}"])
        result.append([f"Снегопад", f"{round(current.Variables(6).Value())}"])
        # result.append([f"weather_code", f"{current.Variables(7).Value()}"])
        result.append([f"Облачность",               f"{round(current.Variables(8).Value())}"])
        result.append([f"Давление",                 f"{round(current.Variables(9).Value())}"])
        result.append([f"Поверхностное давление",   f"{round(current.Variables(10).Value())}"])
        result.append([f"Скорость метра на 10м",    f"{round(current.Variables(11).Value())}"])
        result.append([f"Направление ветра на 10м", f"{round(current.Variables(12).Value())}"])
        result.append([f"Порывыв ветра на 10м",     f"{round(current.Variables(13).Value())}"])
    if "past_days" in params.keys():
        response = responses[0]

        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
        hourly_pressure_msl = hourly.Variables(2).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s"),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
        hourly_data["pressure_msl"] = hourly_pressure_msl

        hourly_dataframe = pd.DataFrame(data=hourly_data)
        result = hourly_dataframe
        result = [result["temperature_2m"].to_numpy(),
                   result['relative_humidity_2m'].to_numpy(),
                   result["pressure_msl"].to_numpy()]

    return result

lat, long = 80.6, 58.1
# # print(f"longitude: {lat}, latitude: {long}")
# paramsCurrent = {
#                 "latitude": lat,
#                 "longitude": long,
#                 "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation",
#                             "rain",
#                             "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure",
#                             "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
#                 "wind_speed_unit": "ms",
#                 "timezone": "Europe/Moscow",
#                 "forecast_days": 1
#             }


# paramsPrognose = {
#                 "latitude": lat,
#                 "longitude": long,
#                 "hourly": ["temperature_2m", "relative_humidity_2m", "pressure_msl"],
#                 "past_days": 92,
#                 "forecast_days": 1
#             }
# print(meteo_data(lat, long, paramsPrognose))