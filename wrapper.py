#!/usr/bin/env/ python3
import json
import requests

def get_last_price(ticker_symbol):
	endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol='+ticker_symbol
	response = json.loads(requests.get(endpoint).text)
	last_price = response['LastPrice']
	return last_price
def get_ticker_symbol(company_name):
	endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input='+company_name
	# TODO Re-factor the following code so it doesn't just arbitrarily take the first
	#      thing in the iterable that's returned and assume it's the security we want
	response = json.loads(requests.get(endpoint).text)[0]
	ticker_symbol = response['Symbol']
	return ticker_symbol

