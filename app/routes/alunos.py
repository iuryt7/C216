from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db, Aluno, CursoCounter, CURSOS_VALIDOS
from schemas.aluno import AlunoCreate, AlunoUpdate

router = APIRouter(prefix="/api/v1/alunos", tags=["Alunos"])


def _gerar_id(db: Session, curso: str) -> tuple[str, int]:
    counter = db.get(CursoCounter, curso)
    if not counter:
        counter = CursoCounter(curso=curso, contador=0)
        db.add(counter)
    counter.contador += 1
    db.flush()
    return f"{curso}{counter.contador}", counter.contador


def _aluno_para_dict(aluno: Aluno) -> dict:
    return {
        "id": aluno.id,
        "nome": aluno.nome,
        "email": aluno.email,
        "curso": aluno.curso,
        "matricula": aluno.matricula,
    }


@router.post("/", status_code=201, summary="Cadastra um novo aluno")
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    curso = aluno.curso.upper()
    if curso not in CURSOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Curso inválido")
    aluno_id, matricula = _gerar_id(db, curso)
    novo = Aluno(id=aluno_id, nome=aluno.nome, email=aluno.email, curso=curso, matricula=matricula)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return _aluno_para_dict(novo)


@router.get("/", summary="Lista todos os alunos")
def listar_alunos(db: Session = Depends(get_db)):
    return [_aluno_para_dict(a) for a in db.query(Aluno).all()]


@router.delete("/", summary="Reseta a lista de alunos")
def resetar_alunos(db: Session = Depends(get_db)):
    db.query(Aluno).delete()
    db.query(CursoCounter).delete()
    db.commit()
    return {"message": "Lista de alunos resetada"}


@router.get("/{aluno_id}", summary="Busca um aluno pelo ID")
def buscar_aluno(aluno_id: str, db: Session = Depends(get_db)):
    aluno = db.get(Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return _aluno_para_dict(aluno)


@router.patch("/{aluno_id}", summary="Atualiza dados de um aluno")
def atualizar_aluno(aluno_id: str, dados: AlunoUpdate, db: Session = Depends(get_db)):
    aluno = db.get(Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    if dados.nome is not None:
        aluno.nome = dados.nome
    if dados.email is not None:
        aluno.email = dados.email
    if dados.curso is not None:
        curso = dados.curso.upper()
        if curso not in CURSOS_VALIDOS:
            raise HTTPException(status_code=400, detail="Curso inválido")
        aluno.curso = curso
    db.commit()
    db.refresh(aluno)
    return _aluno_para_dict(aluno)


@router.delete("/{aluno_id}", summary="Remove um aluno pelo ID")
def remover_aluno(aluno_id: str, db: Session = Depends(get_db)):
    aluno = db.get(Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(aluno)
    db.commit()
    return {"message": f"Aluno {aluno_id} removido com sucesso"}
