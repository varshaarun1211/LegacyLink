
from datetime import datetime, timezone

from models import db


class Opportunity(db.Model):

    __tablename__ = "opportunities"

    id = db.Column(db.Integer, primary_key=True)

    alumni_id = db.Column(
        db.Integer,
        db.ForeignKey("alumni.id"),
        nullable=False
    )

    title = db.Column(db.String(150), nullable=False)

    company = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text, nullable=False)

    opportunity_type = db.Column(
        db.String(50),
        nullable=False
    )

    location = db.Column(
        db.String(150),
        nullable=True
    )

    application_link = db.Column(
        db.String(500),
        nullable=True
    )

    deadline = db.Column(
        db.Date,
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    alumni = db.relationship(
        "Alumni",
        backref=db.backref("opportunities", lazy=True)
    )

    def __repr__(self):
        return f"<Opportunity {self.title}>"
