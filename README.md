# LegacyLink

**Connections that last. Legacies that grow.**

LegacyLink is a college-specific alumni networking platform designed to connect former students, help alumni maintain professional relationships, and support mentorship and career opportunities.

## Technology Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML and CSS

## Database Structure

LegacyLink currently uses SQLite for development.

### 1. Users Table

Stores account and login information.

- `id`: Unique user ID (primary key)
- `email`: User email address (unique)
- `password_hash`: Securely hashed password
- `role`: User role
- `email_verified`: Email verification status
- `created_at`: Account creation date

### 2. Alumni Table

Stores alumni profile information.

- `id`: Unique alumni profile ID (primary key)
- `user_id`: Linked user ID (foreign key, nullable and unique)
- `full_name`: Alumni name
- `department`: Academic department
- `degree`: Degree obtained
- `graduation_year`: Graduation year
- `occupation`: Current occupation
- `company`: Current company
- `skills`: Alumni skills
- `bio`: Profile description
- `verification_status`: Pending, approved, or rejected
- `is_visible`: Directory visibility
- `verified_by`: Admin user ID who verified the profile
- `verified_at`: Verification date and time
- `created_at`: Profile creation date
- `updated_at`: Last profile update date and time

## Relationships

- One user can have one alumni profile.
- Alumni profiles are linked to users through `user_id`.
- Alumni profiles can exist without a linked user account, allowing authorized CSV imports.
- Each alumni profile can be reviewed through the verification process.

## Database Constraints and Validation

- User email addresses must be unique.
- Alumni profile `user_id` values must reference valid user accounts when provided.
- Each user can have at most one linked alumni profile.
- Full name, department, and degree are required.
- Graduation year must be a valid year between 1950 and the current year.
- Verification status must be `pending`, `approved`, or `rejected`.

## Database Indexes

The Alumni table includes indexes to improve query performance:

- `department`: Supports faster department-based searches.
- `graduation_year`: Supports faster graduation-year filtering.

## Database Migrations

LegacyLink uses Flask-Migrate to manage database schema changes.

To initialize migrations for a fresh development setup:

```powershell
flask --app app db init

## Security and Verification

- Passwords are stored as hashes, never as plain text.
- New alumni profiles start with pending verification.
- Pending profiles remain hidden from the directory.
- Rejected profiles remain hidden.
- Only approved and visible profiles should appear in the alumni directory.
- Admin accounts should be created through an authorized process.

## CSV Import

LegacyLink supports importing alumni profile data through a CSV file.

- CSV files are read using Python's `csv` module.
- Duplicate detection checks full name, department, and graduation year.
- Imported profiles start with pending verification.
- Imported profiles are hidden until approved.
- Imported records can exist without a linked user account.

## Database Testing

The database has been tested for:

- Creating, reading, updating, and deleting records.
- User and alumni profile relationships.
- Duplicate email constraints.
- Graduation year validation.
- Required field validation.
- Verification status validation.
- Alumni approval and rejection behaviour.
- CSV importing and duplicate prevention.
- Foreign-key integrity.
- Orphaned alumni records.
- Duplicate alumni records.

The latest database integrity checks reported:

- No duplicate alumni records.
- No duplicate user email addresses.
- No foreign-key violations.
- No orphaned alumni records.

## Project Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Run the application using `python app.py`.

## Future Improvements

- Alumni search and filtering
- Admin verification dashboard
- CSV import for authorized alumni records
- Mentorship and networking features
- Career opportunities and events
- PostgreSQL database for production deployment

## Entity Relationship Diagram

```mermaid
erDiagram
    USERS ||--o| ALUMNI : has

    USERS {
        int id PK
        string email
        string password_hash
        string role
    }

    ALUMNI {
        int id PK
        int user_id FK
        string full_name
        string department
        string degree
        int graduation_year
        string verification_status
    }
```
