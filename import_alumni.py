
import csv
from pathlib import Path
from datetime import datetime

from app import app
from models import db
from models.alumni import Alumni


CSV_FILE = Path(__file__).resolve().parent / "sample_alumni.csv"

with app.app_context():

    imported_count = 0
    skipped_count = 0

    required_fields = [
        "full_name",
        "department",
        "degree",
        "graduation_year"
    ]

    with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames or not all(
            field in reader.fieldnames for field in required_fields
        ):
            raise ValueError("CSV is missing one or more required columns.")

        for row_number, row in enumerate(reader, start=2):

            # Check required fields
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

            if graduation_year < 1950 or graduation_year > datetime.now().year:
                print(f"Row {row_number}: Graduation year out of range. Skipped.")
                skipped_count += 1
                continue

            full_name = row["full_name"].strip()
            department = row["department"].strip()

            # Check for existing records
            existing_alumni = Alumni.query.filter_by(
                full_name=full_name,
                department=department,
                graduation_year=graduation_year
            ).first()

            if existing_alumni:
                print(f"Row {row_number}: Duplicate record for {full_name}. Skipped.")
                skipped_count += 1
                continue

            # Create alumni profile
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

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    print("\n===== IMPORT SUMMARY =====")
    print(f"Successfully imported: {imported_count}")
    print(f"Skipped rows: {skipped_count}")
