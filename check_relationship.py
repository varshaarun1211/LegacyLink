
from app import app
from models.user import User
from models.alumni import Alumni

with app.app_context():

    alumni_records = Alumni.query.all()

    for alumni in alumni_records:
        print("\nAlumni:", alumni.full_name)

        if alumni.user_id is not None:
            print("Linked User ID:", alumni.user_id)
            print("User Email:", alumni.user.email)
        else:
            print("No user account linked (imported or standalone profile)")
