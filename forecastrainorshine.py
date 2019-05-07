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

    def get_temperature(self, day):
        """ Get the temperature for the day for the cities"""
        return self.temps[day]

    def __str__(self):
        """Return the name of the class and space in the memory"""
        return self.name


class Route:
    """ A route represents a sequence of cities """

    def __init__(self, city_list):
        # assuming city_list is a list containing object of the City class
        self.cities = city_list

    def avg_temp(self):
        temp = 0
        for k in range(len(self.cities)):
            temp += self.cities[k].get_temperature(k)
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

    # try:
    id_list = json.loads(open("cities.json").read())
    cities = []
    for id in id_list:
        cities.append(fetch_weather(id))
        avg_temp = 0

    for c in range(len(cities)):
    #get the sum of the highest temp and devide by days
        city = cities[c]
        print(city, ": " + str(city.get_temperature(c)))
        avg_temp += city.get_temperature(c)

    avg_temp /= len(cities)

    
    print(avg_temp)


    #print(cities[0], cities[1], cities[2], cities[3], cities[4])
    #for cp in range(len(cities)):
    #listcities = cities[cp].name
    cities_list = [cities[0].name, cities[1].name, cities[2].name, cities[3].name, cities[4].name]
    cities_temp_list = [cities[0]]
    p = list(permutations(list(cities_list)))
    print(p)
# Route(p)

# except:
# print("File is not available.")
