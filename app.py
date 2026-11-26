
from pathlib import Path

from flask_migrate import Migrate
from alumniMaincode import app
from models import db
from routes.opportunity_routes import opportunity_bp


# Use an explicit absolute path for the SQLite database.
instance_dir = Path(app.instance_path)
instance_dir.mkdir(parents=True, exist_ok=True)

database_path = instance_dir / "legacylink.db"

if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{database_path.as_posix()}"
    )


# Register the Career Opportunities blueprint.
app.register_blueprint(opportunity_bp)


# Initialize Flask-Migrate.
migrate = Migrate(app, db, compare_type=True)


if __name__ == "__main__":
    app.run(debug=True)
