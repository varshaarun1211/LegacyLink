
from datetime import datetime
from models import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(256),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="alumni"
    )

    email_verified = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<User {self.email}>"
    alumni_profile = db.relationship(
    "Alumni",
    foreign_keys="Alumni.user_id",
    backref="user",
    uselist=False
)