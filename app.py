from flask import Flask, request, jsonify, send_from_directory
import requests
import urllib.parse
import random
import os
from duckduckgo_search import DDGS

app = Flask(__name__, static_folder="static")

memoria = []

respostas = [
"E aí 😄",
"Interessante 🤔",
"Conta mais",
"Legal 😎"
]

combos = {
"combo de mahito":"3 m1 → downslash → 1 → dash → 4",
"combo de itadori":"3 m1 → uppercut → 1 → 2 → 3"
}

def pesquisar_wikipedia(termo):

    termo_url = urllib.parse.quote(termo)

    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo_url}"

    try:
        r = requests.get(url,timeout=5)
        data = r.json()

        if "extract" in data:
            return data["extract"]

    except:
        pass

    return None


def pesquisar_duck(termo):

    try:

        with DDGS() as ddgs:

            resultados = ddgs.text(termo,max_results=1)

            for r in resultados:

                return f"{r['title']} - {r['body']}"

    except:
        pass

    return "Não encontrei resultados."


def frost(msg):

    texto = msg.lower()

    memoria.append(texto)

    for c in combos:

        if c in texto:

            return combos[c]

    perguntas = ["quem","o que","como","onde","quando","por que"]

    if any(p in texto for p in perguntas):

        termo = texto.replace("quem é","").replace("o que é","").strip()

        wiki = pesquisar_wikipedia(termo)

        if wiki:
            return wiki

        return pesquisar_duck(termo)

    return random.choice(respostas)


@app.route("/")
def home():

    return send_from_directory("static","index.html")


@app.route("/chat",methods=["POST"])
def chat():

    data = request.json

    msg = data.get("msg","")

    resposta = frost(msg)

    return jsonify({"resposta":resposta})


if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)

