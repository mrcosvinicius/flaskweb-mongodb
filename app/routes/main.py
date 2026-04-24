from flask import Blueprint, jsonify

main_bp = Blueprint("main_bp", __name__)


# rf: o sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route("/login", methods=["POST"])
def login():
    return jsonify({"message": "Tela de login"})


# rf: o sistema deve permitir listagem de todos os clientes
@main_bp.route("/clientes", methods=["GET"])
def listar_clientes():
    return jsonify({"message": "Rota para listagem de clientes"})


# rf: o sistema deve permitir a criacao de um novo cliente
@main_bp.route("/clientes", methods=["POST"])
def criar_cliente():
    return jsonify({"message": "Rota para criar um novo cliente"})


# rf: o sistema deve permitir a visualizacao dos detalhes de um unico cliente
@main_bp.route("/clientes/<int:cliente_id>", methods=["GET"])
def visualizar_cliente(cliente_id):
    return jsonify(
        {"message": f"Rota para visualizar detalhes do cliente {cliente_id}"}
    )


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
