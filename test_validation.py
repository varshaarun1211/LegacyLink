
from app import app
from models.alumni import Alumni

with app.app_context():

    try:
        alumni = Alumni(
            full_name="Validation Test",
            department="Computer Science",
            degree="BTech",
            graduation_year=2040
        )

        print("ERROR: Invalid year was accepted!")

    except ValueError as error:
        print("SUCCESS:", error)
