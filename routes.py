from main import app
from controllers.receitas_controllers import (
    listar_receitas, criar_receita, editar_receita, excluir_receita
)

#rotas
app.add_url_rule('/receitas', 'listar_receitas', listar_receitas)
app.add_url_rule('/receitas/criar', 'criar_receita', criar_receita, methods=['GET','POST'])
app.add_url_rule('/receitas/editar/<int:id>', 'editar_receita', editar_receita, methods=['GET','POST'])
app.add_url_rule('/receitas/excluir/<int:id>', 'excluir_receita', excluir_receita, methods=['POST'])
