##!/usr/bin/python
# -*- coding: utf-8 -*-

""" This module donwloads stocks daily historical prices and saves to a MongoDB database
"""
# Python standard modules
import json
import requests
from datetime import datetime

# External modules
import pymongo
from bs4 import BeautifulSoup


def get_data(ticker, url):
    """ Get stock historical prices from advfn website """
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    open_price = float(soup.find('span', id='quoteElementPiece12').text.replace(',', '.'))
    low_price = float(soup.find('span', id='quoteElementPiece13').text.replace(',', '.'))
    high_price = float(soup.find('span', id='quoteElementPiece14').text.replace(',', '.'))
    close_price = float(soup.find('span', id='quoteElementPiece15').text.replace(',', '.'))

    stock_quotation = {
        'ticker': ticker,
        'open': open_price,
        'high': high_price,
        'low': low_price,
        'close': close_price,
        'date': datetime.today().replace(microsecond=0)
    }
    print(stock_quotation)
    return stock_quotation


def get_conn():
    """ Get MongoDB Database credentials """
    with open('conn.json', 'r') as f:
        credentials = json.load(f)

    username = credentials['username']
    password = credentials['password']
    hostname = credentials['hostname']
    collection = credentials['collection']

    conn = f'mongodb+srv://{username}:{password}@{hostname}/{collection}?retryWrites=true&w=majority'
    return conn


def save_data(data):
    """ Saves stock historical prices to a MongoDB Database """
    client = pymongo.MongoClient(get_conn())
    database = client['stocks']
    collection = database['daily_prices']
    var = collection.insert_one(data)
    print(var.inserted_id)


def main():
    prices = get_data(
        ticker='ENJU3',
        url='https://br.advfn.com/bolsa-de-valores/bovespa/enjoei-com-br-atividades-on-ENJU3/cotacao'
    )
    save_data(prices)


if __name__ == '__main__':
    main()
