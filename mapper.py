#!/usr/bin/evn python3
import sqlite3
import pandas as pd


### CONNECTIONS ###
def connection():
	cursor = sqlite3.connect('master.db',check_same_thread=False).cursor()
	return cursor

def connect_commit():
	connection = sqlite3.connect('master.db',check_same_thread=False)
	return connection


### ACCOUNT CHECK ###
def check_existing(username,password):
	cursor = connection()
	cursor.execute("""SELECT username,password FROM users WHERE username='{}'
						AND password='{}';""".format(username,password))
	try:
		cursor.fetchall()[0][0]
		return username
	except IndexError:
		return None

def check_admin(username,password):
	cursor = connection()
	cursor.execute("""SELECT username,password FROM users WHERE username='{}'
						AND password='{}';""".format(username,password))
	try:
		cursor.fetchall()[0][0]
		return username
	except IndexError:
		return None


### SELECTS ###
def select_balance(username):
	cursor = connection()
	cursor.execute('SELECT balance FROM users WHERE username="{0}";'.format(username))
	user_balance = cursor.fetchall()[0][0]
	return user_balance

def select_ticker(ticker_symbol,username):
	cursor = connection()
	cursor.execute("""SELECT ticker_symbol FROM holdings WHERE ticker_symbol=
					'{0}' AND username='{1}';""".format(ticker_symbol,username))
	ticker_symbols = cursor.fetchone()
	return ticker_symbols

def select_holding(ticker_symbol,username):
	cursor = connection()
	cursor.execute(
		"""SELECT number_of_shares,volume_weighted_average_price
			FROM holdings WHERE ticker_symbol='{0}' AND username=
			'{1}';""".format(ticker_symbol,username))
	x = [i for i in cursor.fetchall()][0]
	return x

def select_leaderboards():
	connection = connect_commit()
	df = pd.read_sql_query(
		"""SELECT username,balance,mrkt_val
			FROM users
			WHERE balance > 0
			ORDER BY mrkt_val DESC
			LIMIT 10;""",connection)
	connection.close
	return df

def pandas_connect(username):
	connection = connect_commit()
	df = pd.read_sql_query('SELECT * FROM holdings WHERE username="{}"'.format(username),connection)
	connection.close
	return df

def admin_pandas_connect():
	connection = connect_commit()
	df = pd.read_sql_query('SELECT * FROM users',connection)
	connection.close
	return df


### INSERTS ###
def insert_to_holdings(ticker_symbol,trade_volume,last_price,username):
	connection = connect_commit()
	cursor = connection.cursor()
	cursor.execute(
		"""INSERT INTO holdings(
			ticker_symbol,number_of_shares,volume_weighted_average_price,username)
			VALUES('{0}',{1},{2},'{3}');""".format(ticker_symbol,trade_volume,last_price,username))
	connection.commit()
	cursor.close()
	connection.close()

def insert_account(username,password,balance,mrkt_val):
	connection = connect_commit()
	cursor = connection.cursor()
	cursor.execute(
		"""INSERT INTO users(
			username, password, balance, mrkt_val) Values('{}','{}',{},{});""".format(
			username, password, balance, mrkt_val))
	connection.commit()
	cursor.close()
	connection.close()


### UPDATES ###
def update_holdings(total_vol,new_vwap,ticker_symbol,username):
	connection = connect_commit()
	cursor = connection.cursor()
	cursor.execute(
		"""UPDATE holdings SET number_of_shares={0},volume_weighted_average_price={1}
		WHERE ticker_symbol='{2}' AND username='{3}';""".format(
		total_vol,new_vwap,ticker_symbol,username))
	connection.commit()
	cursor.close()
	connection.close()

def update_balance(new_balance,new_mrkt_val,username):
	connection = connect_commit()
	cursor = connection.cursor()
	cursor.execute(
		"""UPDATE users
		SET balance={0},mrkt_val={1}
		WHERE username='{2}';""".format(new_balance,new_mrkt_val,username))
	connection.commit()
	cursor.close()
	connection.close()


### DELETES ###
def delete_holding(ticker_symbol,username):
	connection = connect_commit()
	cursor = connection.cursor()
	cursor.execute('''SELECT rowid FROM holdings WHERE ticker_symbol=
						"{0}" and username="{1}";'''.format(ticker_symbol,username))
	id = cursor.fetchall()[0][0]
	cursor.execute('DELETE FROM holdings WHERE rowid={0};'.format(id,))
	connection.commit()
	cursor.close()
	connection.close()

def delete_user(username):
	connection = connect_commit()
	cursor = connection.cursor()
	cursor.execute('SELECT rowid FROM users WHERE username="{0}";'.format(username))
	try:
		id = cursor.fetchall()[0][0]
		cursor.execute('DELETE FROM users WHERE rowid={0};'.format(id,))
		connection.commit()
		cursor.close()
		connection.close()
		return 'Success'
	except IndexError:
		return None
