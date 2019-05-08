#!/usr/bin/env python3

import http.client
import json
import locale
import argparse

class Stat:
    country_name = ''
    population = ''

    def __init__(self, name, population):
        self.country_name = name
        self.population = population
    
    def __str__(self):
        return f'{self.country_name} {locale.format("%d", self.population, grouping=True)}'


# method for getting a single page
def getResultsForSubstring(substring, page_number):
    
    # set up connection
    conn = http.client.HTTPSConnection("jsonmock.hackerrank.com")
    headers = {'Content-type': 'application/json'}

    #fire
    conn.request("GET", f"/api/countries/search?name={substring}&page={page_number}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))


def parsePageResults(numberOfPages, substring, population):
    stats = []

    for x in range(1, numberOfPages + 1):
        #fetch page
        page = getResultsForSubstring(substring, x)

        for country in page['data']:

            if country['population'] > population:
                stats.append(Stat(country['name'], country['population']))
    
    return stats


if __name__ == "__main__":
    description = "Get a sum and optional list of countries with a specific substring in their name\
         and a population greater than the specified value"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('substring', type=str, help='substring to be searched for')
    parser.add_argument('-p', '--population', type=int, help='minimum population', default=150000000)
    parser.add_argument('-l', '--list', action='store_true', help='display list of countries and their populations')
    args = parser.parse_args()


    # set local to US to get commas as a thousands separator,
    # specifically population in our case
    locale.setlocale(locale.LC_ALL, 'en_US')

    returned_json = getResultsForSubstring(args.substring, 1)
    
    stats = parsePageResults(returned_json['total_pages'], args.substring, args.population)

    # print list if flag was set
    if args.list == True:
        for stat in stats:
            print(stat)
    
    print(f"{len(stats)}")
    