#importa as bibliotecas necessarias
from flask import Flask, jsonify, request
from config.db_config import db_manager
from config.email_confg import mail, init_mail
from services.agendar_service import AgendarService
from services.cliente_service import ClienteService
from services.editora_service import EditoraService
from services.livros_service import LivrosService
from services.autor_service import AutorService
from services.emprestimos_service import EmprestimoService
from repositories.clientes_repository import ClienteRepository
from repositories.editora_repository import EditoraRepository
from repositories.livros_repository import LivrosRepository
from repositories.autor_repository import AutorRepository
from repositories.emprestimos_repository import EmprestimoRepository
import logging
import atexit

#Configura o sistema de logging da aplicação
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('biblioteca.log'),
            logging.StreamHandler()
        ]
    )

setup_logging()

#cria a aplicação flask
app= Flask(__name__)#configura o banco de dados
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///biblioteca.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

# Inicializa extensões
db_manager.init_app(app)
init_mail(app)

#inicializa os services e os repositorys
cliente_repo= ClienteRepository()
cliente_service= ClienteService(cliente_repo)

editora_repo= EditoraRepository()
editora_service= EditoraService(editora_repo)

livros_repo= LivrosRepository()
livros_service= LivrosService(livros_repo)

autor_repo= AutorRepository()
autor_service= AutorService(autor_repo)

emprestimo_repo= EmprestimoRepository()
emprestimo_service= EmprestimoService(emprestimo_repo)

agendar_service= AgendarService(mail, app)

#rotas de autores
@app.route("/autores", methods=["GET"])
def listar_autores():
    autores= autor_service.obter_todos_autores()
    return jsonify(autores)

@app.route("/autores/<int:autor_id>", methods=["GET"])
def buscar_autor(autor_id):
    autor= autor_service.obter_autor_por_id(autor_id)
    if not autor:
        return jsonify({"message": "Autor não encontrado"})
    return jsonify(autor)

@app.route("/autores", methods=["POST"])
def criar_autor():
    dados= request.json
    if not dados:
        return jsonify({"message":"Dados invalidos"})
    
    required=["nome", "nacionalidade"]
    if not all(campos in dados for campos in required):
        return jsonify({"message":"Campos obrigatorios faltando"})
    
    autor= autor_service.criar_autor(dados)
    return jsonify(autor)

@app.route("/autores/<int:autor_id>", methods=["PUT"])
def atualizar_autor(autor_id):
    dados= request.json
    if not dados:
        return jsonify({"message":"dados invalidos"})
    autor= autor_service.atualizar_autor(autor_id,dados)
    if not autor:
        return jsonify({"message":"Autor não encontrado"})
    return jsonify(autor)

@app.route("/autores/<int:autor_id>", methods=["DELETE"])
def deletar_autor(autor_id):
    if autor_service.deletar_autor(autor_id):
        return jsonify({"message":"Autor deletado com sucesso"})
    return jsonify({"message":"Autor não encontrado"})

#rotas das editoras
@app.route("/editoras", methods=["GET"])
def listar_editoras():
    editoras= editora_service.obter_todas_editoras()
    return jsonify(editoras)

@app.route("/editoras/<int:editora_id>",methods=["GET"])
def buscar_editora(editora_id):
    editoras= editora_service.obter_editora_por_id(editora_id)
    if not editoras:
        return jsonify({"message":"Editora não encontrada"})
    return jsonify(editoras)

@app.route("/editoras", methods=["POST"])
def criar_editora():
    dados= request.json
    if not dados:
        return jsonify({"message":"Dados invalidos"})
    required=["nome","pais"]
    if not all(campos in dados for campos in required):
        return jsonify({"message":"Campos obrigatorios faltando"})
     
    editoras= editora_service.criar_editora(dados)
    return jsonify(editoras)

