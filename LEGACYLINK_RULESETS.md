# LEGACYLINK – PROJECT RULESETS

**Project Name:** LegacyLink  
**Project Tagline:** Connections that last. Legacies that grow.  
**Document Type:** System Rules and Constraints  
**Version:** 1.0  
**Status:** Project Development  
**Technology Stack:** Python, Flask, Flask-SQLAlchemy, SQLAlchemy, SQLite, PostgreSQL

---

## 1. INTRODUCTION

This document defines the rules, constraints, validation requirements, security standards and development guidelines governing the LegacyLink application.

LegacyLink is a college alumni networking platform designed to connect current students, graduates and alumni through professional networking, mentorship and institutional engagement.

These rules ensure that the application maintains data accuracy, security, consistency and reliable functionality.

### Rule Status Definitions

- **IMPLEMENTED:** Supported by the current database implementation.
- **PLANNED:** Intended functionality that requires further development or integration.
- **TO BE VERIFIED:** Requires checking against the complete application code.

---

## 2. USER AND ACCOUNT RULES

| Rule ID | Rule Description | Status |
|---|---|---|
| LL-USER-001 | Every registered user must have a unique email address. | IMPLEMENTED |
| LL-USER-002 | Passwords must be stored as securely generated hashes rather than plain text. | IMPLEMENTED |
| LL-USER-003 | Each user account must have an assigned role. | IMPLEMENTED |
| LL-USER-004 | User accounts must have an email verification status. | IMPLEMENTED |
| LL-USER-005 | Users must authenticate before accessing protected application features. | TO BE VERIFIED |
| LL-USER-006 | Users must not access administrative functions without administrator permissions. | PLANNED |
| LL-USER-007 | Account registration must validate required information. | TO BE VERIFIED |

---

## 3. SECURITY AND PRIVACY RULES

| Rule ID | Rule Description | Status |
|---|---|---|
| LL-SEC-001 | Sensitive account credentials must never be stored in plain text. | IMPLEMENTED |
| LL-SEC-002 | User information must only be accessible according to authorised permissions. | PLANNED |
| LL-SEC-003 | Private alumni information must not be publicly exposed without permission. | PLANNED |
| LL-SEC-004 | Administrative operations must be restricted to authorised administrators. | PLANNED |
| LL-SEC-005 | External profile links must be validated before being accepted. | PLANNED |
| LL-SEC-006 | Personal information must be collected and displayed responsibly, respecting user consent. | PLANNED |
| LL-SEC-007 | Database credentials and secret configuration values must not be committed to public repositories. | PLANNED |

---

## 4. ALUMNI PROFILE RULES

| Rule ID | Rule Description | Status |
|---|---|---|
| LL-ALUMNI-001 | An alumni profile may be linked to a registered user account. | IMPLEMENTED |
| LL-ALUMNI-002 | An alumni profile must contain a valid full name. | IMPLEMENTED |
| LL-ALUMNI-003 | Department and degree information must be provided. | IMPLEMENTED |
| LL-ALUMNI-004 | Graduation year must be an integer between 1900 and the current year. | IMPLEMENTED |
| LL-ALUMNI-005 | Alumni profiles must have a verification status. | IMPLEMENTED |
| LL-ALUMNI-006 | Verification status must be pending, approved or rejected. | IMPLEMENTED |
| LL-ALUMNI-007 | Alumni profiles may include professional information such as occupation and company. | IMPLEMENTED |
| LL-ALUMNI-008 | Alumni profiles may include skills, biography and career interests. | IMPLEMENTED |
| LL-ALUMNI-009 | Alumni may provide LinkedIn, GitHub and portfolio URLs. | IMPLEMENTED |
| LL-ALUMNI-010 | Alumni may indicate whether they are available for mentorship. | IMPLEMENTED |
| LL-ALUMNI-011 | Alumni must be able to control whether their profiles are visible or public, according to application permissions. | PLANNED |
| LL-ALUMNI-012 | Alumni information must be reviewed before an administrator approves a profile. | PLANNED |

---

## 5. MENTORSHIP RULES

| Rule ID | Rule Description | Status |
|---|---|---|
| LL-MENTOR-001 | Every mentorship request must reference an existing mentor profile. | IMPLEMENTED |
| LL-MENTOR-002 | Every mentorship request must reference an existing mentee profile. | IMPLEMENTED |
| LL-MENTOR-003 | An alumnus cannot send a mentorship request to themselves. | IMPLEMENTED |
| LL-MENTOR-004 | Every mentorship request must have a valid status. | IMPLEMENTED |
| LL-MENTOR-005 | Valid mentorship statuses are pending, accepted and rejected. | IMPLEMENTED |
| LL-MENTOR-006 | Mentorship requests may contain an introductory message. | IMPLEMENTED |
| LL-MENTOR-007 | Users should be able to view their mentorship requests. | PLANNED |
| LL-MENTOR-008 | Only authorised users should be able to respond to their mentorship requests. | PLANNED |
| LL-MENTOR-009 | Mentorship request updates must be recorded with timestamps. | IMPLEMENTED |

---

## 6. DATABASE MANAGEMENT RULES

