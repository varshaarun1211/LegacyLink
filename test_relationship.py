
from app import app
from models import db
from models.user import User

with app.app_context():

    user = User.query.filter_by(
        email="arun.test@example.com"
    ).first()

    if user:
        print("User:", user.email)

        if user.alumni_profile:
            print("Alumni:", user.alumni_profile.full_name)
            print("Department:", user.alumni_profile.department)
        else:
            print("No alumni profile found.")

    else:
        print("Test user not found.")
