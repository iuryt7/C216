from pydantic import BaseModel
from typing import Optional


class AlunoCreate(BaseModel):
    nome: str
    email: str
    curso: str

    model_config = {
        "json_schema_extra": {
            "example": {"nome": "Ana Silva", "email": "ana@email.com", "curso": "GES"}
        }
    }


class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    curso: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {"nome": "Ana Paula Silva", "email": "anapaula@email.com"}
        }
    }
