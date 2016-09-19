#!/usr/bin/python3
# coding: utf8

from datetime import datetime, date, time
from grab import Grab
import json

url = "http://www.muzadisk.ru"
tickets = "/tickets.html"

def get_child(elements):
    for element in elements.getchildren():
        return element

def parse(poster_div):
    months = dict()
    months['января'] = 1
    months['февраля'] = 2
    months['марта'] = 3
    months['апреля'] = 4
    months['мая'] = 5
    months['июня'] = 6
    months['июля'] = 7
    months['августа'] = 8
    months['сентября'] = 9
    months['октября'] = 10
    months['ноября'] = 11
    months['декабря'] = 12

    cur_year = datetime.now().timetuple()[0]
    event = dict()
    values_list = list()
    values_list.append(url+poster_div.select('p//img').attr('src'))
    lenps = len(poster_div._node.xpath('p'))
    #print(lenps)
    for ps in poster_div._node.xpath('p'):
        element = ps
        while element.getchildren():
            element = get_child(element)
        values_list.append(element.text)

    i = 0
    for value in values_list:
        if value is '\xa0':
            values_list.pop(i)
        i += 1
    if len(values_list) == 8:
        values_list[2] = values_list[2] + " " + values_list[3]
        values_list.pop(3)

    #print(values_list)
    if values_list[3] is not None:
        dates = values_list[3].split()
        if dates[0].isnumeric() and lenps >= 5:
            event['img'] = values_list[0]
            event['band'] = values_list[2]
            event['day'] = dates[0].strip(',.')
            event['month'] = months[dates[1].strip(',.')]
            if len(dates) >= 3:
                event['year'] = dates[2]
            else:
                event['year'] = cur_year
            event['place'] = values_list[3].strip()
            event['addr'] = values_list[5]
            event['price'] = values_list[6]
            return event
        else:
            print(values_list)
            pass
    else:
        print(values_list)
        pass


g = Grab()
end_page = False;
x = 0
while end_page == False:
    g.go(url+tickets)
    posters = g.doc.select('//div[@class="dd-article"]')
    pages = g.doc.select('//div[@class="dd-pager"]//a[@title="Вперёд"]');
    try:
        tickets = pages.attr('href')
    except:
        end_page = True

    x += len(posters)
    for poster in posters:
        parsed_event = parse(poster)
        if parsed_event is not None:
            print(parsed_event)
            # pass
