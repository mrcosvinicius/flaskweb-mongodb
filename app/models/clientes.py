from typing import Any, Callable, Literal, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class Cliente(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    nome: str
    email: Optional[str] = None
    telefone: str
    endereco: str
    saldo: float

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


class ClienteDBModel(Cliente):
    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: Any | None = None,
        exclude: Any | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_computed_fields: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        fallback: Callable[[Any], Any] | None = None,
        serialize_as_any: bool = False,
        polymorphic_serialization: bool | None = None,
    ) -> dict[str, Any]:
        data = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            exclude_computed_fields=exclude_computed_fields,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
            polymorphic_serialization=polymorphic_serialization,
        )
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return data


class AtualizaCliente(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    saldo: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
