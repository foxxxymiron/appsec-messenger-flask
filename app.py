import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-me'


def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET' and 'username' in session:
        return redirect(url_for('chat'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirmPassword', '')

        error = None
        if len(username) < 3:
            error = 'Логин должен быть не менее 3 символов'
        elif '@' not in email or '.' not in email:
            error = 'Введите корректный email'
        elif len(password) < 6:
            error = 'Пароль должен быть не менее 6 символов'
        elif password != confirm:
            error = 'Пароли не совпадают'

        if not error:
            conn = get_db_connection()
            existing_user = conn.execute(
                'SELECT id FROM users WHERE username = ?', (username,)
            ).fetchone()
            if existing_user:
                error = 'Пользователь с таким логином уже существует'
            conn.close()

        if error:
            return render_template('index.html', error=error)

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (username, email, password)
        )
        conn.commit()
        conn.close()

        session['username'] = username
        return redirect(url_for('chat'))

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and 'username' in session:
        return redirect(url_for('chat'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        error = None

        conn = get_db_connection()
        user = conn.execute(
            'SELECT password FROM users WHERE username = ?', (username,)
        ).fetchone()
        conn.close()

        if not user:
            error = 'Пользователь не найден'
        elif user['password'] != password:
            error = 'Неверный пароль'

        if error:
            return render_template('login.html', error=error)

        session['username'] = username
        return redirect(url_for('chat'))

    return render_template('login.html')


@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html', username=session['username'])
from flask import jsonify


@app.route('/api/messages', methods=['GET', 'POST'])
def api_messages():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    current_user = session['username']
    conn = get_db_connection()

    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text', '').strip()
        recipient = data.get('recipient', 'Иван')

        if text:
            conn.execute(
                'INSERT INTO messages (sender, recipient, text) VALUES (?, ?, ?)',
                (current_user, recipient, text)
            )
            conn.commit()
        conn.close()
        return jsonify({'status': 'ok'})

    messages = conn.execute(
        'SELECT sender, recipient, text, timestamp FROM messages ORDER BY timestamp ASC'
    ).fetchall()
    conn.close()

    result = []
    for msg in messages:
        result.append({
            'sender': msg['sender'],
            'recipient': msg['recipient'],
            'text': msg['text'],
            'timestamp': msg['timestamp']
        })

    return jsonify(result)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


import webbrowser
from threading import Timer

if __name__ == '__main__':
    Timer(1, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(debug=True)