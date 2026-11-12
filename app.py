import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import webbrowser
from threading import Timer
import secrets
import os
import urllib.request
from urllib.parse import urlparse

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
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        user = conn.execute(query, (username, password)).fetchone()
        conn.close()

        if not user:
            error = 'Неверный логин или пароль'
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


@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        token_from_form = request.form.get('csrf_token')
        token_from_session = session.get('csrf_token')
        
        if not token_from_form or token_from_form != token_from_session:
            return "Ошибка CSRF: Недействительный токен!", 403

        new_password = request.form.get('new_password')
        if new_password:
            conn = get_db_connection()
            conn.execute(
                'UPDATE users SET password = ? WHERE username = ?',
                (new_password, session['username'])
            )
            conn.commit()
            conn.close()
            return "Пароль успешно изменен! <a href='/chat'>Вернуться в чат</a>"
            
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
        
    return render_template('change_password.html', csrf_token=session['csrf_token'])


@app.route('/fetch-avatar', methods=['GET', 'POST'])
def fetch_avatar():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            try:
                parsed_url = urlparse(url)
                
                if parsed_url.scheme not in ('http', 'https'):
                    return "Ошибка: Разрешен только протокол HTTP/HTTPS (защита от file://)", 400
                
                if parsed_url.hostname in ('127.0.0.1', 'localhost', '0.0.0.0'):
                    return "Ошибка: Запросы к локальному серверу запрещены (защита от SSRF)", 400

                with urllib.request.urlopen(url) as response:
                    content = response.read()
                
                if url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    filepath = os.path.join('static', 'img', 'avatar.jpg')
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    return f'<h1>Успешно!</h1><img src="/static/img/avatar.jpg" style="max-width: 300px;"><br><a href="/chat">Назад в чат</a>'
                
                else:
                    return f"<h1>Успешно! Вот что скачал сервер:</h1><pre>{content.decode('utf-8', errors='ignore')}</pre><br><a href='/chat'>Назад в чат</a>"
                    
            except Exception as e:
                return f"Ошибка: {e}"

    return """
    <form method="POST">
        <input type="text" name="url" placeholder="https://example.com/avatar.jpg" size="50">
        <button type="submit">Загрузить аватар</button>
    </form>
    """


@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
    if 'username' not in session:
        return redirect(url_for('index'))
        
    conn = get_db_connection()
    
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        amount = int(request.form.get('amount', 0))
        
        if recipient and amount:
            if amount <= 0:
                return "Ошибка: Сумма перевода должна быть больше нуля! <a href='/wallet'>Назад</a>"
            
            current_user = conn.execute('SELECT coins FROM users WHERE username = ?', (session['username'],)).fetchone()
            if current_user['coins'] < amount:
                return "Ошибка: Недостаточно монет на балансе! <a href='/wallet'>Назад</a>"

            conn.execute(
                'UPDATE users SET coins = coins - ? WHERE username = ?',
                (amount, session['username'])
            )
            conn.execute(
                'UPDATE users SET coins = coins + ? WHERE username = ?',
                (amount, recipient)
            )
            conn.commit()
            return "Перевод выполнен! <a href='/wallet'>Назад</a>"
            
    user = conn.execute('SELECT coins FROM users WHERE username = ?', (session['username'],)).fetchone()
    conn.close()
    
    return f"""
    <h1>Кошелек</h1>
    <p>Ваш баланс: {user['coins']} монет</p>
    <form method="POST">
        <input type="text" name="recipient" placeholder="Кому (логин)">
        <input type="number" name="amount" placeholder="Сумма">
        <button type="submit">Перевести</button>
    </form>
    <p><a href="/chat">Вернуться в чат</a></p>
    """


@app.route('/page')
def page():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    page_name = request.args.get('name', 'chat')
    
    allowed_pages = ['about', 'rules', 'chat']
    if page_name not in allowed_pages:
        return "Ошибка: Страница не найдена (защита от LFI)!", 404
        
    return render_template(f'{page_name}.html', username=session['username'])
@app.route('/view-file')
def view_file():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    filename = request.args.get('file', '')
    if filename:
        try:
            base_dir = os.path.realpath('static')
            filepath = os.path.realpath(os.path.join(base_dir, filename))
            
            if not filepath.startswith(base_dir):
                return "Ошибка: Доступ запрещен (защита от Directory Traversal)!", 403
            
            if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                return f'<h3>File: {filename}</h3><img src="/static/{filename}" style="max-width: 600px;"><br><a href="/chat">Назад</a>'
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return f"<h3>File: {filename}</h3><pre>{content}</pre><br><a href='/chat'>Назад</a>"
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    return "Укажите файл в параметре ?file= (например, ?file=img/fox.png)"


@app.route('/search')
def search():
    if 'username' not in session:
        return redirect(url_for('index'))

    query = request.args.get('q', '')
    
    conn = get_db_connection()
    sql = "SELECT sender, text FROM messages WHERE text LIKE ?"
    search_pattern = f"%{query}%"
    messages = conn.execute(sql, (search_pattern,)).fetchall()
    conn.close()

    return render_template('search.html', query=query, messages=messages)


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


if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        Timer(1, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(debug=True, use_reloader=True)