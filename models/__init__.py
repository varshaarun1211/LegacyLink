
from datetime import datetime, timezone
import sqlite3

from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy

# Create the database object
db = SQLAlchemy()


# Return the current UTC time
def utcnow():
    return datetime.now(timezone.utc)


# Enable foreign-key enforcement for SQLite connections
@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(connection, connection_record):
    if isinstance(connection, sqlite3.Connection):
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# Import models so they are available from the models package
from .user import User
from .alumni import Alumni
