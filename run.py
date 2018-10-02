from api import app
from api.models.dbcontroller import DbController

if __name__ == '__main__':
    DbController().drop_tables()
    DbController().create_tables()
    app.run()