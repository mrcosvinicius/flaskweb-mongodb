from pydantic import BaseModel


class LoginUsuario(BaseModel):
    nome: str
    senha: str
