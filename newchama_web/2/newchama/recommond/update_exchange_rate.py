#! /usr/bin/python
# -*- coding:utf-8 -*-
import urllib2
import json
import csv
import os
import datetime


def get_exchange_rate(currency_from, currency_to):
    yql_base_url = "https://query.yahooapis.com/v1/public/yql"
    yql_query = 'select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20("'+currency_from+currency_to+'")'
    paras = "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    yql_query_url = yql_base_url + "?q=" + yql_query + paras
    try:
        yql_response = urllib2.urlopen(yql_query_url)
        try:
            yql_json = json.loads(yql_response.read())
            rate = float(yql_json['query']['results']['rate']['Rate'])
            return rate
        except (ValueError, KeyError, TypeError):
            return None
    except IOError, e:
        return None


def update_exchange_rate():
    rates = []
    fields = ['source_currency', 'target_currency', 'rate', 'date']
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, 'exchange_rate.csv')
    with open(file_path, 'rU') as fr:
        rows = csv.DictReader(fr, fieldnames=fields, delimiter=',')
        for row in rows:
            rates.append(row)

    for rate_info in rates:
        latest_rate = get_exchange_rate(rate_info['source_currency'],
                                        rate_info['target_currency'])
        if latest_rate:
            rate_info['rate'] = latest_rate
            rate_info['date'] = datetime.datetime.today()

    with open(file_path, 'wb') as fw:
        dw = csv.DictWriter(fw, fieldnames=fields)
        for rate_info in rates:
            dw.writerow(rate_info)

if __name__ == '__main__':
    update_exchange_rate()

