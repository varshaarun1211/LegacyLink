
import csv

from app import app
from models import db
from models.alumni import Alumni


with app.app_context():

    imported_count = 0
    skipped_count = 0

    with open("sample_alumni.csv", "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        required_fields = [
            "full_name",
            "department",
            "degree",
            "graduation_year"
        ]

        for row_number, row in enumerate(reader, start=2):

            # Check for missing required fields
            if any(
                not row.get(field) or not row[field].strip()
                for field in required_fields
            ):
                print(f"Row {row_number}: Missing required information. Skipped.")
                skipped_count += 1
                continue

            # Validate graduation year
            try:
                graduation_year = int(row["graduation_year"].strip())
            except ValueError:
                print(f"Row {row_number}: Invalid graduation year. Skipped.")
                skipped_count += 1
                continue

            if graduation_year < 1950 or graduation_year > 2026:
                print(f"Row {row_number}: Graduation year out of range. Skipped.")
                skipped_count += 1
                continue

            full_name = row["full_name"].strip()
            department = row["department"].strip()

            # Check for duplicate records
            existing_alumni = Alumni.query.filter_by(
                full_name=full_name,
                department=department,
                graduation_year=graduation_year
            ).first()

            if existing_alumni:
                print(f"Row {row_number}: Duplicate record for {full_name}. Skipped.")
                skipped_count += 1
                continue

            # Create alumni record
            alumni = Alumni(
                full_name=full_name,
                department=department,
                degree=row["degree"].strip(),
                graduation_year=graduation_year,
                occupation=(row.get("occupation") or "").strip(),
                company=(row.get("company") or "").strip(),
                skills=(row.get("skills") or "").strip(),
                bio=(row.get("bio") or "").strip(),
                verification_status="pending",
                is_visible=False
            )

            db.session.add(alumni)
            imported_count += 1

        db.session.commit()

    print("\n===== IMPORT SUMMARY =====")
    print(f"Successfully imported: {imported_count}")
    print(f"Skipped rows: {skipped_count}")
