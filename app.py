from flask import Flask, request, jsonify, send_from_directory
from duckduckgo_search import DDGS
import os

app = Flask(__name__, static_folder="static")

def pesquisar(query):

    resultados = []

    try:

        with DDGS() as ddgs:

            busca = ddgs.text(
                query,
                region="br-pt",
                safesearch="off",
                max_results=5
            )

            for r in busca:

                resultados.append({
                    "titulo": r["title"],
                    "descricao": r["body"],
                    "link": r["href"]
                })

    except:
        pass

    return resultados


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/search", methods=["POST"])
def search():

    data = request.json
    query = data.get("query", "")

    resultados = pesquisar(query)

    return jsonify(resultados)


# porta correta para Render
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
