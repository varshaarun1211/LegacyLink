
from datetime import datetime

from sqlalchemy.orm import validates

from models import db


class Alumni(db.Model):

    __tablename__ = "alumni"

    id = db.Column(db.Integer, primary_key=True)

    # Link to the user's login account
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=True
    )

    # Basic identity information
    full_name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(120), nullable=False, index=True)
    degree = db.Column(db.String(120), nullable=False)

    graduation_year = db.Column(
        db.Integer,
        nullable=False,
        index=True
    )

    # Employment and additional information
    occupation = db.Column(db.String(150), nullable=True)
    company = db.Column(db.String(150), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    bio = db.Column(db.Text, nullable=True)

    # Alumni verification
    verification_status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    verified_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    verified_at = db.Column(db.DateTime, nullable=True)

    # Profile visibility settings
    is_visible = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    is_public = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # Record creation and modification times
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Connect the alumni profile to its account
    user = db.relationship(
        "User",
        back_populates="alumni",
        foreign_keys=[user_id]
    )

    # Connect the profile to the administrator who verified it
    verifier = db.relationship(
        "User",
        foreign_keys=[verified_by]
    )

    # Validate graduation year
    @validates("graduation_year")
    def validate_graduation_year(self, key, year):

        if not isinstance(year, int) or isinstance(year, bool):
            raise ValueError("Graduation year must be a number.")

        if year < 1900 or year > datetime.now().year:
            raise ValueError("Invalid graduation year.")

        return year

    # Validate required text fields
    @validates("full_name", "department", "degree")
    def validate_required_fields(self, key, value):

        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} cannot be empty.")

        return value.strip()

    # Validate verification status
    @validates("verification_status")
    def validate_verification_status(self, key, status):

        allowed_statuses = ["pending", "approved", "rejected"]

        if status not in allowed_statuses:
            raise ValueError("Invalid verification status.")

        return status

    def __repr__(self):
        return f"<Alumni {self.full_name}>"
