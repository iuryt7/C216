import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    client.delete("/api/v1/alunos/")
    yield
    client.delete("/api/v1/alunos/")


class TestCriarAluno:
    def test_criar_aluno_ges(self):
        r = client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        assert r.status_code == 201
        data = r.json()
        assert data["id"] == "GES1"
        assert data["matricula"] == 1
        assert data["curso"] == "GES"

    def test_criar_3_alunos_ges(self):
        nomes = ["Ana", "Bruno", "Carla"]
        for i, nome in enumerate(nomes, 1):
            r = client.post("/api/v1/alunos/", json={"nome": nome, "email": f"{nome.lower()}@email.com", "curso": "GES"})
            assert r.status_code == 201
            assert r.json()["id"] == f"GES{i}"

    def test_criar_3_alunos_gec(self):
        nomes = ["Diego", "Eva", "Fabio"]
        for i, nome in enumerate(nomes, 1):
            r = client.post("/api/v1/alunos/", json={"nome": nome, "email": f"{nome.lower()}@email.com", "curso": "GEC"})
            assert r.status_code == 201
            assert r.json()["id"] == f"GEC{i}"

    def test_curso_invalido_retorna_400(self):
        r = client.post("/api/v1/alunos/", json={"nome": "Teste", "email": "teste@email.com", "curso": "XYZ"})
        assert r.status_code == 400

    def test_matriculas_independentes_por_curso(self):
        client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        client.post("/api/v1/alunos/", json={"nome": "Bruno", "email": "bruno@email.com", "curso": "GES"})
        r = client.post("/api/v1/alunos/", json={"nome": "Carla", "email": "carla@email.com", "curso": "GEC"})
        assert r.json()["id"] == "GEC1"
        assert r.json()["matricula"] == 1


class TestListarAlunos:
    def test_listar_alunos_vazio(self):
        r = client.get("/api/v1/alunos/")
        assert r.status_code == 200
        assert r.json() == []

    def test_listar_alunos_com_dados(self):
        client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        client.post("/api/v1/alunos/", json={"nome": "Bruno", "email": "bruno@email.com", "curso": "GEC"})
        r = client.get("/api/v1/alunos/")
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_listar_retorna_todos_os_campos(self):
        client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        aluno = client.get("/api/v1/alunos/").json()[0]
        assert all(k in aluno for k in ["id", "nome", "email", "curso", "matricula"])


class TestBuscarAluno:
    def test_buscar_aluno_existente(self):
        client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        r = client.get("/api/v1/alunos/GES1")
        assert r.status_code == 200
        assert r.json()["nome"] == "Ana"

    def test_buscar_aluno_inexistente_retorna_404(self):
        r = client.get("/api/v1/alunos/GES999")
        assert r.status_code == 404

    def test_buscar_aluno_gec_por_id(self):
        client.post("/api/v1/alunos/", json={"nome": "Diego", "email": "diego@email.com", "curso": "GEC"})
        r = client.get("/api/v1/alunos/GEC1")
        assert r.status_code == 200
        assert r.json()["curso"] == "GEC"


class TestAtualizarAluno:
    def test_atualizar_nome(self):
        client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        r = client.patch("/api/v1/alunos/GES1", json={"nome": "Ana Clara"})
        assert r.status_code == 200
        assert r.json()["nome"] == "Ana Clara"

    def test_atualizar_email(self):
        client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        r = client.patch("/api/v1/alunos/GES1", json={"email": "novo@email.com"})
        assert r.status_code == 200
        assert r.json()["email"] == "novo@email.com"

    def test_atualizar_aluno_inexistente_retorna_404(self):
        r = client.patch("/api/v1/alunos/GES999", json={"nome": "Teste"})
        assert r.status_code == 404

    def test_atualizar_curso_invalido_retorna_400(self):
        client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        r = client.patch("/api/v1/alunos/GES1", json={"curso": "XYZ"})
        assert r.status_code == 400


class TestRemoverAluno:
    def test_remover_aluno(self):
        client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        r = client.delete("/api/v1/alunos/GES1")
        assert r.status_code == 200
        assert client.get("/api/v1/alunos/GES1").status_code == 404

    def test_id_nao_reutilizado_apos_delete(self):
        client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        client.delete("/api/v1/alunos/GES1")
        r = client.post("/api/v1/alunos/", json={"nome": "Bruno", "email": "bruno@email.com", "curso": "GES"})
        assert r.json()["id"] == "GES2"

    def test_remover_aluno_inexistente_retorna_404(self):
        r = client.delete("/api/v1/alunos/GES999")
        assert r.status_code == 404

    def test_remover_nao_afeta_outros_alunos(self):
        client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        client.post("/api/v1/alunos/", json={"nome": "Bruno", "email": "bruno@email.com", "curso": "GES"})
        client.delete("/api/v1/alunos/GES1")
        assert client.get("/api/v1/alunos/GES2").status_code == 200


class TestResetarAlunos:
    def test_resetar_lista(self):
        client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        r = client.delete("/api/v1/alunos/")
        assert r.status_code == 200
        assert client.get("/api/v1/alunos/").json() == []

    def test_resetar_reinicia_contadores(self):
        client.post("/api/v1/alunos/", json={"nome": "Ana", "email": "ana@email.com", "curso": "GES"})
        client.delete("/api/v1/alunos/")
        r = client.post("/api/v1/alunos/", json={"nome": "Bruno", "email": "bruno@email.com", "curso": "GES"})
        assert r.json()["id"] == "GES1"


class TestFluxoCompleto:
    def test_fluxo_3_alunos_ges_e_3_gec(self):
        ges = [{"nome": "Ana", "email": "ana@email.com", "curso": "GES"},
               {"nome": "Bruno", "email": "bruno@email.com", "curso": "GES"},
               {"nome": "Carla", "email": "carla@email.com", "curso": "GES"}]
        gec = [{"nome": "Diego", "email": "diego@email.com", "curso": "GEC"},
               {"nome": "Eva", "email": "eva@email.com", "curso": "GEC"},
               {"nome": "Fabio", "email": "fabio@email.com", "curso": "GEC"}]

        for aluno in ges + gec:
            assert client.post("/api/v1/alunos/", json=aluno).status_code == 201

        assert len(client.get("/api/v1/alunos/").json()) == 6

        assert client.get("/api/v1/alunos/GES3").json()["nome"] == "Carla"
        assert client.get("/api/v1/alunos/GEC3").json()["nome"] == "Fabio"

        client.patch("/api/v1/alunos/GES1", json={"nome": "Ana Paula"})
        assert client.get("/api/v1/alunos/GES1").json()["nome"] == "Ana Paula"

        client.delete("/api/v1/alunos/GEC2")
        assert len(client.get("/api/v1/alunos/").json()) == 5
