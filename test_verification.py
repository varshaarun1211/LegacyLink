
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

    db.session.add(test_alumni)
    db.session.commit()

    print("Initial status:", test_alumni.verification_status)

    # Approve the profile
    test_alumni.verification_status = "approved"
    test_alumni.is_visible = True
    db.session.commit()

    approved = Alumni.query.filter_by(
        verification_status="approved",
        is_visible=True
    ).filter_by(full_name="Verification Test").first()

    print("Approved and visible:", approved is not None)

    # Reject the profile
    test_alumni.verification_status = "rejected"
    test_alumni.is_visible = False
    db.session.commit()

    rejected = Alumni.query.filter_by(
        verification_status="approved",
        is_visible=True,
        full_name="Verification Test"
    ).first()

    print("Rejected profile hidden:", rejected is None)

    # Clean up test record
    db.session.delete(test_alumni)
    db.session.commit()

    print("Verification test completed!")
