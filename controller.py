#!/usr/bin/env/ python3
import model
import wrapper
import mapper
import view
import sqlite3

def log_in():
	user_login_inputs  = ['l','login']
	create_account_inputs = ['c','create']
	admin_login_inputs = ['a','admin']
	exit_inputs =['e','exit']
	allowed_inputs = user_login_inputs + create_account_inputs\
	+ admin_login_inputs + exit_inputs
	user_input = view.intro_UI()
	if user_input in allowed_inputs:
		if user_input in user_login_inputs:
			username,password = view.login_UI()
			username = mapper.check_existing(username,password)
			return username
		elif user_input in create_account_inputs:
			username,password,balance,mrkt_val = view.create_user_UI()
			mapper.insert_account(username,password,balance,mrkt_val)
			return username
		elif user_input in admin_login_inputs:
			username,password = view.login_UI()
			username = mapper.check_admin(username,password)
			return username
		elif user_input in exit_inputs:
			print('\nExiting, Good Bye!')
			return 'exit'
	else:
		return None

def controlla(username):
	while True:
		buy_inputs    = ['buy','b']
		sell_inputs   = ['sell','s']
		lookup_inputs = ['lookup','l']
		quote_inputs  = ['quote','q']
		performance   = ['performance','p']
		holdings      = ['holdings','h']
		exit_inputs   = ['exit','e']
		allowed_inputs = buy_inputs + sell_inputs\
						 + lookup_inputs + quote_inputs\
						 + performance + holdings + exit_inputs
		user_input = view.main_menu_UI().lower()
		if user_input in allowed_inputs:
			if user_input in buy_inputs:
				ticker_symbol,trade_volume = view.buy_UI()
				order_status = model.buy(ticker_symbol,trade_volume,username)
				print(order_status)
				input("\nPress Enter to continue...")
			elif user_input in sell_inputs:
				ticker_symbol,trade_volume = view.sell_UI()
				order_status = model.sell(ticker_symbol,trade_volume,username)
				print(order_status)
				input("\nPress Enter to continue...")
			elif user_input in lookup_inputs:
				company_name = view.lookup_UI()
				ticker_symbol = wrapper.get_ticker_symbol(company_name)
				print(ticker_symbol)
				input("\nPress Enter to continue...")
			elif user_input in quote_inputs:
				ticker_symbol = view.quote_UI()
				last_price = wrapper.get_last_price(ticker_symbol)
				print(last_price)
				input("\nPress Enter to continue...")
			elif user_input in performance:
				view.performance_UI()
				perf = model.portfolio_performance(username)
				print(perf)
				input("\nPress Enter to continue...")
			elif user_input in holdings:
				df  = model.holdings_performance(username)
				df2 = model.portfolio_performance(username)
				print(df2,'\n')
				print(df)
				input("\nPress Enter to continue...")
			elif user_input in exit_inputs:
				print('\nYou are about to exit!')
				input("\nPress Enter to continue...")
				return 'exit'
		else:
			print('\nNot A Command, Try Again!')

def admin_control():
	while True:
		users_list_inputs	= ['usrs','u']
		add_user_inputs		= ['add','a']
		del_user_inputs 	= ['del','d']
		leaderboard_inputs 	= ['leaders','l']
		exit_inputs   		= ['exit','e']

		allowed_inputs = users_list_inputs + add_user_inputs + del_user_inputs\
						 + leaderboard_inputs + exit_inputs

		user_input = view.admin_menu_UI()
		if user_input in allowed_inputs:
			if user_input in users_list_inputs:
				while True:
					print(view.admin_users_menu())
					print(model.admin_users_list())
					x = input("\nEnter Command:    ").lower()
					if x == 'h' or x == 'holdings':
						username = input('Enter Username:   ').lower()
						print('\n',model.holdings_performance(username))
						input("\nPress Enter to continue...")
					elif x == 'r' or x == 'return':
						break
					else:
						print('\nError! That is not a command!')
						input("\nPress Enter to continue...")
			elif user_input in add_user_inputs:
				username,password,balance,mrkt_val = view.create_user_UI()
				mapper.insert_account(username,password,balance,mrkt_val)
				print('Successful, User Added')
				input("\nPress Enter to continue...")
			elif user_input in del_user_inputs:
				while True:
					print(view.admin_del())
					x = input('\nEnter Command:   ')
					if x == 'd' or x == 'delete':
						print(model.admin_users_list())
						username = input('\nEnter Username:   ')
						attempt = mapper.delete_user(username)
						if attempt == 'Success':
							print('\nSuccessful, User Deleted')
							input("\nPress Enter to continue...")
						elif attempt == None:
							print('Cannot Find User! Try Again!')
							input("\nPress Enter to continue...")
					if x == 'r' or x == 'return':
						break
			elif user_input in leaderboard_inputs:
				print(model.leaderboard())
				input("\nPress Enter to continue...")
			elif user_input in exit_inputs:
				print('\nYou are about to exit!')
				input("\nPress Enter to continue...")
				return 'exit'
		else:
			print('\nNot A Command, Try Again!')

def tt_loop():
	while True:
		username = log_in()
		if username == None:
			print('\nError, Try Again!')
			input("\nPress Enter to continue...")
		elif 'exit' in username:
			break
		elif username != None:
			if username == 'admin':
				program = admin_control()
				if 'exit' in program:
					tt_loop()
					break
			else:
				program = controlla(username)
				if 'exit' in program:
					tt_loop()
					break


if __name__ == '__main__':
	print(tt_loop())
