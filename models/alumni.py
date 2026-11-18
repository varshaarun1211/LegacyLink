
from datetime import datetime
from models import db
from sqlalchemy.orm import validates


class Alumni(db.Model):
    __tablename__ = "alumni"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=True
    )

    full_name = db.Column(db.String(120), nullable=False)

    department = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    degree = db.Column(db.String(100), nullable=False)

    graduation_year = db.Column(
        db.Integer,
        nullable=False,
        index=True
    )

    occupation = db.Column(db.String(120), nullable=True)
    company = db.Column(db.String(120), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    bio = db.Column(db.Text, nullable=True)

    verification_status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    is_visible = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    verified_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    verified_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    @validates("graduation_year")
    def validate_graduation_year(self, key, year):
        if not isinstance(year, int) or isinstance(year, bool):
            raise ValueError("Graduation year must be a number.")

        if year < 1950 or year > datetime.now().year:
            raise ValueError("Invalid graduation year.")

        return year

    @validates("full_name", "department", "degree")
    def validate_required_fields(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} cannot be empty.")
        return value.strip()

    @validates("verification_status")
    def validate_verification_status(self, key, status):
        allowed_statuses = ["pending", "approved", "rejected"]
        if status not in allowed_statuses:
            raise ValueError("Invalid verification status.")
        return status

    def __repr__(self):
        return f"<Alumni {self.full_name}>"
