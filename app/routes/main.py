from bson import ObjectId
from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app import db
from app.models.usuarios import LoginUsuario

main_bp = Blueprint("main_bp", __name__)


# rf: o sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route("/login", methods=["POST"])
def login():
    try:
        dados = request.get_json()
        dados_usuarios = LoginUsuario(**dados)

    except ValidationError as e:
        return jsonify(
            {"error": "Dados de login inválidos", "details": e.errors()}
        ), 400
    except Exception as e:
        return jsonify(
            {"error": "Erro ao processar a solicitação", "details": str(e)}
        ), 500
    if dados_usuarios.nome == "admin" and dados_usuarios.senha == "admin":
        return jsonify(
            {"message": f"Usuario {dados_usuarios.nome} autenticado com sucesso!"}
        )
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401


# rf: o sistema deve permitir listagem de todos os clientes
@main_bp.route("/clientes", methods=["GET"])
def listar_clientes():
    todos_clientes = db.clientes.find({})
    clientes_list = []

    for cliente in todos_clientes:
        cliente["_id"] = str(cliente["_id"])
        clientes_list.append(cliente)

    return jsonify(clientes_list)


# rf: o sistema deve permitir a visualizacao dos detalhes de um unico cliente
@main_bp.route("/clientes/<string:cliente_id>", methods=["GET"])
def visualizar_cliente(cliente_id):
    try:
        uid = ObjectId(cliente_id)
    except Exception as e:
        return jsonify({"error": "Erro ao buscar cliente", "details": str(e)}), 500

    cliente = db.clientes.find_one({"_id": uid})
    if cliente:
        cliente["_id"] = str(cliente["_id"])
        return jsonify(cliente)
    else:
        return jsonify({"error": "Cliente não encontrado"}), 404


# rf: o sistema deve permitir a criacao de um novo cliente
@main_bp.route("/clientes", methods=["POST"])
def criar_cliente():
    return jsonify({"message": "Rota para criar um novo cliente"})


# rf: o sistema deve permitir a atualizacao de um unico cliente e cliente existente
@main_bp.route("/clientes/<int:cliente_id>", methods=["PUT"])
def atualizar_cliente(cliente_id):
    return jsonify({"message": f"Rota para atualizar o cliente {cliente_id}"})


# rf: o sistema deve permitir a delecao de um unico cliente e cliente existente
@main_bp.route("/clientes/<int:cliente_id>", methods=["DELETE"])
def deletar_cliente(cliente_id):
    return jsonify({"message": f"Rota para deletar o cliente {cliente_id}"})


# rf: o sistema deve permitir a importacao de compras através de um arquivo
@main_bp.route("/importar-compras", methods=["POST"])
def importar_compras():
    return jsonify({"message": "Rota para importar compras através de um arquivo"})


@main_bp.route("/", methods=["GET"])
def pagina_inicial():
    return jsonify({"message": "Bem-vindo à API de Clientes!"})
