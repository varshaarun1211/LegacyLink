

from app import app
from models import db
from models.user import User
from models.alumni import Alumni
from werkzeug.security import generate_password_hash

with app.app_context():

    # Create a fictional test user
    user = User.query.filter_by(
        email="arun.test@example.com"
    ).first()

    if not user:
        user = User(
            email="arun.test@example.com",
            password_hash=generate_password_hash("demo-password"),
            role="alumni"
        )
        db.session.add(user)
        db.session.flush()

    # Create a fictional approved alumni profile
    profile = Alumni.query.filter_by(user_id=user.id).first()

    if not profile:
        profile = Alumni(
            user_id=user.id,
            full_name="Arun Kumar",
            department="Computer Science",
            degree="BTech Computer Science",
            graduation_year=2024,
            occupation="Software Developer",
            company="Example Technologies",
            verification_status="approved",
            is_visible=True
        )
        db.session.add(profile)

    # Create a fictional pending alumni profile
    pending_profile = Alumni(
        full_name="Priya Sharma",
        department="Information Technology",
        degree="BTech Information Technology",
        graduation_year=2023,
        verification_status="pending",
        is_visible=False
    )

    db.session.add(pending_profile)

    # Save records
    db.session.commit()

    print("Sample alumni records saved successfully!")

    # Retrieve and display alumni records
    alumni_list = Alumni.query.all()

    print("\n--- Alumni Records ---")

    for alumni in alumni_list:
        print(
            alumni.full_name,
            alumni.department,
            alumni.graduation_year
        )

    # Verification test
    print("\n--- Database Verification Test ---")

    pending_count = Alumni.query.filter_by(
        verification_status="pending"
    ).count()

    approved_count = Alumni.query.filter_by(
        verification_status="approved"
    ).count()

    print("Pending alumni:", pending_count)
    print("Approved alumni:", approved_count)
