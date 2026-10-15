# AppSec Messenger — Flask

[Русская версия](README.ru.md)

Server-side messenger built with Python and Flask. Part of a self-paced
AppSec learning roadmap.

This is **Stage 4** of the roadmap — a Flask-based backend with routing,
templates, and simple authentication (sessions). It builds on the
client-side part from Stage 3 and serves as a foundation for the next
stages: database integration (Stage 5) and web vulnerabilities (Stage 6+).

## Screenshots

### Login
![Login page](static/screenshots/login.png)

### Chat
![Chat page](static/screenshots/chat.png)

## Tech Stack

- Python 3.14
- Flask 3.1
- Jinja2 (templates)
- HTML5, CSS3, Vanilla JavaScript

## Features

- User registration with **server-side validation**
  - Username (min 3 characters)
  - Email format
  - Password (min 6 characters)
  - Password confirmation
  - Duplicate username check
- Login with credentials verification
- Session-based authentication (Flask sessions with signed cookies)
- Protected `/chat` route — accessible only to logged-in users
- Logout
- Redirect of authenticated users from `/` and `/login` to `/chat`

## Limitations (by design)

- Users are stored **in memory** (`users = {}`), not in a database.
  → Data is lost on server restart. Database — Stage 5.
- Passwords are stored **in plaintext**.
  → Hashing — Stage 45.
- Messages are stored **in the browser only** (`chat.js`).
  → Message persistence — Stage 5.
- Client-side validation is **for UX only** — the server duplicates every check.

## Project Structure

```
appsec-messenger-flask/
├── app.py                  Flask application
├── requirements.txt        Python dependencies
├── templates/
│   ├── index.html          Registration page
│   ├── login.html          Login page
│   └── chat.html           Chat page
├── static/
│   ├── css/
│   │   └── style.css       Styles
│   ├── js/
│   │   ├── auth.js         Registration form validation
│   │   └── chat.js         Chat logic
│   └── screenshots/
└── venv/                   (not tracked)
```

## Routes

| Method | URL | Description |
|--------|-----|-------------|
| GET / POST | `/` | Registration |
| GET / POST | `/login` | Login |
| GET | `/chat` | Chat (protected) |
| GET | `/logout` | Logout |

## How to Run

1. Install **Python 3.10+**.
2. Clone the repository:
   ```bash
   git clone https://github.com/foxxxymiron/appsec-messenger-flask.git
   ```
3. Open the project folder in VS Code.
4. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
5. Activate it:
   - Windows: `venv\Scripts\Activate.ps1`
   - Linux/macOS: `source venv/bin/activate`
6. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
7. Run the server:
   ```bash
   python app.py
   ```
8. Open `http://127.0.0.1:5000` in your browser.

## Roadmap

- [x] **Stage 3** — Client-side part (HTML + CSS + JS)
- [x] **Stage 4** — Flask backend: routing, templates, simple auth
- [ ] Stage 5 — Database (SQLite), CRUD operations
- [ ] Stage 6+ — Web vulnerabilities (SQLi, XSS, CSRF, etc.)

## Notes

Client-side validation is intended for UX only — it can be bypassed
via DevTools. Real validation is implemented **on the server**
(see `app.py`). This is the core principle of AppSec: **never trust the client**.

## Author

- **Ivantsov Maxim**
- GitHub: [@foxxxymiron](https://github.com/foxxxymiron)