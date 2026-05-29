# C216 - Sistemas Distribuídos

API REST para gerenciamento de alunos, desenvolvida com FastAPI e PostgreSQL.

## Estrutura do projeto

```
C216/
├── backend/
│   ├── middleware/        # logging e custom headers
│   ├── routes/            # endpoints da API
│   ├── schemas/           # modelos Pydantic
│   ├── services/          # entry point (main.py)
│   ├── database.py        # configuração SQLAlchemy
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── templates/
│   │   ├── index.html     # listagem de alunos
│   │   ├── about.html     # informações do desenvolvedor
│   │   ├── contact.html   # informações de contato
│   │   ├── novo_aluno.html
│   │   └── editar_aluno.html
│   ├── static/
│   │   └── styles.css
│   ├── app.py             # aplicação Flask
│   ├── Dockerfile
│   └── requirements.txt
├── db/
│   └── init.sql           # criação das tabelas
├── tests/
│   └── tests.py           # testes automatizados
├── .env                   # credenciais (não commitado)
└── docker-compose.yml
```

## Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose
- Python 3.10+ (apenas para rodar os testes localmente)

## Configuração

Crie o arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=faculdade
DATABASE_URL=postgresql://postgres:sua_senha@db:5432/faculdade
```

## Como rodar o projeto

**1. Primeira execução** (cria o banco e as tabelas do zero):

```bash
docker-compose up --build
```

**2. Execuções seguintes:**

```bash
docker-compose up
```

**3. Para parar:**

```bash
docker-compose down
```

**4. Para parar e apagar os dados do banco:**

```bash
docker-compose down -v
```

| Serviço | Endereço |
|---|---|
| Frontend (Flask) | `http://localhost:5000` |
| API (FastAPI) | `http://localhost:8000` |
| Swagger (docs) | `http://localhost:8000/docs` |

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/v1/alunos/` | Cadastra um novo aluno |
| `GET` | `/api/v1/alunos/` | Lista todos os alunos |
| `GET` | `/api/v1/alunos/{id}` | Busca um aluno pelo ID |
| `PATCH` | `/api/v1/alunos/{id}` | Atualiza dados de um aluno |
| `DELETE` | `/api/v1/alunos/{id}` | Remove um aluno |
| `DELETE` | `/api/v1/alunos/` | Reseta a lista de alunos |

Cursos válidos: `GES`, `GEC`, `GET`, `GEP`

## Como rodar os testes

Os testes usam SQLite localmente — não é necessário ter o Docker rodando.

**1. Instale as dependências** (apenas na primeira vez):

```bash
pip install -r backend/requirements.txt
```

**2. Rode todos os testes:**

```bash
pytest tests/tests.py -v
```

**3. Rodar uma classe específica:**

```bash
pytest tests/tests.py::TestCriarAluno -v
```

**4. Rodar um teste específico:**

```bash
pytest tests/tests.py::TestFluxoCompleto::test_fluxo_3_alunos_por_curso -v
```

**5. Ver output dos prints durante os testes:**

```bash
pytest tests/tests.py -v -s
```

## Verificar dados no banco

Com os containers rodando:

```bash
# listar alunos
docker-compose exec db psql -U postgres -d faculdade -c "SELECT * FROM alunos;"

# listar contadores por curso
docker-compose exec db psql -U postgres -d faculdade -c "SELECT * FROM curso_counters;"
```