| Rule ID | Rule Description | Status |
|---|---|---|
| LL-DB-001 | Every database table must have an appropriate primary key. | IMPLEMENTED |
| LL-DB-002 | Foreign keys must maintain valid relationships between related records. | IMPLEMENTED |
| LL-DB-003 | Email addresses in the users table must remain unique. | IMPLEMENTED |
| LL-DB-004 | An alumni profile's linked user ID must be unique when provided. | IMPLEMENTED |
| LL-DB-005 | Mentorship records must reference valid alumni records. | IMPLEMENTED |
| LL-DB-006 | Database relationships must be maintained using appropriate foreign key constraints. | IMPLEMENTED |
| LL-DB-007 | Database schema modifications must be managed through migration scripts. | IMPLEMENTED |
| LL-DB-008 | Existing database records must be preserved during normal schema migrations. | PLANNED |
| LL-DB-009 | Database integrity must be checked during development and testing. | IMPLEMENTED |
| LL-DB-010 | The application must support the planned transition from SQLite development storage to PostgreSQL production storage. | PLANNED |

---

## 7. ADMINISTRATIVE RULES

| Rule ID | Rule Description | Status |
|---|---|---|
| LL-ADMIN-001 | Administrator accounts must have an assigned administrative role. | IMPLEMENTED |
| LL-ADMIN-002 | Only authorised administrators should approve alumni profiles. | PLANNED |
| LL-ADMIN-003 | Only authorised administrators should reject alumni profiles. | PLANNED |
| LL-ADMIN-004 | The administrator responsible for verification should be recorded. | IMPLEMENTED |
| LL-ADMIN-005 | The date and time of profile verification should be recorded. | IMPLEMENTED |
| LL-ADMIN-006 | Administrative actions should be restricted to authorised users. | PLANNED |

---

## 8. DEVELOPMENT AND COLLABORATION RULES

| Rule ID | Rule Description | Status |
|---|---|---|
| LL-DEV-001 | Source code must follow consistent naming conventions. | PLANNED |
| LL-DEV-002 | Database models must be maintained separately from presentation templates. | IMPLEMENTED |
| LL-DEV-003 | Database schema changes must be documented. | PLANNED |
| LL-DEV-004 | New functionality should include appropriate tests. | PLANNED |
| LL-DEV-005 | Changes must be reviewed before being merged into the main project branch. | PLANNED |
| LL-DEV-006 | Sensitive configuration files and local database files must not be committed accidentally. | PLANNED |
| LL-DEV-007 | Commit messages should clearly describe the changes being introduced. | PLANNED |
| LL-DEV-008 | Existing functionality must be checked after significant changes. | PLANNED |

---

## 9. VALIDATION AND ERROR HANDLING RULES

| Rule ID | Rule Description | Status |
|---|---|---|
| LL-VAL-001 | Required fields must not contain empty values. | IMPLEMENTED |
| LL-VAL-002 | Graduation year must fall within the permitted range. | IMPLEMENTED |
| LL-VAL-003 | Invalid verification statuses must be rejected. | IMPLEMENTED |
| LL-VAL-004 | Invalid mentorship statuses must be rejected. | IMPLEMENTED |
| LL-VAL-005 | Duplicate user email addresses must be prevented. | IMPLEMENTED |
| LL-VAL-006 | Invalid foreign key references must be rejected by the database. | IMPLEMENTED |
| LL-VAL-007 | Application errors should provide understandable feedback without exposing sensitive technical information. | PLANNED |

---

## 10. TESTING RULES

The LegacyLink application must be tested to ensure that its database and application logic behave as expected.

The following testing requirements apply:

1. User email uniqueness must be tested.
2. Alumni required-field validation must be tested.
3. Invalid graduation years must be rejected.
4. Invalid verification statuses must be rejected.
5. Invalid user references must be rejected.
6. Mentorship request creation must be tested.
7. Invalid mentorship statuses must be rejected.
8. Self-mentorship requests must be prevented.
9. Database relationships and integrity must be checked.
10. Tests must be repeated after relevant database or application changes.

**Current testing record:** Eight automated database model tests have passed using pytest.

---

## 11. DATA COLLECTION AND ALUMNI VERIFICATION

LegacyLink uses its own database rather than directly extracting alumni profiles from third-party platforms.

The following principles apply:

1. Alumni should provide their information voluntarily.
2. Information supplied by users must be handled responsibly.
3. LinkedIn profile URLs may be stored as optional professional references.
4. Alumni information obtained from the institution must be collected only through authorised channels.
5. Administrators should review alumni information before approving profiles.
6. The application should not scrape or copy third-party profile information without appropriate authorisation.

---

## 12. FUTURE DEVELOPMENT RULES

As LegacyLink expands, additional functionality may be introduced.

Potential future modules include:

- Alumni job and internship opportunities.
- Alumni networking events and registrations.
- Direct alumni messaging.
- Alumni success stories.
- Alumni recommendation systems.
- Administrative analytics dashboards.

Any new module must follow the existing security, validation, database integrity and development rules.

---

## 13. DOCUMENT MAINTENANCE

This document must be updated whenever important application rules, database constraints, security requirements or development standards change.

New rules should receive unique identifiers to maintain consistency.

The implementation status of each rule must be reviewed against the actual source code before being changed from Planned or To Be Verified to Implemented.

---

## 14. CONCLUSION

These rulesets establish a common standard for the development and maintenance of LegacyLink.

They help ensure that the application remains secure, organised, reliable and consistent while supporting its primary objective of connecting alumni, students and educational institutions.

**End of Document**

**Project:** LegacyLink  
**Document:** LEGACYLINK_RULESETS.md  
**Version:** 1.0