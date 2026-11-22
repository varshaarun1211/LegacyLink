
# LegacyLink – Database Handoff and Integration Guide

**Tagline:** Connections that last. Legacies that grow.

## 1. Project Overview

LegacyLink is a college-specific alumni networking platform designed to help alumni connect, share career experiences, and participate in mentorship.

The database supports:
- User registration and authentication data
- Alumni profiles
- Alumni verification
- Advanced alumni directory filtering
- Enhanced profile information
- Mentorship requests and status tracking

### Technology Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Migrate / Alembic
- SQLite for local development
- PostgreSQL planned for production
- pytest for database testing

---

## 2. Database Tables

The database currently contains three main tables:

1. `users`
2. `alumni`
3. `mentorships`

### 2.1 User table

Stores login and account information.

| Field | Type | Requirements | Purpose |
|---|---|---|---|
| id | Integer | Primary key | Unique user ID |
| email | String | Unique | User email |
| password_hash | String | Required | Hashed password |
| role | String | Required | User role |
| email_verified | Boolean | Required | Email verification status |
| created_at | DateTime | Creation timestamp | Account creation time |

**Important:** Passwords must never be stored as plain text. Admin privileges must be restricted to authorized users.

### 2.2 Alumni table

Stores alumni profile information.

| Field | Type | Requirements | Purpose |
|---|---|---|---|
| id | Integer | Primary key | Unique alumni ID |
| user_id | Integer | Optional, unique FK | Linked user account |
| full_name | String(150) | Required | Alumni name |
| department | String(120) | Required, indexed | Academic department |
| degree | String(120) | Required | Degree earned |
| graduation_year | Integer | Required, indexed | Graduation year |
| occupation | String(150) | Optional | Current occupation |
| company | String(150) | Optional, indexed | Current company |
| skills | Text | Optional | Alumni skills |
| bio | Text | Optional | Profile description |
| linkedin_url | String(255) | Optional | LinkedIn profile |
| github_url | String(255) | Optional | GitHub profile |
| portfolio_url | String(255) | Optional | Portfolio website |
| career_interests | Text | Optional | Career interests |
| available_for_mentorship | Boolean | Required, default false | Mentorship opt-in |
| verification_status | String(20) | Required | Pending, approved, or rejected |
| verified_by | Integer | Optional FK | Admin who verified profile |
| verified_at | DateTime | Optional | Verification timestamp |
| is_visible | Boolean | Required | Directory visibility |
| is_public | Boolean | Required | Public profile setting |
| created_at | DateTime | Creation timestamp | Profile creation |
| updated_at | DateTime | Update timestamp | Last profile update |

### 2.3 Mentorship table

Stores mentorship requests between alumni.

| Field | Type | Requirements | Purpose |
|---|---|---|---|
| id | Integer | Primary key | Unique request ID |
| mentor_id | Integer | Required FK to alumni.id | Alumni offering mentorship |
| mentee_id | Integer | Required FK to alumni.id | Alumni requesting mentorship |
| message | Text | Optional | Introductory message |
| status | String(20) | Required, default pending | Request status |
| requested_at | DateTime | Required | Request creation time |
| updated_at | DateTime | Required | Last status update |

Allowed mentorship statuses:
- `pending`
- `accepted`
- `rejected`

A database constraint prevents an alumnus from being both the mentor and mentee in the same request.

---

## 3. Database Relationships

### User and Alumni
- A user can have one alumni profile.
- An alumni profile can optionally be linked to a user account.
- An alumni profile can reference the user who verified it.

### Alumni and Mentorship
- One alumni can offer mentorship to multiple alumni.
- One alumni can request mentorship from multiple alumni.
- Each mentorship request has one mentor and one mentee.
- Both mentor and mentee reference the `alumni` table.

---

## 4. Feature Workflows

### 4.1 Registration and Profile Creation

1. A user registers an account.
2. The password is securely hashed.
3. An alumni profile can be linked to the account.
4. New alumni profiles should enter the verification process.

### 4.2 Alumni Verification

1. New profiles start with `pending` verification status.
2. An authorized administrator reviews the profile.
3. The administrator approves or rejects the profile.
4. Only approved and appropriately visible profiles should appear in the public directory.

### 4.3 Enhanced Alumni Profiles

Alumni profiles support:
- LinkedIn links
- GitHub links
- Portfolio links
- Career interests
- Mentorship availability

The backend should validate submitted URLs and ensure profile updates are authorized.

### 4.4 Advanced Alumni Directory

The database supports filtering by:

