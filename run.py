from api import app
from api import db
from api.models.models import User

if __name__ == '__main__':
    db.drop_tables()
    db.create_tables()
    admin_user = User('superman', 'Sup3rM@n', 'admin')
    db.add_user(admin_user)
    app.run(debug=True)