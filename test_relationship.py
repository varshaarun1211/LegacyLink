
from app import app
from models import db
from models.user import User

with app.app_context():

    user = User.query.filter_by(
        email="arun.test@example.com"
    ).first()

    if user:
        print("User:", user.email)

        if user.alumni:
            print("Alumni:", user.alumni.full_name)
            print("Department:", user.alumni.department)
        else:
            print("No alumni profile found.")

    else:
        print("Test user not found.")
