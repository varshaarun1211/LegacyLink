# LegacyLink

**Connections that last. Legacies that grow.**

A lightweight alumni networking platform built for a single college, using Python and Flask.

LegacyLink helps graduates of one college stay connected, keep their professional profiles up to date, and find each other through a searchable directory. Every registration is checked by an administrator before it appears publicly, so the directory only ever lists genuine alumni. The code is deliberately small and easy to read: one Flask file, one SQLite database, and a handful of templates.

This is an early version focused on the essentials. Events, job opportunities and mentorship are planned for later releases.

## Features

- **Alumni registration** - Alumni sign up with their name, email, department, degree and graduation year.
- **Admin verification** - New accounts stay `pending` until an administrator approves or rejects them.
- **Secure login** - Passwords are stored as hashes, never as plain text.
- **Alumni directory** - Only approved and visible profiles are listed.
- **Search and filters** - Search by name and filter by department or graduation year.
- **Protected admin routes** - Permissions are checked on the backend, not just hidden in the interface.
- **Simple stack** - Python, Flask, Flask-SQLAlchemy and SQLite. No extra services required.

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Backend | Flask |
| Database | SQLite via Flask-SQLAlchemy |
| Frontend | HTML, Jinja templates, Bootstrap |
| Version control | Git and GitHub |
| Deployment | Render (planned) |

## Project Structure

```
LegacyLink/
├── app.py              # Flask app, database models and routes
├── requirements.txt    # Python dependencies
├── .gitignore          # Keeps the database and venv out of GitHub
├── README.md
└── templates/
    ├── base.html
    ├── register.html
    ├── login.html
    ├── alumni.html
    └── verifications.html
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

The SQLite database (`instance/legacylink.db`) is created automatically on first run. Open http://127.0.0.1:5000 in your browser.

### 5. Create an admin account

Admins cannot register publicly. Create one from the terminal:

```bash
flask --app app create-admin
```

## How It Works

1. An alumnus registers. Their profile is saved with `verification_status = "pending"`.
2. An admin opens `/admin/verifications` and checks the details against authorized college records.
3. The admin approves or rejects the registration.
4. Approved and visible profiles appear in the alumni directory.

## Routes

| Route | Method | Purpose |
|---|---|---|
| `/register` | GET, POST | Alumni registration |
| `/login` | GET, POST | Log in |
| `/logout` | POST | Log out |
| `/alumni` | GET | Alumni directory with search and filters |
| `/admin/verifications` | GET | View pending registrations (admin only) |
| `/admin/approve/<id>` | POST | Approve a profile (admin only) |
| `/admin/reject/<id>` | POST | Reject a profile (admin only) |

## Security and Privacy

- Passwords are hashed with Werkzeug.
- Admin routes are restricted on the server.
- Pending and rejected profiles never appear in the directory.
- Use **fictional sample data** during development.
- Never commit the database or real alumni information to GitHub.
- Set a strong `SECRET_KEY` environment variable before deploying.

## Roadmap

- [ ] Alumni profile page and profile editing
- [ ] Email confirmation
- [ ] CSRF protection
- [ ] Events and reunions
- [ ] Job and internship postings
- [ ] Mentorship requests
- [ ] Deployment on Render with a persistent database

## Contributing

1. Create a branch: `git checkout -b feature-name`
2. Commit your changes: `git commit -m "Describe your change"`
3. Push the branch: `git push origin feature-name`
4. Open a pull request on GitHub.

## License

Add a license of your choice (for example MIT) before making the repository public.
