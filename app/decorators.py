from functools import wraps

import jwt
from flask import current_app, jsonify, request


def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"error": "Token de autenticação mal formatado"}), 401
        if not token:
            return jsonify({"error": "Token de autenticação não encontrado"}), 401

        try:
            dados = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token de autenticação expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token de autenticação inválido"}), 401

        return f(dados, *args, **kwargs)

    return decorated
