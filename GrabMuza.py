#!/usr/bin/python3
# coding: utf8

import sys, time, os
from grab import Grab
import logging
from pprint import pprint

# logging.basicConfig(level=logging.DEBUG)

url = "http://www.muzadisk.ru"
tickets = "/tickets.html"

months = dict()
months['января'] = "01"
months['февраля'] = "02"
months['марта'] = "03"
months['апреля'] = "04"
months['мая'] = "05"
months['июня'] = "06"
months['июля'] = "07"
months['августа'] = "08"
months['сентября'] = "09"
months['октября'] = "10"
months['ноября'] = "11"
months['декабря'] = "12"


def parse(poster_div):
    event = dict()
    values_list = list()
    values_list.append(url+poster_div.select('p//img').attr('src'))
    for ps in poster_div._node.xpath('p'):
        if ps.getchildren():
            for element in ps.getchildren():
                if element.getchildren():
                    for element2 in element.getchildren():
                        if element2.getchildren():
                            for element3 in element2.getchildren():
                                if element3.getchildren():
                                    for element4 in element3.getchildren():
                                        if element4.getchildren():
                                            for element5 in element4.getchildren():
                                                if element5.text is not None:
                                                    values_list.append(element5.text)
                                        else:
                                            if element4.text is not None:
                                                values_list.append(element4.text)

                                else:
                                    if element3.text is not None:
                                        values_list.append(element3.text)
                        else:
                            values_list.append(element2.text)
                else:
                    if element.text is not None:
                        values_list.append(element.text)
        else:
            values_list.append(ps.text)
    i = 0
    for value in values_list:
        if value is '\xa0':
            values_list.pop(i)
        i += 1
    dates = values_list[2].strip('.').split()
    event['img'] = values_list[0]
    event['band'] = values_list[1]
    event['day'] = dates[0]
    event['month'] = months[dates[1]]
    event['year'] = '2016'
    event['place'] = values_list[3].strip()
    event['addr'] = values_list[4]
    event['price'] = values_list[5]
    return event

g = Grab()
g.go(url+tickets)
posters = g.doc.select('//div[@class="dd-article"]')

for poster in posters:
    parsed_event = parse(poster)
    print(parsed_event)
