from datetime import datetime, timedelta, timezone

import jwt
from bson import ObjectId
from flask import Blueprint, current_app, jsonify, request
from pydantic import ValidationError

from app import db
from app.decorators import token_obrigatorio
from app.models.clientes import AtualizaCliente, Cliente, ClienteDBModel
from app.models.usuarios import Usuario

main_bp = Blueprint("main_bp", __name__)


# rf: o sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route("/login", methods=["POST"])
def login():
    try:
        dados = request.get_json()
        dados_usuarios = Usuario(**dados)

    except ValidationError as e:
        return jsonify(
            {"error": "Dados de login inválidos", "details": e.errors()}
        ), 400
    except Exception as e:
        return jsonify(
            {"error": "Erro ao processar a solicitação", "details": str(e)}
        ), 500
    if (
        dados_usuarios.nome == "admin"
        and dados_usuarios.senha == current_app.config["SECRET_KEY"]
    ):
        token = jwt.encode(
            {
                "user_id": dados_usuarios.nome,
                "exp": datetime.now(timezone.utc) + timedelta(hours=2),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"token de acesso": token}), 200

    return jsonify({"error": "Credenciais inválidas"}), 401


# rf: o sistema deve permitir listagem de todos os clientes
@main_bp.route("/clientes", methods=["GET"])
def listar_clientes():
    todos_clientes = db.clientes.find({})
    clientes_list = [
        ClienteDBModel(**cliente).model_dump(by_alias=True, exclude_none=True)
        for cliente in todos_clientes
    ]

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
        cliente_model = ClienteDBModel(**cliente).model_dump(
            by_alias=True, exclude_none=True
        )
        return jsonify(cliente_model)
    else:
        return jsonify({"error": "Cliente não encontrado"}), 404


# rf: o sistema deve permitir a criacao de um novo cliente
@main_bp.route("/clientes", methods=["POST"])
@token_obrigatorio
def criar_cliente(token_dados):
    try:
        cliente = Cliente(**request.get_json())
    except ValidationError as e:
        return jsonify(
            {"error": "Dados de cliente inválidos", "details": e.errors()}
        ), 400
    except Exception as e:
        return jsonify(
            {"error": "Erro ao processar a solicitação", "details": str(e)}
        ), 500
    db.clientes.insert_one(cliente.model_dump(by_alias=True, exclude_none=True))
    return jsonify({"message": f"Cliente {cliente.nome} criado com sucesso!"}), 201


# rf: o sistema deve permitir a atualizacao de um unico cliente e cliente existente
@main_bp.route("/clientes/<string:cliente_id>", methods=["PUT"])
@token_obrigatorio
def atualizar_cliente(token_dados, cliente_id):
    try:
        uid = ObjectId(cliente_id)
        dados_atualizado = AtualizaCliente(**request.get_json())

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 500

    resultado_atualizado = db.clientes.update_one(
        {"_id": uid},
        {"$set": dados_atualizado.model_dump(exclude_unset=True)},
    )

    if resultado_atualizado.matched_count == 0:
        return jsonify({"error": "Cliente não encontrado"}), 404

    cliente_atualizado = db.clientes.find_one({"_id": uid})

    if cliente_atualizado:
        cliente_model = ClienteDBModel(**cliente_atualizado).model_dump(
            by_alias=True, exclude_none=True
        )
        return jsonify(cliente_model)
    else:
        return jsonify({"error": "Cliente não encontrado após atualização"}), 404


# rf: o sistema deve permitir a delecao de um unico cliente e cliente existente
@main_bp.route("/clientes/<string:cliente_id>", methods=["DELETE"])
@token_obrigatorio
def deletar_cliente(token_dados, cliente_id):
    try:
        uid = ObjectId(cliente_id)
        produto_deletado = db.clientes.delete_one({"_id": uid})

        if produto_deletado.deleted_count == 0:
            return jsonify({"error": "Cliente não encontrado"}), 404

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 500

    return jsonify({"message": f"Cliente {cliente_id} deletado com sucesso!"}), 204


@main_bp.route("/", methods=["GET"])
def pagina_inicial():
    return jsonify({"message": "Bem-vindo à API de Clientes!"})
