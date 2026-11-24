from app import app
from models import db
from models.user import User
from sqlalchemy.exc import IntegrityError

with app.app_context():

    duplicate_user = User(
        email="arun.test@example.com",
        password_hash="dummy-hash",
        role="alumni"
    )

    db.session.add(duplicate_user)

    try:
        db.session.commit()
        print("ERROR: Duplicate email was accepted!")

    except IntegrityError:
        db.session.rollback()
        print("SUCCESS: Duplicate email was rejected!")