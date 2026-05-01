from bson import ObjectId
from flask import Blueprint, jsonify, request

from app import db
from app.models.usuarios import Usuario, UsuarioResposta

usuarios_bp = Blueprint("usuarios_bp", __name__)


@usuarios_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    todos_usuarios = db.usuarios.find({}, {"senha": 0})
    lista_usuarios = []

    for usuario in todos_usuarios:
        usuario["_id"] = str(usuario["_id"])
        lista_usuarios.append(
            UsuarioResposta(**usuario).model_dump(by_alias=True, exclude_none=True)
        )

    return jsonify(lista_usuarios)


@usuarios_bp.route("/usuarios/<string:usuario_id>", methods=["GET"])
def vizualizar_usuario(usuario_id):
    try:
        uid = ObjectId(usuario_id)
    except Exception as e:
        return jsonify({"error": "ID de usuário inválido", "details": str(e)}), 400

    usuario_buscado = db.usuarios.find_one({"_id": uid}, {"senha": 0})
    if not usuario_buscado:
        return jsonify({"error": "Usuário não encontrado"}), 404
    else:
        if "_id" in usuario_buscado:
            usuario_buscado["_id"] = str(usuario_buscado["_id"])
        usuario_model = UsuarioResposta(**usuario_buscado).model_dump(
            by_alias=True, exclude_none=True
        )
        return jsonify(usuario_model)


@usuarios_bp.route("/usuarios", methods=["POST"])
def criar_usuario():
    dados = request.get_json()
    try:
        novo_usuario = Usuario(**dados)
        resultado = db.usuarios.insert_one(
            novo_usuario.model_dump(by_alias=True, exclude_none=True)
        )
        return jsonify(
            {"message": "Usuário criado com sucesso", "id": str(resultado.inserted_id)}
        ), 201
    except Exception as e:
        return jsonify({"error": "Erro ao criar usuário", "details": str(e)}), 500


@usuarios_bp.route("/usuarios/<string:usuario_id>", methods=["DELETE"])
def deletar_usuario(usuario_id):
    try:
        resultado = db.usuarios.delete_one({"_id": usuario_id})
        if resultado.deleted_count == 0:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify({"message": "Usuário deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": "Erro ao deletar usuário", "details": str(e)}), 500