| Filter | Database field |
|---|---|
| Company | company |
| Skills | skills |
| Graduation year | graduation_year |
| Department | department |

The backend team should implement the directory queries and combine filters when users select multiple criteria.

For skills, the field is stored as Text. The backend should decide how to support keyword or skill matching.

Directory results must respect verification and visibility settings.

### 4.5 Mentorship Workflow

1. An alumnus opts into mentorship by setting `available_for_mentorship` to true.
2. Another alumnus finds an eligible mentor.
3. The mentee submits a mentorship request with an optional message.
4. The request is stored with `pending` status.
5. The mentor can accept or reject the request.
6. The status is updated accordingly.

Backend validation should ensure:
- The mentor exists.
- The mentee exists.
- The mentor is available for mentorship.
- The mentor and mentee are different alumni.
- Only the intended mentor can accept or reject a request.
- Only authorized users can access or update relevant requests.

---

## 5. Backend Integration Responsibilities

The backend team is responsible for:
- Creating Flask routes and API endpoints.
- User authentication and authorization.
- Profile creation and editing.
- Alumni verification operations.
- Directory filtering and search.
- Mentorship request creation and status updates.
- Input validation and error handling.
- Enforcing privacy and visibility rules.

The database models are not API endpoints. The backend should expose suitable APIs using these models.

### Suggested API design (not yet implemented)

| Method | Suggested endpoint | Purpose |
|---|---|---|
| GET | /api/alumni | Search and filter alumni |
| GET | /api/alumni/{id} | Retrieve an alumni profile |
| PUT | /api/alumni/{id} | Update an alumni profile |
| POST | /api/mentorships | Create a mentorship request |
| GET | /api/mentorships | Retrieve authorized mentorship requests |
| PATCH | /api/mentorships/{id} | Accept or reject a request |

These are proposed integration endpoints, not confirmed existing routes.

---

## 6. Frontend Integration Responsibilities

The frontend team is responsible for:
- Registration and login screens.
- Alumni profile creation and editing forms.
- Profile visibility indicators.
- Alumni directory and filters.
- Mentorship availability controls.
- Mentorship request forms.
- Pending, accepted, and rejected request displays.
- Admin verification screens.

The frontend must communicate with the backend APIs. It must not connect directly to the database.

---

## 7. Database Developer Responsibilities

The database work includes:
- Maintaining SQLAlchemy models.
- Managing database relationships and constraints.
- Creating and reviewing migrations.
- Maintaining database integrity checks.
- Writing database tests.
- Supporting CSV imports.
- Maintaining database documentation.
- Coordinating schema changes with backend and frontend developers.

---

## 8. Local Development Setup

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Apply database migrations:

```powershell
flask --app app db upgrade
```

Run tests:

```powershell
pytest -v
```

Check database integrity:

```powershell
python check_database_integrity.py
```

Generate a migration after model changes:

```powershell
flask --app app db migrate -m "Describe database change"
```

Review the generated migration before applying it.

Do not edit previously applied migrations without coordinating with the team.

---

## 9. Production Database Deployment

PostgreSQL is planned for production.

Deployment requirements:
- Configure the database connection through an environment variable.
- Never commit database passwords or credentials.
- Install the PostgreSQL driver.
- Apply migrations to the production database.
- Verify the production schema before integrating the backend.

SQLite is used locally; local data does not automatically transfer to PostgreSQL.

---

## 10. Integration Rules

1. Never store plain-text passwords.
2. Keep user email addresses unique.
3. Validate required alumni fields.
4. Validate graduation years.
5. Restrict admin verification to authorized administrators.
6. Respect profile visibility and verification status.
7. Allow mentorship only when the mentor has opted in.
8. Prevent self-mentorship requests.
9. Restrict mentorship request updates to authorized users.
10. Coordinate database schema changes with the whole team.

---

## 11. Current Implementation Status

| Feature | Database status |
|---|---|
| User model | Implemented |
| Alumni model | Implemented |
| Alumni verification fields | Implemented |
| Enhanced alumni profile fields | Implemented |
| Directory filter fields | Implemented |
| Company, department and graduation-year indexes | Implemented |
| Mentorship model | Implemented |
| Mentorship status validation | Implemented |
| Self-mentorship database constraint | Implemented |
| Database integrity checker | Updated |
| Database tests | Implemented and passing |
| Backend API endpoints | Backend team responsibility |
| Frontend screens | Frontend team responsibility |
| PostgreSQL production deployment | Pending integration |

---

**LegacyLink**

*Connections that last. Legacies that grow.*
