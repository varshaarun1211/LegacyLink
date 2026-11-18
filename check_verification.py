
from app import app
from models.alumni import Alumni

with app.app_context():

    records = Alumni.query.all()

    for alumni in records:
        print("\nName:", alumni.full_name)
        print("Status:", alumni.verification_status)
        print("Visible:", alumni.is_visible)

        if alumni.verification_status == "pending" and alumni.is_visible:
            print("WARNING: Pending profile is visible!")

        elif alumni.verification_status == "rejected" and alumni.is_visible:
            print("WARNING: Rejected profile is visible!")

        elif alumni.verification_status == "approved" and alumni.is_visible:
            print("OK: Approved profile is visible.")

        else:
            print("OK: Visibility is consistent with its status.")
