
import os
from flask import Flask, render_template
from flask_migrate import Migrate
from models import db
from models.user import User
from models.alumni import Alumni

app = Flask(__name__, instance_relative_config=True)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///legacylink.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Initialize migrations with explicit model metadata
migrate = Migrate(app, db, compare_type=True)

# Home route
@app.route("/")
def home():
    return render_template("index.html")


# Create tables if they do not exist
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
