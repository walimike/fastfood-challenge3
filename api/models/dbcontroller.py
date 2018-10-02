import psycopg2
from pprint import pprint


class DbController:
    """
    Class initiates connection to Data Base.
    """
    def __init__(self):
        try:
            self.connection = pscycop2.connect(user = "postgres",
                                    password = "1234",
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = "walimike")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint("Can not connect to database")

    def create_tables(self):
        """Method creates tables."""
        user_table = "CREATE TABLE IF NOT EXISTS user_table(usrId serial PRIMARY KEY,\
          username varchar(50), password varchar(20), role varchar(15))"
        orders_table = "CREATE TABLE IF NOT EXISTS orders_table(orderId serial PRIMARY KEY,\
          item varchar(100), price integer, order_status varchar(20), client varchar(50))"
        menu_table = "CREATE TABLE IF NOT EXISTS menu_table(menuid serial PRIMARY KEY,\
         item varchar(100),  price integer)"
        self.cursor.execute(user_table)
        self.cursor.execute(orders_table)
        self.cursor.execute(menu_table)

    def drop_tables(self):
        """Method drops tables."""
        drop_user_table = "DROP TABLE users cascade"
        drop_orders_table = "DROP TABLE orders cascade"
        drop_menu_table = "DROP TABLE menu cascade"
        self.cursor.execute(drop_user_table)
        self.cursor.execute(drop_orders_table)
        self.cursor.execute(drop_menu_table)

    def add_user(self,user):
        username, password,role = user.name, user.password, user.role
        add_user=("INSERT INTO user_table VALUES (%s, %s, %s, %s)", (1,"username","password","role"))
        self.cursor.execute(add_user))

    def add_order(self,order):
        orderid, ordername, price = 1, order.name, order.price
        add_order=("INSERT INTO orders_table VALUES (%s, %s, %s)", ("orderid","ordername","price"))
        self.cursor.execute(add_user))

    def add_to_menu(self,food_item):
        foodid, food, price = 1, food_item.name, food_item.price
        add_user=("INSERT INTO user_table VALUES (%s, %s, %s, %s)", (1,"username","password","role"))
        self.cursor.execute(add_user))

    def get_element_by_id(self, id, table):
        self.cursor.execute("SELECT * from (%s)",("table")
        data = self.cursor.fetchone(table)
        return data
