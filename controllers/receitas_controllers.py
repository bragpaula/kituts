from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import Receita, db

@login_required
def listar_receitas():
    receitas = Receita.query.filter_by(usuario_id=current_user.id).all()
    return render_template('listar_receitas.html', receitas=receitas)


@login_required
def criar_receita():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        ingredientes = request.form['ingredientes']
        modo_preparo = request.form['modo_preparo']

        nova_receita = Receita(
            titulo=titulo,
            descricao=descricao,
            ingredientes=ingredientes,
            modo_preparo=modo_preparo,
            usuario=current_user
        )
        db.session.add(nova_receita)
        db.session.commit()
        flash('Receita criada com sucesso!', 'success')
        return redirect(url_for('listar_receitas'))

    return render_template('criar_receita.html')


@login_required
def editar_receita(id):
    receita = Receita.query.get_or_404(id)
    if receita.usuario != current_user:
        flash('Você não tem permissão para editar essa receita.', 'danger')
        return redirect(url_for('listar_receitas'))

    if request.method == 'POST':
        receita.titulo = request.form['titulo']
        receita.descricao = request.form['descricao']
        receita.ingredientes = request.form['ingredientes']
        receita.modo_preparo = request.form['modo_preparo']
        db.session.commit()
        flash('Receita atualizada com sucesso!', 'success')
        return redirect(url_for('listar_receitas'))

    return render_template('editar_receita.html', receita=receita)


@login_required
def excluir_receita(id):
    receita = Receita.query.get_or_404(id)
    if receita.usuario != current_user:
        flash('Você não tem permissão para excluir essa receita.', 'danger')
        return redirect(url_for('listar_receitas'))

    db.session.delete(receita)
    db.session.commit()
    flash('Receita excluída com sucesso!', 'success')
    return redirect(url_for('listar_receitas'))
