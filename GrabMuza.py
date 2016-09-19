#!/usr/bin/python3
# coding: utf8

from datetime import datetime, date, time
from grab import Grab

# import logging
# from pprint import pprint
# logging.basicConfig(level=logging.DEBUG)

url = "http://www.muzadisk.ru"
tickets = "/tickets.html"

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
                                                if element5.getchildren():
                                                    for element6 in element5.getchildren():
                                                        if element6.getchildren():
                                                            for element7 in element6.getchildren():
                                                                if element7.text is not None:
                                                                    values_list.append(element7.text)
                                                        else:
                                                            if element6.text is not None:
                                                                values_list.append(element6.text)
                                                else:
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
    #print(values_list)
    if values_list[2] is not None:
        dates = values_list[2].split()
        if dates[0].isnumeric() and lenps >= 6:
            event['img'] = values_list[0]
            event['band'] = values_list[1]
            event['day'] = dates[0].strip(',.')
            event['month'] = months[dates[1].strip(',.')]
            if len(dates) >= 3:
                event['year'] = dates[2]
            else:
                event['year'] = cur_year
            event['place'] = values_list[3].strip()
            event['addr'] = values_list[4]
            event['price'] = values_list[5]
            return event
        else:
            #print(values_list)
            pass
    else:
        #print(values_list)
        pass


g = Grab()
end_page = False;
while end_page == False:
    g.go(url+tickets)
    posters = g.doc.select('//div[@class="dd-article"]')
    pages = g.doc.select('//div[@class="dd-pager"]//a[@title="Вперёд"]');
    try:
        tickets = pages.attr('href')
    except:
        end_page=True

    for poster in posters:
        parsed_event = parse(poster)
        if parsed_event is not None:
            print(parsed_event)
