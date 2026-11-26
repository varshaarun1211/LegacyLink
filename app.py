
import os
import re
from datetime import datetime
from functools import wraps
from urllib.parse import urlparse
from flask_migrate import Migrate

import click
from flask import (
    Flask, abort, flash, redirect, render_template, request, url_for
)
from flask_login import (
    LoginManager, current_user, login_required, login_user, logout_user
)
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Alumni, Mentorship, User, db, utcnow
from routes.opportunity_routes import opportunity_bp


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PER_PAGE = 12

login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL", "sqlite:///legacylink.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("FLASK_ENV") == "production",
    )

    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    register_routes(app)
    register_cli(app)
    return app


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def admin_required(view):
    """Backend permission check: never rely on hidden buttons."""

    @wraps(view)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapper


def is_safe_next(target):
    if not target:
        return False
    parsed = urlparse(target)
    return not parsed.netloc and not parsed.scheme and target.startswith("/")


def clean(value, max_len=None):
    value = (value or "").strip()
    return value[:max_len] if max_len else value


def validate_profile_fields(form):
    """Returns (data, errors) for the shared profile fields."""
    errors = []

    data = {
        "full_name": clean(form.get("full_name"), 150),
        "department": clean(form.get("department"), 120),
        "degree": clean(form.get("degree"), 120),
        "occupation": clean(form.get("occupation"), 150) or None,
        "company": clean(form.get("company"), 150) or None,
        "skills": clean(form.get("skills"), 1000) or None,
        "bio": clean(form.get("bio"), 2000) or None,
        "github_url": clean(form.get("github_url"), 255) or None,
        "linkedin_url": clean(form.get("linkedin_url"), 255) or None,
    }

    for field in ("full_name", "department", "degree"):
        if not data[field]:
            errors.append(
                f"{field.replace('_', ' ').title()} is required."
            )

    for field in ("github_url", "linkedin_url"):
        value = data[field]

        if value:
            parsed = urlparse(value)

            if (
                parsed.scheme not in ("http", "https")
                or not parsed.netloc
            ):
                errors.append(
                    f"Enter a valid HTTP or HTTPS "
                    f"{field.replace('_url', '')} URL."
                )

    try:
        year = int(form.get("graduation_year", ""))
        if not 1900 <= year <= datetime.now().year:
            raise ValueError
        data["graduation_year"] = year
    except ValueError:
        errors.append("Enter a valid graduation year.")

    return data, errors


