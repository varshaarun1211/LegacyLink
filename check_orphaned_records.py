
from app import app
from models import db
from models.alumni import Alumni
from models.user import User

with app.app_context():

    records = Alumni.query.filter(
        Alumni.user_id.isnot(None)
    ).all()

    orphaned = []

    for alumni in records:
        user = db.session.get(User, alumni.user_id)

        if user is None:
            orphaned.append(alumni.full_name)

    if orphaned:
        print("Orphaned records found:", orphaned)
    else:
        print("No orphaned alumni records found!")
