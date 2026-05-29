from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import criar_tabelas
from middleware.logging_middleware import log_requests
from middleware.custom_header_middleware import add_custom_headers
from routes.alunos import router as alunos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()
    yield


app = FastAPI(
    title="Gerenciador de Alunos",
    description=(
        "API REST para gerenciamento de alunos.\n\n"
        "**Cursos disponíveis:** GES, GEC, GET, GEP\n\n"
        "**Regras de ID:** gerado automaticamente como `CURSO + número sequencial` (ex: GES1, GEC2). "
        "IDs de alunos removidos **nunca** são reutilizados."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.middleware("http")(log_requests)
app.middleware("http")(add_custom_headers)

app.include_router(alunos_router)