@app.route("/editoras/<int:editora_id>", methods=["PUT"])
def atualizar_editora(editora_id):
    dados= request.json
    if not dados:
        return jsonify({"message":"Dados invalidos"})
    editora= editora_service.atualizar_editora(editora_id,dados)
    if not editora:
        return jsonify({"message":"Editora não encontrada"})
    return jsonify(editora)

@app.route("/editoras/<int:editora_id>", methods=["DELETE"])
def deletar_editora(editora_id):
    if editora_service.deletar_editora(editora_id):
        return jsonify({"message":"Editora deletada com sucesso"})
    return jsonify({"message":"Editora não encontrada"})

#rota dos clientes
@app.route("/cliente", methods=["GET"])
def listar_clientes():
    clientes= cliente_service.obter_todos_clientes()
    return jsonify(clientes)

@app.route("/cliente/<int:cliente_id>", methods=["GET"])
def buscar_cliente(cliente_id):
    cliente= cliente_service.obter_cliente_por_id(cliente_id)
    if not cliente:
        return jsonify({"message":"Cliente não encontrado"})
    return jsonify(cliente)

@app.route("/cliente", methods=["POST"])
def criar_cliente():
    dados= request.json
    if not dados:
        return jsonify({"message":"Dados invalidos"})
    required=["nome","email","CPF"]
    if not all(campos in dados for campos in required):
        return jsonify({"message":"Campos obrigatorios faltando"})
    
    clientes=cliente_service.criar_cliente(dados)
    return jsonify(clientes)

@app.route("/cliente/<int:cliente_id>", methods=["PUT"])
def atualizar_cliente(cliente_id):
    dados= request.json
    if not dados:
        return jsonify({"message":"Dados invalidos"})
    cliente= cliente_service.atualizar_cliente(cliente_id, dados)
    if not cliente:
        return jsonify({"message":"Cliente não encontrado"})
    return jsonify(cliente)

@app.route("/cliente/<int:cliente_id>", methods=["DELETE"])
def deletar_cliente(cliente_id):
    if cliente_service.deletar_cliente(cliente_id):
        return jsonify({"message":"Cliente deletado com sucesso"})
    return jsonify({"message":"Cliente não encontrado"})

#rotas dos livros
@app.route("/livros", methods=["GET"])
def listar_livros():
    livros= livros_service.obter_todos_livros()
    return jsonify(livros)

@app.route("/livros/<int:livro_id>", methods=["GET"])
def listar_por_id(livro_id):
    livro= livros_service.obter_por_id(livro_id)
    if not livro:
        return jsonify({"message":"Livro não encontrado"})
    return jsonify(livro)

@app.route("/livros", methods=["POST"])
def criar_livro():
    dados= request.json
    if not dados:
        return jsonify({"message":"Dados invalidos"})
    required=["titulo","autor_id","editora_id","genero","Quantidade_paginas","Quantidade_disponivel"]
    if not all(campos in dados for campos in required):
        return jsonify({"message":"Campos obrigatorios faltando"})
    livro= livros_service.criar_livro(dados)
    return jsonify(livro)

@app.route("/livros/<int:livro_id>", methods=["PUT"])
def atualizar_livro(livro_id):
    dados= request.json
    if not dados:
        return jsonify({"message":"Dados invalidos"})
    livro= livros_service.atualizar_livro(livro_id,dados)
    if not livro:
        return jsonify({"message":"Livro não encontrado"})
    return jsonify(livro)

@app.route("/livros/<int:livro_id>", methods=["DELETE"])
def deletar_livro(livro_id):
    if livros_service.deletar_livro(livro_id):
        return jsonify({"message":"Livro deletado com sucesso"})
    return jsonify({"message":"Livro não encontrado"})

#rotas dos emprestimos
@app.route("/emprestimos", methods=["GET"])
def listar_todos():
    emprestimos= emprestimo_service.obter_todos_emprestimos()
    return jsonify(emprestimos)

