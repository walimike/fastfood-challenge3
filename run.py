from api import app
from api import db

if __name__ == '__main__':
    db.create_tables()
    app.run()