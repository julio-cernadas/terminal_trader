#!/usr/bin/env python3
import sqlite3

connection = sqlite3.connect('master.db',check_same_thread=False)
cursor     = connection.cursor()

cursor.execute(
    """CREATE TABLE users(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(16) UNIQUE,
        password VARCHAR(32),
        balance FLOAT,
        mrkt_val FLOAT
    );"""
)

cursor.execute(
    """CREATE TABLE holdings(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker_symbol VARCHAR UNIQUE,
        number_of_shares INTEGER,
        volume_weighted_average_price FLOAT,
        username VARCHAR(16),
        	FOREIGN KEY(username) REFERENCES users(username)
    );"""
)

cursor.execute(
    """CREATE TABLE orders(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        unix_time FLOAT,
        transaction_type BOOL,
        last_price FLOAT,
        trade_volume INTEGER
    );"""
)

cursor.close()
connection.close()
