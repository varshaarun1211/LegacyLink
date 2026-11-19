
from flask_migrate import Migrate

from alumniMaincode import app
from models import db


# Enable database migrations
migrate = Migrate(app, db, compare_type=True)


# Run the complete LegacyLink application
if __name__ == "__main__":
    app.run(debug=True)
