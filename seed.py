#!/usr/bin/env python3
import sqlite3


connection = sqlite3.connect('master.db',check_same_thread=False)
cursor     = connection.cursor()

cursor.execute(
	"""INSERT INTO users(
		username,
		password,
		balance,
		mrkt_val) VALUES(
		'admin',
		'pass',
		0.00,
		0.00);""")

connection.commit()
cursor.close()
connection.close()
