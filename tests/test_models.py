
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from models import db
from models.user import User
from models.alumni import Alumni


@pytest.fixture
def session(tmp_path):
    test_db = tmp_path / "test_legacy_link.db"
    engine = create_engine(f"sqlite:///{test_db.as_posix()}")

    db.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    test_session = TestSession()

    try:
        yield test_session
    finally:
        test_session.close()
        db.metadata.drop_all(engine)
        engine.dispose()


def test_user_email_must_be_unique(session):
    email = f"{uuid.uuid4().hex}@example.com"

    first = User(email=email, role="alumni")
    first.set_password("test-password")
    session.add(first)
    session.commit()

    second = User(email=email, role="alumni")
    second.set_password("another-password")
    session.add(second)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()


def test_alumni_required_fields():
    with pytest.raises(ValueError, match="full_name cannot be empty"):
        Alumni(
            full_name="",
            department="Computer Science",
            degree="BTech",
            graduation_year=2024
        )


def test_invalid_graduation_year():
    with pytest.raises(ValueError, match="Invalid graduation year"):
        Alumni(
            full_name="Test Person",
            department="Computer Science",
            degree="BTech",
            graduation_year=1800
        )


def test_verification_status_validation():
    with pytest.raises(ValueError, match="Invalid verification status"):
        Alumni(
            full_name="Test Person",
            department="Computer Science",
            degree="BTech",
            graduation_year=2024,
            verification_status="unknown"
        )


def test_alumni_rejects_nonexistent_user_id(tmp_path):
    test_db = tmp_path / "test_foreign_keys.db"
    engine = create_engine(f"sqlite:///{test_db.as_posix()}")

    db.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    session = TestSession()

    try:
        alumni = Alumni(
            user_id=999999,
            full_name="Foreign Key Test",
            department="Computer Science",
            degree="BTech",
            graduation_year=2024
        )

        session.add(alumni)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

    finally:
        session.close()
        db.metadata.drop_all(engine)
        engine.dispose()
