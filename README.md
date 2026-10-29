# AppSec Messenger — Flask

[Русская версия](README.ru.md)

Server-side messenger built with Python and Flask. Part of a self-paced AppSec learning roadmap.

This is the main project of the roadmap, where vulnerabilities are intentionally introduced, exploited, and then mitigated. **Stages 1-8 are completed.**

## Screenshots

### Login
![Login page](static/screenshots/login.png)

### Chat
![Chat page](static/screenshots/chat.png)

## 🎯 Roadmap Progress

- [x] **Stage 1:** Introduction to AppSec (Theory)
- [x] **Stage 2:** Python Basics (Theory & Practice)
- [x] **Stage 3:** Client-side (HTML/CSS/JS)
- [x] **Stage 4:** Flask Backend & Auth
- [x] **Stage 5:** SQLite Database & CRUD
- [x] **Stage 6:** SQL Injection (UNION-based) & Mitigation
- [x] **Stage 7:** Blind SQL Injection (Time, Boolean, Error) & Mitigation
- [x] **Stage 8:** Cross-Site Scripting (Stored XSS) & Mitigation

## Tech Stack

- Python 3.14
- Flask 3.1
- Jinja2 (templates)
- SQLite (database)
- HTML5, CSS3, Vanilla JavaScript

## Features

- User registration with **server-side validation**:
  - Username (min 3 characters)
  - Email format
  - Password (min 6 characters)
  - Password confirmation
  - Duplicate username check
- Login with credentials verification
- Session-based authentication (Flask sessions with signed cookies)
- Protected `/chat` route — accessible only to logged-in users
- Logout
- **Persistent storage** in SQLite:
  - `users` table — credentials
  - `messages` table — chat history
- **Messages API**:
  - `GET /api/messages` — fetch message history
  - `POST /api/messages` — send a new message
- **Security Labs (Intentionally Vulnerable):**
  - SQL Injection (UNION-based) in `/login` and `/search` (Mitigated).
  - Blind SQL Injection in `/login` (Mitigated).
  - Stored XSS in `chat.js` via `innerHTML` (Mitigated).

## Limitations (by design)

- Passwords are stored **in plaintext**.
  → Hashing — Stage 45.
- Client-side validation is **for UX only** — the server duplicates every check.
- Messages are broadcast to all users (no private conversations yet).

## Project Structure

```
appsec-messenger-flask/
├── app.py                  Flask application
├── init_db.py              Database initialization script
├── inject_xss.py           Script to inject XSS payload into DB (Stage 8)
├── requirements.txt        Python dependencies
├── app.db                  SQLite database (not tracked)
├── templates/
│   ├── index.html          Registration page
│   ├── login.html          Login page
│   ├── search.html         Search page (Vulnerable to SQLi in Stage 6)
│   └── chat.html           Chat page
├── static/
│   ├── css/
│   │   └── style.css       Styles
│   ├── js/
│   │   ├── auth.js         Registration form validation
│   │   └── chat.js         Chat logic (Fixed XSS in Stage 8)
│   └── screenshots/
├── writeups/               Local security reports for Stage 6-8
└── venv/                   (not tracked)
```

## Routes

| Method | URL | Description |
|--------|-----|-------------|
| GET / POST | `/` | Registration |
| GET / POST | `/login` | Login |
| GET | `/chat` | Chat (protected) |
| GET | `/search` | Search messages (protected, vulnerable to SQLi) |
| GET | `/logout` | Logout |
| GET / POST | `/api/messages` | Messages API (protected) |

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
7. Initialize the database:
   ```bash
   python init_db.py
   ```
8. Run the server:
   ```bash
   python app.py
   ```
9. Open `http://127.0.0.1:5000` in your browser.

## Mitigation Notes

All vulnerabilities introduced during the roadmap have been patched using best practices:
- **SQL Injection:** Prevented by using **Parameterized Queries** (`?` placeholders), which strictly separate SQL code from user input.
- **Stored XSS:** Prevented by using **Safe DOM APIs** (`textContent` instead of `innerHTML`), which treat user input as plain text and prevent HTML/JS execution.

*The malicious XSS payload remains in the database to demonstrate that safe rendering prevents execution even if malicious data is stored.*

## Notes

Client-side validation is intended for UX only — it can be bypassed via DevTools. Real validation is implemented **on the server** (see `app.py`). This is the core principle of AppSec: **never trust the client**.

Security headers like `HttpOnly` cookies and safe DOM rendering provide Defense in Depth against session hijacking and XSS.

## Author

- **Ivantsov Maxim**
- GitHub: [@foxxxymiron](https://github.com/foxxxymiron)