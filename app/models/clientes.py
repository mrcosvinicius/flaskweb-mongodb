from typing import Optional

from pydantic import BaseModel


class Cliente(BaseModel):
    nome: str
    email: Optional[str] = None
    telefone: str
    endereco: str
    saldo: float
