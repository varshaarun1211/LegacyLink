
import pytest

from app import app
from models import db, Alumni, Mentorship


@pytest.fixture
def database():
    with app.app_context():
        db.create_all()

        yield

        db.session.rollback()

        # Remove test records created by these tests.
        db.session.query(Mentorship).delete()
        db.session.query(Alumni).filter(
            Alumni.full_name.in_(["Mentor One", "Mentee One", "Alumni One"])
        ).delete(synchronize_session=False)

        db.session.commit()


def create_alumni(name):
    alumni = Alumni(
        full_name=name,
        department="Computer Science",
        degree="B.Tech",
        graduation_year=2022
    )
    db.session.add(alumni)
    db.session.commit()
    return alumni


def test_mentorship_request_creation(database):
    mentor = create_alumni("Mentor One")
    mentee = create_alumni("Mentee One")

    request = Mentorship(
        mentor_id=mentor.id,
        mentee_id=mentee.id,
        message="I would like career guidance."
    )

    db.session.add(request)
    db.session.commit()

    assert request.status == "pending"
    assert request.mentor.id == mentor.id
    assert request.mentee.id == mentee.id


def test_invalid_mentorship_status(database):
    request = Mentorship(
        mentor_id=1,
        mentee_id=2
    )

    with pytest.raises(ValueError):
        request.status = "invalid"


def test_mentorship_cannot_be_self_requested(database):
    alumni = create_alumni("Alumni One")

    request = Mentorship(
        mentor_id=alumni.id,
        mentee_id=alumni.id
    )

    db.session.add(request)

    with pytest.raises(Exception):
        db.session.commit()

    db.session.rollback()
