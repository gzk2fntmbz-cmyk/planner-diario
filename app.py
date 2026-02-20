from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

ARQUIVO = "tarefas.json"


# ---------- helpers ----------
def carregar_tarefas():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_tarefas(tarefas):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=2, ensure_ascii=False)


# ---------- rotas ----------
@app.route("/")
def index():
    tarefas = carregar_tarefas()
    return render_template("index.html", tarefas=tarefas)


@app.route("/adicionar", methods=["POST"])
def adicionar():
    tarefas = carregar_tarefas()

    texto = request.form.get("texto")
    prioridade = request.form.get("prioridade")
    hora = request.form.get("hora")

    tarefas.append({
        "texto": texto,
        "prioridade": prioridade,
        "hora": hora,
        "feita": False
    })

    salvar_tarefas(tarefas)
    return redirect(url_for("index"))


@app.route("/toggle/<int:idx>")
def toggle(idx):
    tarefas = carregar_tarefas()

    if 0 <= idx < len(tarefas):
        tarefas[idx]["feita"] = not tarefas[idx]["feita"]

    salvar_tarefas(tarefas)
    return redirect(url_for("index"))


@app.route("/remover/<int:idx>")
def remover(idx):
    tarefas = carregar_tarefas()

    if 0 <= idx < len(tarefas):
        tarefas.pop(idx)

    salvar_tarefas(tarefas)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