def register_routes(app):

    # Register the opportunity feature routes.
    app.register_blueprint(opportunity_bp)

    @app.context_processor
    def inject_notification_counts():
        counts = {
            "admin_pending": 0,
            "mentorship_received": 0,
            "mentorship_updates": 0,
        }

        if not current_user.is_authenticated:
            return {"notification_counts": counts}

        if current_user.is_admin:
            counts["admin_pending"] = Alumni.query.filter_by(
                verification_status="pending"
            ).count()

        profile = current_user.alumni

        if profile is not None:
            counts["mentorship_received"] = Mentorship.query.filter_by(
                mentor_id=profile.id,
                status="pending"
            ).count()

            counts["mentorship_updates"] = Mentorship.query.filter(
                Mentorship.mentee_id == profile.id,
                Mentorship.status.in_(["accepted", "rejected"])
            ).count()

        return {"notification_counts": counts}

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():

        if current_user.is_authenticated:
            return redirect(url_for("alumni_directory"))

        if request.method == "GET":
            return render_template("register.html", form={})

        email = clean(request.form.get("email")).lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        data, errors = validate_profile_fields(request.form)

        if not EMAIL_RE.match(email) or len(email) > 255:
            errors.append("Enter a valid email address.")

        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")

        if password != confirm:
            errors.append("Passwords do not match.")

        if not errors and User.query.filter_by(email=email).first():
            errors.append("An account with this email already exists.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "register.html", form=request.form
            ), 400

        try:
            user = User(email=email, role="alumni")
            user.set_password(password)
            db.session.add(user)
            db.session.flush()

            profile = Alumni.query.filter(
                Alumni.user_id.is_(None),
                func.lower(Alumni.full_name) == data["full_name"].lower(),
                func.lower(Alumni.department) == data["department"].lower(),
                Alumni.graduation_year == data["graduation_year"],
            ).first()

            if profile:
                for k, v in data.items():
                    setattr(profile, k, v)
                profile.user_id = user.id
            else:
                profile = Alumni(user_id=user.id, **data)
                db.session.add(profile)

            profile.verification_status = "pending"
            profile.verified_by = None
            profile.verified_at = None

            db.session.commit()

        except (IntegrityError, ValueError):
            db.session.rollback()
            flash(
                "Could not complete registration. Please check your details.",
                "danger"
            )
            return render_template(
                "register.html", form=request.form
            ), 400

        flash(
            "Registration submitted. An administrator will verify your alumni status.",
            "success"
        )
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():

        if current_user.is_authenticated:
            return redirect(url_for("alumni_directory"))

        if request.method == "GET":
            return render_template("login.html")

        email = clean(request.form.get("email")).lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html"), 401

        login_user(user)
        nxt = request.args.get("next")

        return redirect(
            nxt if is_safe_next(nxt) else url_for("alumni_directory")
        )

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("login"))

    @app.route("/alumni")
    @login_required
    def alumni_directory():
        q = clean(request.args.get("q"), 100)
        department = clean(request.args.get("department"), 120)
        year = request.args.get("graduation_year", type=int)
        page = request.args.get("page", 1, type=int)

        query = Alumni.query.filter_by(
            verification_status="approved",
            is_visible=True,
            is_public=True
        )

        if q:
            query = query.filter(
                Alumni.full_name.ilike(f"%{q}%")
            )

        if department:
            query = query.filter(
                Alumni.department == department
            )

        if year:
            query = query.filter(
                Alumni.graduation_year == year
            )

        pagination = query.order_by(
            Alumni.full_name
        ).paginate(
            page=page,
            per_page=PER_PAGE,
            error_out=False
        )

        public = Alumni.query.filter_by(
            verification_status="approved",
            is_visible=True,
            is_public=True
        )

        departments = [
            d for (d,) in public.with_entities(
                Alumni.department
            ).distinct().order_by(Alumni.department)
        ]

        years = [
            y for (y,) in public.with_entities(
                Alumni.graduation_year
            ).distinct().order_by(Alumni.graduation_year.desc())
        ]

        return render_template(
            "directory.html",
            pagination=pagination,
            alumni=pagination.items,
            departments=departments,
            years=years,
            q=q,
            department=department,
            graduation_year=year,
        )

    @app.route("/alumni/profile/<int:id>")
    def alumni_profile(id):
        profile = db.get_or_404(Alumni, id)

        is_owner = (
            current_user.is_authenticated
            and profile.user_id == current_user.id
        )

        is_admin = (
            current_user.is_authenticated
            and current_user.is_admin
        )

        if not (is_owner or is_admin):
            if (
                profile.verification_status != "approved"
                or not profile.is_visible
                or not profile.is_public
            ):
                abort(404)

        return render_template(
            "profile.html",
            profile=profile,
            is_owner=is_owner
        )

    @app.route("/profile/edit", methods=["GET", "POST"])
    @login_required
    def edit_profile():
        profile = current_user.alumni

        if profile is None:
            abort(404)

        if request.method == "GET":
            return render_template(
                "edit_profile.html",
                profile=profile
            )

        data, errors = validate_profile_fields(request.form)

        if errors:
            for e in errors:
                flash(e, "danger")

            return render_template(
                "edit_profile.html",
                profile=profile
            ), 400

        identity_changed = any(
            getattr(profile, f) != data[f]
            for f in (
                "full_name",
                "department",
                "degree",
                "graduation_year"
            )
        )

        for k, v in data.items():
            setattr(profile, k, v)

        profile.is_visible = (
            request.form.get("is_visible") == "on"
        )

        if (
            identity_changed
            and profile.verification_status == "approved"
        ):
            profile.verification_status = "pending"
            profile.verified_by = None
            profile.verified_at = None

            flash(
                "You changed identity details, so your profile needs to be re-verified.",
                "warning"
            )

        db.session.commit()
        flash("Profile updated.", "success")

        return redirect(
            url_for("alumni_profile", id=profile.id)
        )

    @app.route("/admin/verifications")
    @admin_required
    def admin_verifications():
        status = request.args.get("status", "pending")

        if status not in ("pending", "approved", "rejected"):
            status = "pending"

        profiles = (
            Alumni.query
            .filter_by(verification_status=status)
            .order_by(Alumni.id.desc())
            .all()
        )

        return render_template(
            "admin_verifications.html",
            profiles=profiles,
            status=status
        )

    def _set_status(id, status):
        profile = db.get_or_404(Alumni, id)
        profile.verification_status = status
        profile.verified_by = current_user.id
        profile.verified_at = utcnow()

        db.session.commit()

        flash(
            f"{profile.full_name} marked as {status}.",
            "success"
        )

        return redirect(url_for("admin_verifications"))

    @app.route("/admin/approve/<int:id>", methods=["POST"])
    @admin_required
    def admin_approve(id):
        return _set_status(id, "approved")

    @app.route("/admin/reject/<int:id>", methods=["POST"])
    @admin_required
    def admin_reject(id):
        return _set_status(id, "rejected")

    @app.route("/admin/visibility/<int:id>", methods=["POST"])
    @admin_required
    def admin_toggle_visibility(id):
        profile = db.get_or_404(Alumni, id)
        profile.is_visible = not profile.is_visible
        db.session.commit()

        flash("Visibility updated.", "success")

        return redirect(
            request.referrer or url_for("admin_verifications")
        )

    # ---------------- MENTORSHIP ----------------

    @app.route(
        "/profile/mentorship-availability",
        methods=["POST"]
    )
    @login_required
    def mentorship_availability():
        profile = current_user.alumni

        if profile is None:
            abort(404)

        enabled = (
            request.form.get("available_for_mentorship") == "on"
        )

        if (
            enabled
            and profile.verification_status != "approved"
        ):
            flash(
                "Your alumni profile must be approved before you can offer mentorship.",
                "warning"
            )
            return redirect(
                url_for("alumni_profile", id=profile.id)
            )

        profile.available_for_mentorship = enabled
        db.session.commit()

        flash("Mentorship availability updated.", "success")

        return redirect(
            url_for("alumni_profile", id=profile.id)
        )

    @app.route("/mentorship/request/<int:mentor_id>", methods=["POST"])
    @login_required
    def mentorship_request(mentor_id):
        mentee = current_user.alumni

        if mentee is None:
            abort(404)

        if mentee.verification_status != "approved":
            abort(403)

        mentor = db.get_or_404(Alumni, mentor_id)

        if mentor.id == mentee.id:
            flash(
                "You cannot request mentorship from yourself.",
                "warning"
            )
            return redirect(
                url_for("alumni_profile", id=mentor.id)
            )

        if (
            mentor.verification_status != "approved"
            or not mentor.available_for_mentorship
            or not mentor.is_visible
            or not mentor.is_public
            or mentor.user_id is None
        ):
            abort(404)

        existing = Mentorship.query.filter(
            Mentorship.mentor_id == mentor.id,
            Mentorship.mentee_id == mentee.id,
            Mentorship.status.in_(["pending", "accepted"])
        ).first()

        if existing:
            flash(
                "You already have an active request with this alumnus.",
                "info"
            )
            return redirect(
                url_for("alumni_profile", id=mentor.id)
            )

        message = clean(
            request.form.get("message"),
            2000
        )

        mentorship = Mentorship(
            mentor_id=mentor.id,
            mentee_id=mentee.id,
            message=message or None,
            status="pending"
        )

        db.session.add(mentorship)
        db.session.commit()

        flash("Mentorship request sent.", "success")

        return redirect(
            url_for("alumni_profile", id=mentor.id)
        )

    @app.route("/mentorship/received")
    @login_required
    def mentorship_received():
        profile = current_user.alumni

        if profile is None:
            abort(404)

        requests_received = (
            Mentorship.query
            .filter_by(mentor_id=profile.id)
            .order_by(Mentorship.requested_at.desc())
            .all()
        )

        return render_template(
            "mentorship_received.html",
            requests_received=requests_received
        )

    @app.route("/mentorship/sent")
    @login_required
    def mentorship_sent():
        profile = current_user.alumni

        if profile is None:
            abort(404)

        requests_sent = (
            Mentorship.query
            .filter_by(mentee_id=profile.id)
            .order_by(Mentorship.requested_at.desc())
            .all()
        )

        return render_template(
            "mentorship_sent.html",
            requests_sent=requests_sent
        )

    @app.route(
        "/mentorship/<int:request_id>/respond",
        methods=["POST"]
    )
    @login_required
    def mentorship_respond(request_id):
        profile = current_user.alumni

        if profile is None:
            abort(404)

        mentorship = db.get_or_404(Mentorship, request_id)

        if mentorship.mentor_id != profile.id:
            abort(403)

        if mentorship.status != "pending":
            flash(
                "This request has already been processed.",
                "warning"
            )
            return redirect(
                url_for("mentorship_received")
            )

        action = request.form.get("action")

        if action not in ("accept", "reject"):
            abort(400)

        mentorship.status = (
            "accepted" if action == "accept" else "rejected"
        )

        db.session.commit()

        flash(
            f"Mentorship request {mentorship.status}.",
            "success"
        )

        return redirect(
            url_for("mentorship_received")
        )

    @app.route(
        "/mentorship/<int:request_id>/cancel",
        methods=["POST"]
    )
    @login_required
    def mentorship_cancel(request_id):
        profile = current_user.alumni

        if profile is None:
            abort(404)

        mentorship = db.get_or_404(Mentorship, request_id)

        if mentorship.mentee_id != profile.id:
            abort(403)

        if mentorship.status != "pending":
            flash(
                "Only pending requests can be cancelled.",
                "warning"
            )
            return redirect(
                url_for("mentorship_sent")
            )

        db.session.delete(mentorship)
        db.session.commit()

        flash("Mentorship request cancelled.", "success")

        return redirect(
            url_for("mentorship_sent")
        )

    @app.errorhandler(403)
    def forbidden(_e):
        return render_template(
            "error.html",
            code=403,
            message="You don't have permission."
        ), 403

    @app.errorhandler(404)
    def not_found(_e):
        return render_template(
            "error.html",
            code=404,
            message="Page not found."
        ), 404


