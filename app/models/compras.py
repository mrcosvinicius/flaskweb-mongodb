from pydantic import BaseModel


class Compra(BaseModel):
    produto: str
    quantidade: int
    preco_unitario: float
