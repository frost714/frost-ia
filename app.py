from flask import Flask, request, jsonify, send_from_directory
import requests
import urllib.parse
import random
import os
import re
from duckduckgo_search import DDGS

app = Flask(__name__, static_folder="static")

# respostas simples
respostas = [
    "Interessante 🤔",
    "Pode explicar melhor?",
    "Conta mais sobre isso.",
    "Hmm entendi.",
]

# detectar conta matemática
def calcular(texto):

    try:
        conta = re.search(r'\d+[\+\-\*\/]\d+', texto)

        if conta:
            resultado = eval(conta.group())
            return f"O resultado é {resultado}"

    except:
        pass

    return None


# pesquisar wikipedia
def pesquisar_wikipedia(termo):

    termo_url = urllib.parse.quote(termo)

    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo_url}"

    try:

        r = requests.get(url, timeout=5)

        data = r.json()

        if "extract" in data and len(data["extract"]) > 20:

            return data["extract"]

    except:
        pass

    return None


# pesquisar internet
def pesquisar_web(termo):

    try:

        with DDGS() as ddgs:

            resultados = ddgs.text(termo, max_results=1)

            for r in resultados:

                return f"{r['title']} - {r['body']}"

    except:
        pass

    return None


def frost(msg):

    texto = msg.lower().strip()

    # 1️⃣ matemática
    calc = calcular(texto)

    if calc:
        return calc

    # 2️⃣ perguntas
    perguntas = [
        "quem é","quem foi",
        "o que é","o que foi",
        "onde fica",
        "quando foi",
        "como funciona"
    ]

    for p in perguntas:

        if p in texto:

            termo = texto.replace(p,"").strip()

            wiki = pesquisar_wikipedia(termo)

            if wiki:
                return wiki

            web = pesquisar_web(termo)

            if web:
                return web

    # 3️⃣ pergunta normal
    if "?" in texto:

        wiki = pesquisar_wikipedia(texto)

        if wiki:
            return wiki

        web = pesquisar_web(texto)

        if web:
            return web

    # 4️⃣ conversa
    if texto in ["oi","ola","olá","eae"]:

        return "Olá! Eu sou a Frost IA ❄️"

    if "tudo bem" in texto:

        return "Estou funcionando perfeitamente 😄"

    # fallback
    return random.choice(respostas)


@app.route("/")
def home():

    return send_from_directory("static","index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    msg = data.get("msg","")

    resposta = frost(msg)

    return jsonify({"resposta":resposta})


if __name__ == "__main__":

    port = int(os.environ.get("PORT",8080))

    app.run(host="0.0.0.0", port=port)
