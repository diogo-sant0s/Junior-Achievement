from flask import render_template, request, redirect, url_for
from main import app
from database import session, User  # Ajustei 'user' para 'User' conforme classe

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

@app.route('/UserDashboard')
def dashpage():
    return render_template("dashboard.html")

@app.route('/register', methods=['GET'])
def registerpage():
    return render_template("user.html")

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    # Checar se já existe email cadastrado (exemplo simples)
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        # Você pode melhorar retornando uma mensagem de erro na página
        return redirect(url_for('registerpage') + '?error=email_exists')

    new_user = User(name=name, email=email, password=password)
    session.add(new_user)
    session.commit()

    # Redirecionar para a página de login/registro com sucesso
    return redirect(url_for('registerpage') + '?success=true')
