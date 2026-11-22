
from app import app
from models import db
from models.user import User
from models.alumni import Alumni
from models.mentorship import Mentorship
from sqlalchemy import func, text


with app.app_context():

    database_path = db.engine.url.database

    print("\n===== DATABASE INTEGRITY CHECK =====")
    print(f"Database: {database_path}")

    # 1. Check that required tables exist
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()

    required_tables = {"users", "alumni", "mentorships"}

    print("\nRequired tables:")
    for table in sorted(required_tables):
        print(f"{table}: {'Found' if table in tables else 'MISSING'}")

    if not required_tables.issubset(tables):
        raise RuntimeError(
            "Required tables are missing. Check the database configuration."
        )

    # 2. Check duplicate alumni
    duplicates = (
        db.session.query(
            Alumni.full_name,
            Alumni.department,
            Alumni.graduation_year,
            func.count(Alumni.id)
        )
        .group_by(
            Alumni.full_name,
            Alumni.department,
            Alumni.graduation_year
        )
        .having(func.count(Alumni.id) > 1)
        .all()
    )

    print("\n1. Duplicate alumni:")
    print(duplicates if duplicates else "None found!")

    # 3. Check duplicate user emails
    duplicate_emails = (
        db.session.query(
            User.email,
            func.count(User.id)
        )
        .group_by(User.email)
        .having(func.count(User.id) > 1)
        .all()
    )

    print("\n2. Duplicate user emails:")
    print(duplicate_emails if duplicate_emails else "None found!")

    # 4. Check foreign-key integrity
    violations = db.session.execute(
        text("PRAGMA foreign_key_check")
    ).fetchall()

    print("\n3. Foreign-key violations:")
    print(violations if violations else "None found!")

    # 5. Check orphaned alumni
    orphaned = []

    for alumni in Alumni.query.filter(
        Alumni.user_id.isnot(None)
    ).all():

        if db.session.get(User, alumni.user_id) is None:
            orphaned.append(alumni.full_name)

    print("\n4. Orphaned alumni:")
    print(orphaned if orphaned else "None found!")

    # 6. Check invalid mentorship references
    invalid_mentorships = []

    for request in Mentorship.query.all():
        mentor_exists = db.session.get(Alumni, request.mentor_id)
        mentee_exists = db.session.get(Alumni, request.mentee_id)

        if mentor_exists is None or mentee_exists is None:
            invalid_mentorships.append(request.id)

    print("\n5. Invalid mentorship references:")
    print(
        invalid_mentorships
        if invalid_mentorships
        else "None found!"
    )

    # 7. Check mentorship requests where mentor and mentee are identical
    self_requests = Mentorship.query.filter(
        Mentorship.mentor_id == Mentorship.mentee_id
    ).all()

    print("\n6. Mentorship self-requests:")
    print(
        [request.id for request in self_requests]
        if self_requests
        else "None found!"
    )

    print("\n===== CHECK COMPLETED =====")
