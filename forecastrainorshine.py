"""
This program will take in 5 cities and use openweathermap api to get the information and find
the best way to travel to according to temperature
"""

import requests
import json
from itertools import permutations

API_KEY = "391ca8dca14d4a785f9d52917910b3fe"
WS_URL = "https://api.openweathermap.org/data/2.5/forecast"


class City:
    """ Representing a city including the forecast max temps for each of the next 5 days """

    def __init__(self, name, temperatures):
        self.name = name
        self.temps = temperatures

    """ Get the temperature for the day for the cities"""

    def get_temperature(self, day):
        return self.temps[day]

    def __str__(self):
        return self.name


class Route:
    """ A route represents a sequence of cities """

    def __init__(self, city_list):
        # assuming city_list is a list containing object of the City class
        self.cities = city_list

    def avg_temp(self):
        temp = 0
        for j in range(len(self.cities)):
            temp += self.cities[j].get_temperature(j)
        temp /= len(self.cities)
        print(temp)
        return temp

    def __str__(self):
        # todo maybe use old join to create string containing the route city 1 : city 2 :
        pass


def fetch_weather(id):
    # request parameter(s): Start with '?'
    # separate name and value with '='
    # multiple parameter name value pairs are separate with '&'
    query_string = "?id={}&units=imperial&APIKEY={}".format(id, API_KEY)
    request_url = WS_URL + query_string
    print("Request URL: ", request_url)
    response = requests.get(request_url)
    # todo try except
    try:
        if response.status_code == 200:
            d = response.json()
            city_name = d["city"]['name']
            lst = d['list']
            tmp_list = []
            for i in range(len(lst) // 8):
                li = [x for x in range(len(lst)) if x // 8 == i]
                tmp_list.append(max([lst[j]["main"]["temp_max"] for j in li]))
            return City(city_name, tmp_list)
        else:
            print("How should I know?")
            return None
    except:
        print("It appears there is no connection to get information needed.")

if __name__ == "__main__":

    try:
        id_list = json.loads(open("cities.json").read())
        cities = []
        for id in id_list:
            cities.append(fetch_weather(id))
            avg_temp = 0

        for i in range(len(cities)):
            city = cities[i]
            print(city, ": " + str(city.get_temperature(i)))
            avg_temp += city.get_temperature(i)

        avg_temp /= len(cities)
        print(avg_temp)

        p = list(permutations(range(len(cities))))
        print(p)

    except:
        print("File is not available.")
