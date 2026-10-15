from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-me'
users = {}


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
        elif username in users:
            error = 'Пользователь с таким логином уже существует'

        if error:
            return render_template('index.html', error=error)
        users[username] = {'email': email, 'password': password}
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
        if username not in users:
            error = 'Пользователь не найден'
        elif users[username]['password'] != password:
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


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True) 