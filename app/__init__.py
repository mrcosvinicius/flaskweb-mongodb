from flask import Flask
from pymongo import MongoClient

db = None


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    global db

    try:
        client = MongoClient(app.config["MONGO_URI"])
        db = client.get_default_database()
        print("Conexão com o MongoDB estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro na conexão com o banco de dados: {e}")

    from .routes.main import main_bp
    from .routes.usuario_routes import usuarios_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(usuarios_bp)

    return app
