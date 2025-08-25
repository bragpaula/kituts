from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.models import Usuario
from controllers.receitas_controllers import (
    listar_receitas, criar_receita, editar_receita, excluir_receita
)
from db import db
import hashlib

app = Flask(__name__)
app.secret_key = 'jepale'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///kituts.db"
db.init_app(app)

# Login Manager
lm = LoginManager(app)
lm.login_view = 'login'

def hash(txt):
    return hashlib.sha256(txt.encode('utf-8')).hexdigest()


@lm.user_loader
def user_loader(id):
    return Usuario.query.get(int(id))

#rotas
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form['emailForm']
    senha = request.form['senhaForm']
    user = Usuario.query.filter_by(email=email, senha=hash(senha)).first()
    if not user:
        return 'Usuario ou senha incorretos'
    login_user(user)
    return redirect(url_for('dashboard'))


@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')

    nome = request.form['nameForm']
    email = request.form['emailForm']
    senha = request.form['senhaForm']

    novo_usuario = Usuario(nome=nome, email=email, senha=hash(senha))
    db.session.add(novo_usuario)
    db.session.commit()


    return redirect(url_for('login'))



@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

import routes

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
