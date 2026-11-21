# LegacyLink – Database Handoff

## 1. Overview

LegacyLink uses a relational database to manage user accounts and alumni profiles.

**Current stack:**
- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite (development)
- PostgreSQL (production)
- Flask-Migrate

## 2. Database Models

### User

Stores account information.

| Field | Purpose |
|---|---|
| id | Unique user ID |
| email | Unique email address |
| password_hash | Hashed password |
| role | User role |
| email_verified | Email verification status |
| created_at | Account creation time |

### Alumni

Stores alumni profile information.

| Field | Purpose |
|---|---|
| id | Unique alumni ID |
| user_id | Optional link to a user account |
| full_name | Alumni name |
| department | Academic department |
| degree | Degree earned |
| graduation_year | Year of graduation |
| occupation | Current occupation |
| company | Current company |
| skills | Alumni skills |
| bio | Profile description |
| verification_status | Pending, approved, or rejected |
| verified_by | Admin user who verified the profile |
| verified_at | Verification timestamp |
| is_visible | Directory visibility setting |
| is_public | Public profile setting |
| created_at | Creation timestamp |
| updated_at | Last update timestamp |

## 3. Relationships

- One user can have one alumni profile.
- An alumni profile can optionally belong to a user account.
- An alumni profile can reference the user who verified it.

## 4. Alumni Verification Workflow

1. Newly registered alumni profiles start as `pending`.
2. An authorized admin reviews the profile.
3. The admin can approve or reject the profile.
4. Only approved and appropriately visible profiles should appear in the public alumni directory.

Public directory queries should check the approval and visibility fields.

## 5. Database Initialization

For local development:

```powershell
flask --app app db upgrade
```

To run tests:

```powershell
pytest -v
```

To check database integrity:

```powershell
python check_database_integrity.py
```

## 6. Database Migrations

Flask-Migrate manages schema changes.

When models change, generate and review a migration before applying it:

```powershell
flask --app app db migrate -m "Describe database change"
flask --app app db upgrade
```

Do not edit previously applied migrations without coordinating with the team.

## 7. PostgreSQL Deployment

- SQLite is used for local development.
- PostgreSQL is intended for production deployment.
- Configure the production database connection using an environment variable.
- Never commit database passwords or connection credentials.
- Apply migrations after configuring the production database.

## 8. Important Notes for Integration

- Do not store plain-text passwords.
- Email addresses must remain unique.
- Required alumni fields must not be empty.
- Graduation years must be valid.
- Only authorized admins should approve alumni profiles.
- Public directory queries must respect verification and visibility settings.

**LegacyLink tagline:** Connections that last. Legacies that grow.