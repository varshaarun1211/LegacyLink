
from app import app
from models.alumni import Alumni

with app.app_context():

    alumni = Alumni.query.filter_by(
        full_name="Arun Kumar"
    ).first()

    if alumni:
        print("Name:", alumni.full_name)
        print("Occupation:", alumni.occupation)
        print("Company:", alumni.company)
    else:
        print("Alumni record not found.")
