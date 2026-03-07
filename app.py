from flask import Flask, request, jsonify
import requests, urllib.parse, random
from duckduckgo_search import DDGS

app = Flask(__name__)

# ---------------- MEMÓRIA ----------------
memoria = []

# ---------------- COMBOS ----------------
combos = {
    "combo de mahito": "Combo Mahito: 3 m1 → downslash → 1 no ar → 2 Mahito → R dash → 4 Mahito → 3 Mahito → 2x skill 2",
    "combo de itadori": "Combo Itadori: 3 m1 → uppercut → 1 → 2 → 3 no ar",
    "combo de nanami": "Combo Nanami: 3 clicks → downslash → 4-1-2-3 → depois vai pra trás 😏"
}

# ---------------- ASSUNTOS ----------------
assuntos = {
    "jogo": ["Eu gosto bastante de jogos 🎮. Qual seu favorito?"],
    "anime": ["Anime é muito bom 😄 Qual você gosta?"],
    "musica": ["Música sempre melhora o dia 🎵"],
    "filme": ["Filmes são ótimos 🍿"]
}

# ---------------- RESPOSTAS ----------------
respostas_conversa = [
    "Interessante 🤔",
    "Conta mais sobre isso.",
    "Hmm, entendi.",
    "Legal 😎"
]

# ---------------- WIKIPEDIA ----------------
def pesquisar_wikipedia(termo):

    termo_url = urllib.parse.quote(termo)
    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo_url}"

    try:
        r = requests.get(url, timeout=5)
        data = r.json()

        if "extract" in data:
            return data["extract"]

    except:
        pass

    return None

# ---------------- DUCKDUCKGO ----------------
def pesquisar_duck(termo):

    try:
        with DDGS() as ddgs:
            resultados = ddgs.text(termo, max_results=1)

            for r in resultados:
                return f"{r['title']}\n{r['body']}"

    except:
        pass

    return "Não encontrei resultados."

# ---------------- IA ----------------
def frost(texto):

    texto = texto.lower()
    memoria.append({"usuario": texto})

    # -------- COMBOS --------
    for c in combos:
        if c in texto:
            resposta = combos[c]
            memoria[-1]["frost"] = resposta
            return resposta

    # -------- ASSUNTOS --------
    for a in assuntos:
        if a in texto:
            resposta = random.choice(assuntos[a])
            memoria[-1]["frost"] = resposta
            return resposta

    # -------- PERGUNTAS (PESQUISA AUTOMÁTICA) --------
    perguntas = ["quem", "o que", "como", "onde", "quando", "por que"]

    if any(texto.startswith(p) for p in perguntas):

        termo = texto.replace("quem é","")
        termo = termo.replace("quem foi","")
        termo = termo.replace("o que é","")
        termo = termo.replace("o que foi","")
        termo = termo.strip()

        wiki = pesquisar_wikipedia(termo)

        if wiki:
            resposta = wiki
        else:
            resposta = pesquisar_duck(termo)

        memoria[-1]["frost"] = resposta
        return resposta

    # -------- CONTEXTO --------
    for item in reversed(memoria[:-1]):

        if any(p in texto for p in item["usuario"].split()):

            resposta = f"Você mencionou isso antes 🤔 {item.get('frost','')}"
            memoria[-1]["frost"] = resposta
            return resposta

    # -------- PADRÃO --------
    resposta = random.choice(respostas_conversa)

    memoria[-1]["frost"] = resposta

    return resposta

# ---------------- ROTAS ----------------
@app.route("/")
def home():
    return "Frost IA online ❄️"

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    msg = data.get("msg","")

    resposta = frost(msg)

    return jsonify({
        "resposta": resposta,
        "memoria": memoria[-10:]
    })

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

