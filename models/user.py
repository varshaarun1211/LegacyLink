
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from models import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(255),
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
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # Connects a user account to one alumni profile
    alumni = db.relationship(
        "Alumni",
        back_populates="user",
        foreign_keys="Alumni.user_id",
        uselist=False
    )

    # Hash and store the password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check an entered password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Check whether this account is an administrator
    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f"<User {self.email}>"
