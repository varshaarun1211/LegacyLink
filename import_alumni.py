
import csv

from app import app
from models import db
from models.alumni import Alumni


with app.app_context():

    with open("sample_alumni.csv", "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        imported_count = 0
        skipped_count = 0

        for row in reader:

            full_name = row["full_name"].strip()
            department = row["department"].strip()
            graduation_year = int(row["graduation_year"])

            existing_alumni = Alumni.query.filter_by(
                full_name=full_name,
                department=department,
                graduation_year=graduation_year
            ).first()

            if existing_alumni:
                print(f"Skipping duplicate: {full_name}")
                skipped_count += 1
                continue

            alumni = Alumni(
                full_name=full_name,
                department=department,
                degree=row["degree"].strip(),
                graduation_year=graduation_year,
                occupation=row["occupation"].strip(),
                company=row["company"].strip(),
                skills=row["skills"].strip(),
                bio=row["bio"].strip(),
                verification_status="pending",
                is_visible=False
            )

            db.session.add(alumni)
            imported_count += 1

        db.session.commit()

        print(f"Successfully imported: {imported_count}")
        print(f"Skipped duplicates: {skipped_count}")
