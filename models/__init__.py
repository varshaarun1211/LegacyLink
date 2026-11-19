
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

# Create the database object
db = SQLAlchemy()


# Return the current UTC time
def utcnow():
    return datetime.utcnow()


# Import models so they are available from the models package
from .user import User
from .alumni import Alumni
