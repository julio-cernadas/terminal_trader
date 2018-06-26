#!/usr/bin/env/ python3
import sqlite3
import pandas as pd

import wrapper # In-Use
import mapper  # Not-In-Use_Yet

def buy(ticker_symbol,trade_volume,username):
	trade_volume = float(trade_volume)
	user_balance = mapper.select_balance(username)
	brokerage_fee = 6.95
	last_price = wrapper.get_last_price(ticker_symbol)
	print(last_price)
	transaction_cost = (last_price*float(trade_volume))+brokerage_fee
	if user_balance >= transaction_cost:
		ticker_symbols = mapper.select_ticker(ticker_symbol,username)

		if ticker_symbols == None: # If the holding exists. Continue...
			mapper.insert_to_holdings(ticker_symbol,trade_volume,last_price,username)

		else:
			x = mapper.select_holding(ticker_symbol,username)
			prev_volume = float(x[0])
			prev_price = float(x[1])
			# Calculating VWAP
			old = prev_volume * prev_price
			new = trade_volume * last_price
			total_vol = prev_volume + trade_volume
			new_vwap = (old + new) / (total_vol)
			mapper.update_holdings(total_vol,new_vwap,ticker_symbol,username)

		new_balance = user_balance - transaction_cost
		mrkt_value = market_value(username)
		new_mrkt_val = mrkt_value + new_balance
		mapper.update_balance(new_balance,new_mrkt_val,username)
		return 'Successful!'

	else:
		return 'Error: You do not have enough money to trade!'

def sell(ticker_symbol,trade_volume,username):
	trade_volume = float(trade_volume)
	user_balance = mapper.select_balance(username)
	ticker_symbols = mapper.select_ticker(ticker_symbol,username)
	brokerage_fee = 6.95
	last_price = wrapper.get_last_price(ticker_symbol)
	transaction_cost = (last_price*trade_volume)-brokerage_fee
	if ticker_symbols != None: # If the holding exists. Continue...
		x = mapper.select_holding(ticker_symbol,username)
		prev_volume = float(x[0])
		vwap = float(x[1])
		total_vol = prev_volume-trade_volume
		new_balance = user_balance + transaction_cost

		if prev_volume > trade_volume:
			mapper.update_holdings(total_vol,vwap,ticker_symbol,username)
			mrkt_value = market_value(username)
			new_mrkt_val = mrkt_value + new_balance
			mapper.update_balance(new_balance,new_mrkt_val,username)

		elif prev_volume == trade_volume:
			mapper.delete_holding(ticker_symbol,username)
			mrkt_value = market_value(username)
			new_mrkt_val = mrkt_value + new_balance
			mapper.update_balance(new_balance,new_mrkt_val,username)

		elif prev_volume < trade_volume:
			return 'You do not have that many shares!'
		return 'Successful!'
	else:
		return 'You do not have that stock!'

def portfolio_performance(username):
	user_balance = float(mapper.select_balance(username))
	mrkt_val = market_value(username)
	port_val = mrkt_val + user_balance
	PnL1 = port_val - 100000
	PnL2 = ((port_val - 100000)/100000.00)*100
	return 'Market Value: {0} | P/L: ${1} | {2}% | Balance Remaining: {3}'.format(port_val,PnL1,PnL2,user_balance)

def holdings_performance(username):
	df1 = mapper.pandas_connect(username)
	df = df1.drop(['pk','username'],axis=1)
	df.columns = ['Ticker','Shares','@Price']
	df['Init_Value'] = df['@Price']*df['Shares']
	last_prices = []
	for tkr in df['Ticker']:
		price = wrapper.get_last_price(tkr)
		last_prices.append(float(price))
	df['Mrkt_Price'] = last_prices
	df['Mrkt_Value'] = df['Mrkt_Price']*df['Shares']
	df['P/L'] = df['Mrkt_Value']-df['Init_Value']
	return df

def market_value(username):
	df = holdings_performance(username)
	mrkt_value = df['Mrkt_Value'].sum()
	return mrkt_value

def admin_users_list():
	df1 = mapper.admin_pandas_connect()
	df = df1.drop(['pk'],axis=1)
	return df

def leaderboard():
	df1 = mapper.select_leaderboards()

	return df1

# if __name__ == '__main__':
