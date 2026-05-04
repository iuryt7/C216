from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Gerenciador de Alunos",
    description=(
        "API REST para gerenciamento de alunos.\n\n"
        "**Cursos disponíveis:** GES, GEC, GET, GEP\n\n"
        "**Regras de ID:** gerado automaticamente como `CURSO + número sequencial` (ex: GES1, GEC2). "
        "IDs de alunos removidos **nunca** são reutilizados."
    ),
    version="1.0.0",
)

alunos_db: dict[str, dict] = {}
curso_counters: dict[str, int] = {}

CURSOS_VALIDOS = {"GES", "GEC", "GET", "GEP"}

TAG_ALUNOS = "Alunos"


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


def gerar_id(curso: str) -> str:
    curso_counters[curso] = curso_counters.get(curso, 0) + 1
    return f"{curso}{curso_counters[curso]}"


@app.post("/api/v1/alunos/", status_code=201, tags=[TAG_ALUNOS], summary="Cadastra um novo aluno")
def criar_aluno(aluno: AlunoCreate):
    curso = aluno.curso.upper()
    if curso not in CURSOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Curso inválido")
    aluno_id = gerar_id(curso)
    matricula = curso_counters[curso]
    alunos_db[aluno_id] = {
        "id": aluno_id,
        "nome": aluno.nome,
        "email": aluno.email,
        "curso": curso,
        "matricula": matricula,
    }
    return alunos_db[aluno_id]


@app.get("/api/v1/alunos/", tags=[TAG_ALUNOS], summary="Lista todos os alunos")
def listar_alunos():
    return list(alunos_db.values())


@app.delete("/api/v1/alunos/", tags=[TAG_ALUNOS], summary="Reseta a lista de alunos")
def resetar_alunos():
    alunos_db.clear()
    curso_counters.clear()
    return {"message": "Lista de alunos resetada"}


@app.get("/api/v1/alunos/{aluno_id}", tags=[TAG_ALUNOS], summary="Busca um aluno pelo ID")
def buscar_aluno(aluno_id: str):
    aluno = alunos_db.get(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


@app.patch("/api/v1/alunos/{aluno_id}", tags=[TAG_ALUNOS], summary="Atualiza dados de um aluno")
def atualizar_aluno(aluno_id: str, dados: AlunoUpdate):
    aluno = alunos_db.get(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    if dados.nome is not None:
        aluno["nome"] = dados.nome
    if dados.email is not None:
        aluno["email"] = dados.email
    if dados.curso is not None:
        curso = dados.curso.upper()
        if curso not in CURSOS_VALIDOS:
            raise HTTPException(status_code=400, detail="Curso inválido")
        aluno["curso"] = curso
    return aluno


@app.delete("/api/v1/alunos/{aluno_id}", tags=[TAG_ALUNOS], summary="Remove um aluno pelo ID")
def remover_aluno(aluno_id: str):
    aluno = alunos_db.pop(aluno_id, None)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"message": f"Aluno {aluno_id} removido com sucesso"}
