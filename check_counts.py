from app import app
from models.user import User
from models.alumni import Alumni

with app.app_context():

    print("Users:", User.query.count())

    print("Alumni:", Alumni.query.count())