import re
from flask import render_template, request, redirect, url_for, session as flask_session
from main import app
from database import session as db_session, User
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

# ========== DECORADOR DE PROTEÇÃO ==========
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in flask_session:
            return redirect(url_for('register') + '?error=Faça login para acessar.')
        return f(*args, **kwargs)
    return decorated_function

# ========== VALIDAÇÃO DE SENHA FORTE ==========
def is_strong_password(password):
    if len(password) < 8:
        return False
    
    # Precisa ter pelo menos um: letra maiúscula, número ou símbolo
    has_upper = re.search(r'[A-Z]', password)
    has_digit = re.search(r'\d', password)
    has_symbol = re.search(r'[@$!%*?&]', password)

    return bool(has_upper or has_digit or has_symbol)

# ========== ROTAS PÚBLICAS ==========
@app.route('/')
def loaderpage():
    return render_template("loader.html")

@app.route('/info')
def infopage():
    return render_template("home.html")

@app.route('/contact')
def contactpage():
    return render_template("home.html")

@app.route('/home')
def homepage():
    return render_template("home.html")

# ========== ROTAS PROTEGIDAS ==========
@app.route('/UserDashboard')
@login_required
def dashpage():
    return render_template("dashboard.html")

@app.route('/dashboard/profile')
@login_required
def profilepage():
    return render_template("dashboard/profile.html")

@app.route('/dashboard/receipts')
@login_required
def receiptspage():
    return render_template("dashboard/receipts.html")

# ========== REGISTRO ==========
@app.route('/user', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not is_strong_password(password):
            return redirect(url_for('register') + '?error=Senha fraca. Use 8+ caracteres com maiúsculas, números ou símbolos.')

        existing_user = db_session.query(User).filter_by(email=email).first()
        if existing_user:
            return redirect(url_for('register') + '?error=Email já em uso.')

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()

        return redirect(url_for('register') + '?registered=true')

    return render_template("user.html")

# ========== LOGIN ==========
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = db_session.query(User).filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        flask_session['user_id'] = user.id  # SALVAR LOGIN NA SESSÃO
        return redirect(url_for('dashpage') + '?login=success')
    else:
        return redirect(url_for('register') + '?error=Credenciais inválidas.')

# ========== LOGOUT ==========
@app.route('/logout')
def logout():
    flask_session.pop('user_id', None)
    return redirect(url_for('register') + '?logout=success')

# ========== ATUALIZAÇÃO DE CREDENCIAIS ==========
# ========== ATUALIZAÇÃO DE CREDENCIAIS ==========  
@app.route('/update_credentials', methods=['GET', 'POST'])
@login_required
def update_credentials():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_id = flask_session.get('user_id')
        user = db_session.query(User).filter_by(id=user_id).first()

        if user:
            if email and user.email != email:
                existing_user = db_session.query(User).filter_by(email=email).first()
                if existing_user:
                    return redirect(url_for('dashpage') + '?error=Email já em uso.')
                user.old_email = user.email
                user.email = email

            if password:
                if not is_strong_password(password):
                    return redirect(url_for('dashpage') + '?error=Senha fraca. Use 8+ caracteres com maiúsculas, números ou símbolos.')
                user.password = generate_password_hash(password)

            db_session.commit()
            return redirect(url_for('dashpage') + '?updated=true')
        else:
            return redirect(url_for('dashpage') + '?error=user_not_found')
    else:
        # Se a rota for acessada via GET, redireciona para o perfil
        return redirect(url_for('profilepage'))
