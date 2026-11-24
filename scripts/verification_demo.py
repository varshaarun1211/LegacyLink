
from app import app
from models import db
from models.alumni import Alumni


with app.app_context():

    test_alumni = Alumni(
        full_name="Verification Test",
        department="Computer Science",
        degree="BTech",
        graduation_year=2023
    )

    try:
        # 1. Create a new alumni profile
        db.session.add(test_alumni)
        db.session.commit()

        print("Initial status:", test_alumni.verification_status)

        assert test_alumni.verification_status == "pending"

        # 2. Approve the profile
        test_alumni.verification_status = "approved"
        db.session.commit()

        approved = Alumni.query.filter_by(
            verification_status="approved",
            is_visible=True,
            is_public=True,
            full_name="Verification Test"
        ).first()

        assert approved is not None
        print("Approved profile found:", True)

        # 3. Reject the profile
        test_alumni.verification_status = "rejected"
        test_alumni.is_visible = False
        db.session.commit()

        rejected = Alumni.query.filter_by(
            verification_status="approved",
            is_visible=True,
            is_public=True,
            full_name="Verification Test"
        ).first()

        assert rejected is None
        print("Rejected profile hidden:", True)

        # 4. Test invalid verification status
        try:
            test_alumni.verification_status = "invalid"
            print("ERROR: Invalid status was accepted!")
        except ValueError:
            print("Invalid status rejected: True")

    finally:
        # 5. Clean up test record
        if test_alumni in db.session:
            db.session.delete(test_alumni)
            db.session.commit()
        else:
            db.session.rollback()

    print("Verification test completed!")