def register_cli(app):

    @app.cli.command("init-db")
    def init_db():
        """Create all tables."""
        db.create_all()
        click.echo("Database initialized.")

    @app.cli.command("create-admin")
    @click.option("--email", prompt=True)
    @click.password_option()
    def create_admin(email, password):
        """Admins are created here, never via public registration."""
        email = email.strip().lower()

        if User.query.filter_by(email=email).first():
            raise click.ClickException(
                "A user with that email already exists."
            )

        user = User(
            email=email,
            role="admin",
            email_verified=True
        )

        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        click.echo(f"Admin {email} created.")

    @app.cli.command("seed-sample")
    def seed_sample():
        """Add FICTIONAL sample alumni for development."""
        samples = [
            (
                "Asha Raman", "Computer Science", "B.Sc",
                2018, "Software Engineer", "ExampleSoft"
            ),
            (
                "Karthik Iyer", "Mechanical Engineering", "B.E",
                2015, "Design Engineer", "Sample Motors"
            ),
            (
                "Meera Nair", "Commerce", "B.Com",
                2020, "Analyst", "Demo Capital"
            ),
        ]

        for name, dept, deg, yr, occ, comp in samples:
            db.session.add(
                Alumni(
                    full_name=name,
                    department=dept,
                    degree=deg,
                    graduation_year=yr,
                    occupation=occ,
                    company=comp,
                    verification_status="approved",
                    is_visible=True,
                )
            )

        db.session.commit()
        click.echo("Sample records added.")


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
