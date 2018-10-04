import psycopg2
from urllib.parse import urlparse
from flask import current_app as app

class DbController:
	
	def __init__(self):
		connection_credentials = """
				dbname='walimike' user='postgres' password='1234'
	            host='localhost' port='5432'
				"""
		try:
			self.connection = psycopg2.connect(connection_credentials)
			self.connection.autocommit = True
			self.cursor = self.connection.cursor()

		except Exception as e:
			print(e)
			print('Failed to connect to db')


	def create_tables(self):

		""" Create all database tables"""

		create_table = "CREATE TABLE IF NOT EXISTS users \
			( user_id SERIAL PRIMARY KEY, username VARCHAR(10),	password VARCHAR(100), role VARCHAR(10));"
		self.cursor.execute(create_table)

		create_table = "CREATE TABLE IF NOT EXISTS menu \
			( food_id SERIAL PRIMARY KEY, foodname VARCHAR(15), price INTEGER);"
		self.cursor.execute(create_table)

		create_table = "CREATE TABLE IF NOT EXISTS orders \
			( order_id SERIAL PRIMARY KEY, \
			user_id INTEGER REFERENCES users(user_id), \
			foodname VARCHAR(20), price VARCHAR(20), status VARCHAR(10), username VARCHAR(20));"
		self.cursor.execute(create_table)	

	def add_user(self,new_user):
		query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s);"
		self.cursor.execute(query, (new_user.name, new_user.password, new_user.role))
		
	def add_food_to_menu(self, foodname, price):
		query = "INSERT INTO menu (foodname, price) VALUES (%s, %s)"
		self.cursor.execute(query, (foodname, price))

	def get_orders(self):
		query = "SELECT row_to_json(row) FROM (SELECT * FROM orders) row;"
		self.cursor.execute(query)
		orders = self.cursor.fetchall()
		return orders

	def get_users(self):
		
		query = "SELECT row_to_json(row) FROM (SELECT * FROM users) row;"
		self.cursor.execute(query)
		users = self.cursor.fetchall()
		return users

	def get_menu(self):
		query = "SELECT row_to_json(row) FROM (SELECT * FROM menu) row; "
		self.cursor.execute(query)
		menu = self.cursor.fetchall()
		return menu

	def get_an_order(self, column, value):
		query = "SELECT * FROM orders WHERE {} = '{}';".format(column, value)
		self.cursor.execute(query)
		user = self.cursor.fetchone()
		return user

	def get_user(self, value):
		query = "SELECT row_to_json(row) FROM (SELECT username FROM users WHERE username = '%s') row;" % (value)
		self.cursor.execute(query)
		user = self.cursor.fetchone()
		return user

	def place_order(self, foodname,price,status,user):
		query = "INSERT INTO orders (foodname, price, status,username) VALUES (%s, %s, %s, %s)"
		self.cursor.execute(query, (foodname, price, status, user))

	def update_status(self, order_id, status):
		query = "UPDATE orders SET status = '{}' WHERE order_id = '{}';\
		".format(status, order_id)
		self.cursor.execute(query)

	def get_history_by_userid(self, username):
		query = "SELECT * FROM orders WHERE username = '{}';".format(username)
		self.cursor.execute(query)
		history = self.cursor.fetchall()
		return history

	#def get_user_role(self,name):
	#	query = "SELECT role FROM users WHERE username = '{}';".format(name)	
	#	self.cursor.execute(query)
	#	role = self.cursor.fetchone()
	#	return role

	def drop_tables(self):
		query = "DROP TABLE IF EXISTS orders;DROP TABLE IF EXISTS menu;DROP TABLE IF EXISTS users; "
		self.cursor.execute(query)
		return "Droped"