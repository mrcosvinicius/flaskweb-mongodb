from pydantic import BaseModel, Field


class Usuario(BaseModel):
    nome: str
    senha: str


class UsuarioResposta(BaseModel):
    id: str = Field(alias="_id")
    nome: str
