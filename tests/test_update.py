
from app import app
from models import db
from models.alumni import Alumni

with app.app_context():

    # Find Arun's alumni profile
    alumni = Alumni.query.filter_by(
        full_name="Arun Kumar"
    ).first()

    if alumni:

        # Update profile information
        alumni.occupation = "Senior Software Developer"
        alumni.company = "ABC Technologies"

        # Save changes
        db.session.commit()

        print("Alumni profile updated successfully!")

        # Verify updated information
        updated_alumni = Alumni.query.filter_by(
            full_name="Arun Kumar"
        ).first()

        print("Name:", updated_alumni.full_name)
        print("Occupation:", updated_alumni.occupation)
        print("Company:", updated_alumni.company)

    else:
        print("Alumni record not found.")
