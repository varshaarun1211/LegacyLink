
from datetime import datetime
from models import db


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

    department = db.Column(db.String(100), nullable=False)

    degree = db.Column(db.String(100), nullable=False)

    graduation_year = db.Column(db.Integer, nullable=False)

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

    def __repr__(self):
        return f"<Alumni {self.full_name}>"
