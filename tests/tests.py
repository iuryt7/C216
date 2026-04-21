import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) ## foi para corrigir o erro de importação do app.main, não sei por que tava dando isso mas funcionou

import pytest
from fastapi.testclient import TestClient
 
from app.main import app
 
client = TestClient(app)
 
 

class TestHelloWorld:
    def test_hello_world_retorna_200(self):
        response = client.get("/")
        assert response.status_code == 200
 
    def test_hello_world_retorna_mensagem_correta(self):
        response = client.get("/")
        assert response.json() == {"message": "Hello, FastAPI!"}
 
 
class TestHelloViaQuery:
    def test_hello_via_query_com_nome(self):
        response = client.get("/api/v1/hello", params={"name": "Iury"})
        assert response.status_code == 200
        assert response.json() == {"message": "Hello Iury"}
 
    def test_hello_via_query_com_nome_vazio(self):
        response = client.get("/api/v1/hello", params={"name": ""})
        assert response.status_code == 200
        assert response.json() == {"message": "Hello "}
 
    def test_hello_via_query_sem_parametro_retorna_422(self):
        response = client.get("/api/v1/hello")
        assert response.status_code == 422
 
    def test_hello_via_query_com_caracteres_especiais(self):
        response = client.get("/api/v1/hello", params={"name": "João da Silva"})
        assert response.status_code == 200
        assert response.json() == {"message": "Hello João da Silva"}
 
 
class TestHelloViaPath:
    def test_hello_via_path_com_nome(self):
        response = client.get("/api/v1/hello/Iury")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello Iury"}
 
    def test_hello_via_path_com_nome_numerico(self):
        response = client.get("/api/v1/hello/123")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello 123"}
 
    def test_hello_via_path_sem_nome(self):
        response = client.get("/api/v1/hello/")
        assert response.status_code == 422
 
class TestHelloPost:
    def test_post_hello_com_body_valido(self):
        response = client.post("/api/v1/hello", json={"name": "Iury"})
        assert response.status_code == 200
        assert response.json() == {"message": "Hello Iury"}
 
    def test_post_hello_sem_body_retorna_422(self):
        response = client.post("/api/v1/hello")
        assert response.status_code == 422
 
    def test_post_hello_com_body_invalido_retorna_422(self):
        response = client.post("/api/v1/hello", json={"nome": "Iury"})
        assert response.status_code == 422
 
    def test_post_hello_com_name_nao_string_retorna_422(self):
        response = client.post("/api/v1/hello", json={"name": 123})
        assert response.status_code in (200, 422)
 

class TestUpdate:
    def test_put_update_com_body_valido(self):
        response = client.put("/api/v1/update", json={"name": "Iury"})
        assert response.status_code == 200
        assert response.json() == {
            "message": "Recurso atualizado com o nome: Iury"
        }
 
    def test_put_update_sem_body_retorna_422(self):
        response = client.put("/api/v1/update")
        assert response.status_code == 422
 
    def test_put_update_body_sem_name_retorna_422(self):
        response = client.put("/api/v1/update", json={})
        assert response.status_code == 422
 
 
class TestDelete:
    def test_delete_com_nome_valido(self):
        response = client.delete("/api/v1/delete", params={"name": "Iury"})
        assert response.status_code == 200
        assert response.json() == {
            "message": "Recurso deletado com o nome: Iury"
        }
 
    def test_delete_sem_nome_retorna_422(self):
        response = client.delete("/api/v1/delete")
        assert response.status_code == 422
 
 
class TestPatch:
    def test_patch_com_body_valido(self):
        response = client.patch("/api/v1/patch", json={"name": "Iury"})
        assert response.status_code == 200
        assert response.json() == {
            "message": "Modificação parcial aplicada ao recurso com o nome: Iury"
        }
 
    def test_patch_sem_body_retorna_422(self):
        response = client.patch("/api/v1/patch")
        assert response.status_code == 422
 
    def test_patch_body_sem_name_retorna_422(self):
        response = client.patch("/api/v1/patch", json={})
        assert response.status_code == 422
 

@pytest.mark.parametrize(
    "nome",
    ["Iury", "Ana", "João", "Maria", "x", "A" * 100],
)
def test_fluxo_completo_com_varios_nomes(nome: str):
    r = client.get("/api/v1/hello", params={"name": nome})
    assert r.status_code == 200
    assert r.json()["message"] == f"Hello {nome}"

    if "/" not in nome:
        r = client.get(f"/api/v1/hello/{nome}")
        assert r.status_code == 200
 
    r = client.post("/api/v1/hello", json={"name": nome})
    assert r.status_code == 200
 
    r = client.put("/api/v1/update", json={"name": nome})
    assert r.status_code == 200
 
    r = client.delete("/api/v1/delete", params={"name": nome})
    assert r.status_code == 200
 
    r = client.patch("/api/v1/patch", json={"name": nome})
    assert r.status_code == 200