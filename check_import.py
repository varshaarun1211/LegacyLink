from app import app
from models import db
from models.alumni import Alumni

with app.app_context():

    records = Alumni.query.all()

    for alumni in records:
        print(
            alumni.full_name,
            alumni.department,
            alumni.graduation_year,
            alumni.verification_status,
            alumni.is_visible
        )