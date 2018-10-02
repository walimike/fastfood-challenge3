from api.views import app
from api.models.dbcontroller import DbController

if __name__ == '__main__':
    DbController().create_tables()
    app.run()