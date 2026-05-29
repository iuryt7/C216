import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "c216-secret-key"

API_URL = os.getenv("API_URL", "http://localhost:8000")


@app.route("/")
def index():
    try:
        response = requests.get(f"{API_URL}/api/v1/alunos/")
        alunos = response.json() if response.status_code == 200 else []
    except requests.exceptions.ConnectionError:
        alunos = []
        flash("Erro ao conectar com a API.", "error")
    return render_template("index.html", alunos=alunos)


@app.route("/alunos/novo", methods=["GET", "POST"])
def novo_aluno():
    cursos = ["GES", "GEC", "GET", "GEP"]
    if request.method == "POST":
        data = {
            "nome": request.form["nome"],
            "email": request.form["email"],
            "curso": request.form["curso"],
        }
        try:
            response = requests.post(f"{API_URL}/api/v1/alunos/", json=data)
            if response.status_code == 201:
                flash("Aluno criado com sucesso!", "success")
                return redirect(url_for("index"))
            flash(f"Erro: {response.json().get('detail', 'Erro desconhecido')}", "error")
        except requests.exceptions.ConnectionError:
            flash("Erro ao conectar com a API.", "error")
    return render_template("novo_aluno.html", cursos=cursos)


@app.route("/alunos/<aluno_id>/editar", methods=["GET", "POST"])
def editar_aluno(aluno_id):
    cursos = ["GES", "GEC", "GET", "GEP"]
    if request.method == "POST":
        data = {k: v for k, v in {
            "nome": request.form.get("nome"),
            "email": request.form.get("email"),
            "curso": request.form.get("curso"),
        }.items() if v}
        try:
            response = requests.patch(f"{API_URL}/api/v1/alunos/{aluno_id}", json=data)
            if response.status_code == 200:
                flash("Aluno atualizado com sucesso!", "success")
                return redirect(url_for("index"))
            flash(f"Erro: {response.json().get('detail', 'Erro desconhecido')}", "error")
        except requests.exceptions.ConnectionError:
            flash("Erro ao conectar com a API.", "error")

    try:
        response = requests.get(f"{API_URL}/api/v1/alunos/{aluno_id}")
        if response.status_code == 404:
            flash("Aluno não encontrado.", "error")
            return redirect(url_for("index"))
        aluno = response.json()
    except requests.exceptions.ConnectionError:
        flash("Erro ao conectar com a API.", "error")
        return redirect(url_for("index"))
    return render_template("editar_aluno.html", aluno=aluno, cursos=cursos)


@app.route("/alunos/<aluno_id>/deletar", methods=["POST"])
def deletar_aluno(aluno_id):
    try:
        response = requests.delete(f"{API_URL}/api/v1/alunos/{aluno_id}")
        if response.status_code == 200:
            flash("Aluno removido com sucesso!", "success")
        else:
            flash("Erro ao remover aluno.", "error")
    except requests.exceptions.ConnectionError:
        flash("Erro ao conectar com a API.", "error")
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
