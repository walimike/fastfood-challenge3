from api import app, db
from api.models.dbcontroller import DbController
from api.models.models import User
from api.config import app_config

if __name__ == '__main__':
    #app.config.from_object(app_config(config_name))
    db.drop_tables()
    db.create_tables()
    admin_user = User('superman', 'Sup3rM@n', 'admin')
    db.add_user(admin_user)
    app.run(debug = True)