@app.route("/emprestimos/<int:emprestimo_id>", methods=["GET"])
def emprestimo_por_id(emprestimo_id):
    emprestimo= emprestimo_service.obter_por_id(emprestimo_id)
    if not emprestimo:
        return jsonify({"message":"Empréstimo não encontrado"})
    return jsonify(emprestimo)

@app.route("/emprestimos/cliente/<int:cliente_id>", methods=["GET"])
def emprestimo_por_cliente(cliente_id):
    emprestimos= emprestimo_service.listar_por_cliente(cliente_id)
    return jsonify(emprestimos)

@app.route("/emprestimos/livro/<int:livro_id>", methods=["GET"])
def emprestimo_por_livro(livro_id):
    emprestimo= emprestimo_service.lista_por_livro(livro_id)
    return jsonify(emprestimo)

@app.route("/emprestimos/ativos", methods=["GET"])
def listar_ativos():
    emprestimos= emprestimo_service.listar_emprestimos_ativos()
    return jsonify(emprestimos)

@app.route("/emprestimos/atrasados", methods=["GET"])
def listar_atrasados():
    emprestimos= emprestimo_service.listar_emprestimos_vencidos()
    return jsonify(emprestimos)

@app.route("/emprestimos", methods=["POST"])
def criar_emprestimo():
    dados=request.json
    if not dados:
        return jsonify({"message":"Dados invalidos"})
    required=["data_emprestimo", "data_devolucao"]
    if not all(campos in dados for campos in required):
        return jsonify({"message":"campos faltando"})
    emprestimo= emprestimo_service.criar_emprestimo(dados)
    return jsonify(emprestimo)

@app.route("/emprestimos/<int:emprestimo_id>", methods=["PUT"])
def atualizar_emprestimo(emprestimo_id):
    dados= request.json
    if not dados:
        return jsonify({"message":"Dados invalidos"})
    emprestimo= emprestimo_service.atualizar_emprestimo(emprestimo_id, dados)
    if not emprestimo:
        return jsonify({"message":"mensagem não encontrada"})
    return jsonify(emprestimo)

@app.route("/emprestimos/<int:emprestimo_id>", methods=["DELETE"])
def deletar_eprestimo(emprestimo_id):
    if emprestimo_service.deletar_emprestimo(emprestimo_id):
        return jsonify({"message":"emprestimo deletado"})
    return jsonify({"message":"emprestimo não econtrado"})

@app.route("/emprestimos/<int:emprestimo_id>/finalizar", methods=["POST"])
def finalizar_emprestimo(emprestimo_id):
    if not emprestimo_service.finalizar_emprestimo(emprestimo_id):
        return jsonify({"message":"emprestimo não encontrado"})
    return jsonify({"message":"emprestimo finalizado com sucesso"})

@app.route("/clientes/<int:cliente_id>/bloquear", methods=["POST"])
def bloquar_cliente(cliente_id):
    if not emprestimo_service.bloquear_cliente(cliente_id):
        return jsonify({"message":"cliente não encontrado"})
    return jsonify({"message":"cliente bloqueado"})

@app.route("/clientes/<int:cliente_id>/desbloquear", methods=["POST"])
def desbloquear_cliente(cliente_id):
    if not emprestimo_service.desbloquear_cliente(cliente_id):
        return jsonify({"message":"cliente não encontrado"})
    return jsonify({"message":"cliente desbloqueado"})

#gerenciados de serviçoes em segundo plano

servico_iniciado= False # Controle global para serviços agendados

#Inicia serviços automáticos antes da primeira requisição
@app.before_request
def iniciar_servicos():
    global servico_iniciado
    if not servico_iniciado:
        agendar_service.iniciar_agendamentos()
        servico_iniciado= True

#Para os serviços agendados quando a aplicação é encerrada
def parar_servico():
        agendar_service.parar_agendamento() 

# Registra a função de parada para execução quando a aplicação terminar
atexit.register(parar_servico)

if __name__=="__main__":
    with app.app_context():
        db_manager.db.create_all()
    app.run(debug=True, use_reloader=False)