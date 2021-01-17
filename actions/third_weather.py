# -*- coding: utf-8 -*-
# @File  : third_weather.py
# @Author: LVFANGFANG
# @Date  : 2021/1/17 3:50 下午
# @Desc  :

import requests

KEY = 'e5a7084f0bcc4d86a9a1128bc15bca3f'


def get_location_id(location):
    url = 'https://geoapi.qweather.com/v2/city/lookup'
    params = {
        'location': location,
        'key': KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    location = response.json()['location']
    location_id = location[0]['id'] if location else None

    return location_id


def get_weather(location_id):
    url = f'https://devapi.qweather.com/v7/weather/3d'
    params = {
        'location': location_id,
        'key': KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_weather_by_day(location, day=1):
    location_id = get_location_id(location)
    weather_data = get_weather(location_id)
    result = {
        'location': location,
        'result': weather_data['daily'][day]
    }
    return result


if __name__ == '__main__':
    print(get_weather_by_day('深圳', 1))
