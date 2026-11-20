@'
# LegacyLink Database Documentation

## Database
- Development: SQLite
- Planned deployment: PostgreSQL
- ORM: Flask-SQLAlchemy

## Tables

### users
- id
- email
- password_hash
- role
- email_verified
- created_at

### alumni
- id
- user_id
- full_name
- department
- degree
- graduation_year
- occupation
- company
- skills
- bio
- verification_status
- verified_by
- verified_at
- is_visible
- is_public
- created_at
- updated_at

## Database Features
- Unique user email addresses
- Alumni-to-user relationship
- Foreign-key constraints
- Required-field validation
- Graduation-year validation
- Verification statuses: pending, approved, rejected
- Duplicate alumni prevention during CSV import
- CSV import skips invalid records
- Imported alumni profiles start pending and hidden

## Testing
- CRUD tests
- Database integrity checks
- Duplicate-record checks
- Foreign-key checks
- CSV import validation

## Setup
Install dependencies:

```bash
pip install -r requirements.txt