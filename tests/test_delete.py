
from app import app
from models import db
from models.alumni import Alumni

with app.app_context():

    # Create a disposable test record if it doesn't exist
    test_alumni = Alumni.query.filter_by(
        full_name="Delete Test Record"
    ).first()

    if not test_alumni:
        test_alumni = Alumni(
            full_name="Delete Test Record",
            department="Computer Science",
            degree="BTech Computer Science",
            graduation_year=2022,
            verification_status="pending",
            is_visible=False
        )

        db.session.add(test_alumni)
        db.session.commit()

    print("Test record created/found.")

    # Retrieve the record
    test_alumni = Alumni.query.filter_by(
        full_name="Delete Test Record"
    ).first()

    # Delete the record
    db.session.delete(test_alumni)
    db.session.commit()

    # Verify deletion
    remaining_record = Alumni.query.filter_by(
        full_name="Delete Test Record"
    ).first()

    if remaining_record is None:
        print("SUCCESS: Test record deleted!")
    else:
        print("ERROR: Test record still exists.")
