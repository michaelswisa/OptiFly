import packege.of_calculations
from packege import *
from datetime import datetime


def creat_json_targets(path_csv, path_json, key):
    csv_data = file.read_csv(path_csv)
    targets_list = []
    for row in csv_data[1:]:
        cuantry = row[0]
        location = request.get_location(cuantry, key)
        weather_of_cuntry = request.get_weather(cuantry, key)

        dict_weather_of_cuntry = filter_one_dey_weather(weather_of_cuntry, "2024-09-13 00:00:00")
        distance = of_calculations.haversine_distance(location[0]['lat'], location[0]['lon'])
        new_targets = {'City': row[0], 'Priority': row[1], 'lat': location[0]['lat'], 'lon': location[0]['lon'],
                       'distance': distance}

        combo_dict = {**new_targets, **dict_weather_of_cuntry}
        targets_list.append(combo_dict)

    file.write_json(path_json, targets_list)
    return


def filter_one_dey_weather(data, date_string):
    target_datetime = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

    for entry in data['list']:
        dt_txt = entry['dt_txt']
        dt = datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')
        if dt == target_datetime:
            score_weather = weather.weather_score(entry['weather'][0]['main'])
            new_dict = {'weather': score_weather, 'clouds': entry['clouds']['all'],
                        'wind_speed': entry['wind']['speed'], }
            return new_dict

    return {}
