import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import json
import hashlib
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Функция для хеширования пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Функция для загрузки пользователей из файла JSON
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Функция для сохранения пользователей в файл JSON
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        if username in users:
            return render_template('register.html', error='Пользователь уже существует')

        users[username] = {
            'password': hash_password(password),
            'date_registered': str(datetime.datetime.now())
        }
        save_users(users)

        session['username'] = username
        return redirect(url_for('dashboard'))

    return render_template('register.html')

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        if username not in users:
            return render_template('login.html', error='Пользователь не  найден')

        if users[username]['password'] == hash_password(password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='В пароле ошибка!')

    return render_template('login.html')

# Личный кабинет
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        users = load_users()
        date_registered = users[username]['date_registered']
        return render_template('dashboard.html', username=username, date_registered=date_registered)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    context = ('ssl_cert/cert.pem', 'ssl_cert/key.pem')
    app.run(debug=True, ssl_context = context)
