import psycopg2

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
			user_id INTEGER NOT NULL REFERENCES users(user_id), \
			food_id INTEGER NOT NULL REFERENCES menu(food_id), \
			quantity INTEGER, status VARCHAR(10));"
		self.cursor.execute(create_table)	


	def add_user(self,new_user):
		query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s);"
		self.cursor.execute(query, (new_user.name, new_user.password, new_user.role))

	def add_food_to_menu(self, foodname, price):
		query = "INSERT INTO menu (foodname, price) VALUES ('{}', '{}');"\
			.format(foodname, price)
		self.cursor.execute(query)

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
		query = "SELECT row_to_json(row) FROM (SELECT * FROM ) row; "
		self.cursor.execute(query)
		menu = self.cursor.fetchall()
		return menu

	def get_an_order(self, column, value):
		query = "SELECT * FROM orders WHERE {} = '{}';".format(column, value)
		self.cursor.execute(query)
		user = self.cursor.fetchone()
		return user

	def get_user(self, column, value):
		query = "SELECT  row_to_json (row) FROM (users WHERE {} = '{}') row;".format(column, value)
		self.cursor.execute(query)
		user = self.cursor.fetchone()
		return user

	def place_order(self, user_id, food_id, quantity):
		query = "INSERT INTO orders (user_id, food_id, quantity, status) \
			VALUES ('{}', '{}', '{}', 'pending');".format(user_id, food_id, quantity)
		self.cursor.execute(query)

	def update_status(self, order_id, status):
		query = "UPDATE orders SET status = '{}' WHERE order_id = '{}';\
		".format(status, order_id)
		self.cursor.execute(query)

	def get_history_by_userid(self, userid):
		query = "SELECT * FROM orders WHERE user_id = '{}';".format(userid)
		self.cursor.execute(query)
		history = self.cursor.fetchall()
		return history
		
	def drop_tables(self):
		query = "DROP TABLE orders;DROP TABLE menu;DROP TABLE users; "
		self.cursor.execute(query)
		return "Droped"

#DbController().add_user('wali','123456789','admin')