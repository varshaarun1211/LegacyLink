
import os
from flask import Flask, render_template
from models import db

# Import models so SQLAlchemy recognises both tables
from models.user import User
from models.alumni import Alumni

app = Flask(__name__, instance_relative_config=True)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///legacylink.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect SQLAlchemy to Flask
db.init_app(app)


# Home route
@app.route("/")
def home():
    return render_template("index.html")


# Create database tables
with app.app_context():
    db.create_all()


# Run application
if __name__ == "__main__":
    app.run(debug=True)
