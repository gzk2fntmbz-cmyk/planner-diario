from flask import Flask, render_template, request, redirect
import json
import os
import uuid

app = Flask(__name__)
ARQUIVO = "tarefas.json"


# ----------------- helpers -----------------
def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_tarefas(tarefas):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)


# ----------------- rotas -----------------
@app.route("/")
def index():
    tarefas = carregar_tarefas()
    return render_template("index.html", tarefas=tarefas)


@app.route("/adicionar", methods=["POST"])
def adicionar():
    tarefas = carregar_tarefas()

    nova = {
        "id": str(uuid.uuid4()),  # 🔥 ID único por tarefa
        "titulo": request.form["titulo"],
        "horario": request.form["horario"],
        "prioridade": request.form["prioridade"],
        "concluida": False
    }

    tarefas.append(nova)
    salvar_tarefas(tarefas)
    return redirect("/")


@app.route("/toggle/<id>")
def toggle(id):
    tarefas = carregar_tarefas()

    for tarefa in tarefas:
        if tarefa["id"] == id:
            tarefa["concluida"] = not tarefa["concluida"]
            break

    salvar_tarefas(tarefas)
    return redirect("/")


@app.route("/remover/<id>")
def remover(id):
    tarefas = carregar_tarefas()
    tarefas = [t for t in tarefas if t["id"] != id]
    salvar_tarefas(tarefas)
    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
