from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
ARQUIVO = "tarefas.json"

def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_tarefas(tarefas):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

@app.route("/")
def index():
    tarefas = carregar_tarefas()
    return render_template("index.html", tarefas=tarefas)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    tarefas = carregar_tarefas()

    nova = {
        "titulo": request.form["titulo"],
        "horario": request.form["horario"],
        "prioridade": request.form["prioridade"],
        "concluida": False
    }

    tarefas.append(nova)
    salvar_tarefas(tarefas)
    return redirect("/")

@app.route("/concluir/<int:id>")
def concluir(id):
    tarefas = carregar_tarefas()
    if 0 <= id < len(tarefas):
        tarefas[id]["concluida"] = True
        salvar_tarefas(tarefas)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
