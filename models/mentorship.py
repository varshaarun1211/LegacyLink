
from datetime import datetime, timezone

from sqlalchemy.orm import validates

from models import db


class Mentorship(db.Model):

    __tablename__ = "mentorships"

    id = db.Column(db.Integer, primary_key=True)

    mentor_id = db.Column(
        db.Integer,
        db.ForeignKey("alumni.id"),
        nullable=False,
        index=True
    )

    mentee_id = db.Column(
        db.Integer,
        db.ForeignKey("alumni.id"),
        nullable=False,
        index=True
    )

    message = db.Column(db.Text, nullable=True)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    requested_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    mentor = db.relationship(
        "Alumni",
        foreign_keys=[mentor_id],
        backref="mentorship_requests_received"
    )

    mentee = db.relationship(
        "Alumni",
        foreign_keys=[mentee_id],
        backref="mentorship_requests_sent"
    )

    __table_args__ = (
        db.CheckConstraint(
            "mentor_id != mentee_id",
            name="check_different_mentor_and_mentee"
        ),
    )

    @validates("status")
    def validate_status(self, key, status):
        allowed_statuses = ["pending", "accepted", "rejected"]

        if status not in allowed_statuses:
            raise ValueError("Invalid mentorship status.")

        return status

    def __repr__(self):
        return (
            f"<Mentorship mentor={self.mentor_id} "
            f"mentee={self.mentee_id} status={self.status}>"
        )
