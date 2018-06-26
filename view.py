#!/usr/bin/env/ python3
import os
import cowsay
import getpass

def header():
	return '''
-------------------------------
|       Terminal Trader       |
|       $ Money Moves $       |
-------------------------------
           Main Menu
_______________________________
 [Command Option in Brackets]
- Buy Security      [B | Buy]
- Sell Security     [S | Sell]
- Lookup Company    [L | Lookup]
- Quote Security    [Q | Quote]
- Performance       [P | Performance]
- Holdings          [H | Holdings]
- Exit Menu         [E | Exit]

'''

def login_options():
	return '''
-------------------------------
|       Terminal Trader       |
|       $ Money Moves $       |
-------------------------------
           Main Menu
_______________________________
 [Command Option in Brackets]
- User Login        [L | Login]
- Create Account    [C | Create]
- Admin Login       [A | Admin]
- Exit Terminal     [E | Exit]

'''

def admin_options():
	return '''
      Super User Logged In
-------------------------------
|       Terminal Trader       |
|       $    Admin    $       |
-------------------------------
           Main Menu
_______________________________
 [Command Option in Brackets]
- Users List        [U | Usrs]
- Add User          [A | Add]
- Delete User       [D | Del]
- Leaderboard       [L | Leaders]
- Exit Terminal     [E | Exit]

'''

def admin_del():
	os.system('clear')
	return '''
-----------------------------
|         Deletion           |
|        $  Menu  $          |
------------------------------
*    Proceed with Caution    *
 [Command Option in Brackets]

- Delete User    [D | Delete]
- Return Home    [R | Return]

'''

def admin_users_menu():
	os.system('clear')
	return '''
-----------------------------
|        Users List          |
|        $  Menu  $          |
------------------------------

 [Command Option in Brackets]

- User Holdings  [H | Holdings]
- Return Home    [R | Return]

'''

def intro_UI():
	os.system('clear')
	cowsay.milk('Welcome, User!')
	print(login_options())
	user_input = input('Enter Command:  ').lower()
	return user_input

def login_UI():
	os.system('clear')
	username = input('Enter Username:  ').lower()
	password = getpass.getpass('Enter Password: ').lower()
	return username,password

def create_user_UI():
	os.system('clear')
	username = input('Select Username:    ').lower()
	while True:
		password = input('Select Password:    ').lower()
		password1 = input('Confirm Password:   ').lower()
		if password == password1:
			print('* Balance Requirement is $100,000 *')
			balance = 100000
			mrkt_val = 0
			return username,password,balance,mrkt_val
		else:
			print('Passwords dont match!')

def main_menu_UI():
	os.system('clear')
	print(header())
	user_input = input('Enter Command:  ').lower()
	return user_input

def admin_menu_UI():
	os.system('clear')
	print(admin_options())
	user_input = input('Enter Command:  ').lower()
	return user_input

def buy_UI():
	os.system('clear')
	print('Buy Stock')
	ticker_symbol = input('Ticker Symbol: ').lower()
	trade_volume = input('Trade Volume: ')
	return ticker_symbol,trade_volume

def sell_UI():
	os.system('clear')
	print('Sell Stock')
	ticker_symbol = input('Ticker Symbol: ').lower()
	trade_volume = input('Trade Volume: ')
	return ticker_symbol,trade_volume

def lookup_UI():
	os.system('clear')
	print('Look Up Company')
	company_name = input('Enter Name: ').lower()
	return company_name

def quote_UI():
	os.system('clear')
	print('Quote for Ticker')
	ticker_symbol = input('Ticker Symbol: ').lower()
	return ticker_symbol

def performance_UI():
	os.system('clear')
	print('Portfolio Performance\n')

