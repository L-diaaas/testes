import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/alunos"

@pytest.fixture
def aluno_exemplo():
    return {
        "nome": "João Silva",
        "turma_id": 1,
        "idade": 20,
        "data_nascimento": "2005-05-15",
        "nota_primeiro_semestre": 7.5,
        "nota_segundo_semestre": 8.0,
        "media_final": 7.75
    }

def test001_criar_aluno(aluno_exemplo):
    response = requests.post(BASE_URL, json=aluno_exemplo)
    assert response.status_code == 201
    assert response.json()["message"] == "Aluno adicionado com sucesso"
    assert response.json()["aluno"]["nome"] == aluno_exemplo["nome"]

def test002_criar_aluno_invalido():
    response = requests.post(BASE_URL, json={})
    assert response.status_code == 400  # A API deveria retornar 400
    assert "erro" in response.json()
    
def test003_listar_alunos():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert isinstance(response.json(), list)  

def test004_obter_aluno_existente():
    aluno_id = 1
    response = requests.get(f"{BASE_URL}/{aluno_id}")
    assert response.status_code == 200
    assert "nome" in response.json()

def test005_obter_aluno_inexistente():
    aluno_id = 9999
    response = requests.get(f"{BASE_URL}/{aluno_id}")
    assert response.status_code == 404  # A API deveria retornar 404
    assert "mensagem" in response.json()

def test006_atualizar_aluno_existente():
    aluno_id = 1
    dados_atualizados = {
        "nome": "João Souza",
        "idade": 21,
        "nota_primeiro_semestre": 8.5,
        "nota_segundo_semestre": 9.0,
        "media_final": 8.75
    }
    response = requests.put(f"{BASE_URL}/{aluno_id}", json=dados_atualizados)
    assert response.status_code == 200
    assert response.json()["aluno"]["nome"] == "João Souza"

def test007_atualizar_aluno_inexistente():
    aluno_id = 9999
    dados_atualizados = {"nome": "Aluno Inexistente"}
    response = requests.put(f"{BASE_URL}/{aluno_id}", json=dados_atualizados)
    assert response.status_code == 404  # A API deveria retornar 404
    assert "mensagem" in response.json()

def test008_excluir_aluno_existente():
    aluno_id = 1
    response = requests.delete(f"{BASE_URL}/{aluno_id}")
    assert response.status_code == 204
    assert "mensagem" in response.json()

def test009_excluir_aluno_inexistente():
    aluno_id = 9999
    response = requests.delete(f"{BASE_URL}/{aluno_id}")
    assert response.status_code == 404  # A API deveria retornar 404
    assert "mensagem" in response.json()

def test010_excluir_todos_alunos():
    response = requests.delete(BASE_URL)
    assert response.status_code == 200
    assert "mensagem" in response.json()
