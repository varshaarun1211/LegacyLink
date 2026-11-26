
from datetime import date
from urllib.parse import urlparse

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from flask_login import login_required, current_user
from sqlalchemy import or_

from models import db, Alumni, Opportunity


opportunity_bp = Blueprint(
    "opportunity",
    __name__,
    url_prefix="/opportunities"
)


def get_current_alumni():
    """Get the alumni profile of the logged-in user."""
    return Alumni.query.filter_by(
        user_id=current_user.id
    ).first()


def validate_application_link(link):
    """Allow only valid HTTP or HTTPS application links."""
    if not link:
        return True

    parsed = urlparse(link)

    return (
        parsed.scheme in ("http", "https")
        and bool(parsed.netloc)
    )


# 1. BROWSE AND SEARCH OPPORTUNITIES

@opportunity_bp.route("/", methods=["GET"])
def list_opportunities():

    search_query = request.args.get("q", "").strip()

    query = Opportunity.query.filter_by(is_active=True)

    if search_query:
        search_pattern = f"%{search_query}%"

        query = query.filter(
            or_(
                Opportunity.title.ilike(search_pattern),
                Opportunity.company.ilike(search_pattern)
            )
        )

    opportunities = query.order_by(
        Opportunity.created_at.desc()
    ).all()

    return render_template(
        "opportunities.html",
        opportunities=opportunities,
        search_query=search_query
    )


# 2. VIEW OPPORTUNITY DETAILS

@opportunity_bp.route("/<int:opportunity_id>", methods=["GET"])
def opportunity_detail(opportunity_id):

    opportunity = Opportunity.query.filter_by(
        id=opportunity_id,
        is_active=True
    ).first_or_404()

    return render_template(
        "opportunity_detail.html",
        opportunity=opportunity
    )


# 3. CREATE AN OPPORTUNITY

@opportunity_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_opportunity():

    alumni = get_current_alumni()

    # Only approved alumni can post opportunities.
    if not alumni or alumni.verification_status != "approved":
        flash(
            "Only verified alumni can post opportunities. "
            "Please wait until your profile is approved.",
            "danger"
        )
        return redirect(
            url_for("opportunity.list_opportunities")
        )

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        company = request.form.get("company", "").strip()
        description = request.form.get("description", "").strip()
        opportunity_type = request.form.get(
            "opportunity_type", ""
        ).strip()
        location = request.form.get("location", "").strip()
        application_link = request.form.get(
            "application_link", ""
        ).strip()
        deadline_value = request.form.get("deadline", "").strip()

        if not all([
            title,
            company,
            description,
            opportunity_type
        ]):
            flash("Please fill in all required fields.", "danger")

        elif (
            len(title) > 150
            or len(company) > 150
            or len(opportunity_type) > 50
            or len(location) > 150
            or len(application_link) > 500
        ):
            flash(
                "One or more fields exceed the allowed length.",
                "danger"
            )

        elif not validate_application_link(application_link):
            flash(
                "Please enter a valid HTTP or HTTPS application link.",
                "danger"
            )

        else:
            deadline = None

            if deadline_value:
                try:
                    deadline = date.fromisoformat(deadline_value)
                except ValueError:
                    flash("Please enter a valid deadline.", "danger")
                    return render_template(
                        "opportunity_form.html",
                        opportunity=None
                    )

            opportunity = Opportunity(
                alumni_id=alumni.id,
                title=title,
                company=company,
                description=description,
                opportunity_type=opportunity_type,
                location=location or None,
                application_link=application_link or None,
                deadline=deadline
            )

            try:
                db.session.add(opportunity)
                db.session.commit()

                flash(
                    "Opportunity posted successfully!",
                    "success"
                )

                return redirect(
                    url_for(
                        "opportunity.opportunity_detail",
                        opportunity_id=opportunity.id
                    )
                )

            except Exception:
                db.session.rollback()
                flash(
                    "Unable to save the opportunity. Please try again.",
                    "danger"
                )

    return render_template(
        "opportunity_form.html",
        opportunity=None
    )
