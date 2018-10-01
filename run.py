from api.views.auth import app
from api.models.dbcontroller import DbController

if __name__ == '__main__':
    DbController().create_tables()
    app.run()