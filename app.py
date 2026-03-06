from flask import Flask, request, jsonify
import requests
import urllib.parse
import random
from duckduckgo_search import DDGS

app = Flask(__name__)

memoria = []

# ---------------- COMBOS ----------------

combos = {

"combo de mahito":
"Combo Mahito: 3 m1 → downslash → 1 no ar → 2 Mahito → R dash → 4 Mahito → 3 Mahito → 2x skill 2",

"combo de itadori":
"Combo Itadori: 3 m1 → uppercut → 1 Itadori → 2 Itadori → 3 Itadori no ar",

"combo de nanami":
"Combo Nanami: 3 clicks → downslash → 4-1-2-3 → depois vai pra trás do cara 😏"
}

# ---------------- ASSUNTOS ----------------

assuntos = {

"jogos":[
"Eu gosto bastante de jogos 🎮 você joga quais?",
"Jogos são muito legais! Qual seu favorito?",
"Ultimamente tenho ouvido falar muito de Blox Fruits."
],

"anime":[
"Eu gosto bastante de anime 😄 principalmente Jujutsu Kaisen.",
"Anime é incrível. Qual seu favorito?",
"Jujutsu Kaisen tem lutas muito boas."
],

"musica":[
"Eu gosto de música também 🎵 que tipo você gosta?",
"Música ajuda muito a relaxar.",
"Qual sua música favorita?"
]
}

# ---------------- PSICOLOGO ----------------

solucoes = {

"triste":[
"Quando estamos tristes, conversar com alguém de confiança ajuda muito.",
"Tente fazer algo que você gosta, como ouvir música ou jogar.",
"Às vezes descansar ajuda a melhorar."
],

"roubado":[
"Ser roubado é muito chato. Talvez seja bom avisar alguém de confiança.",
"Você pode avisar sua família ou responsáveis."
],

"terminei":[
"Términos são difíceis. Conversar com amigos pode ajudar.",
"Com o tempo a dor diminui."
]
}

# ---------------- SIGMA ----------------

respostas_sigma = [
"Sigma detectado 🐺",
"Independência total 😎",
"Focado e sozinho."
]

# ---------------- CONVERSA ----------------

respostas_conversa = [
"E aí 😁",
"Hmmm interessante 🤔",
"Conta mais sobre isso.",
"Legal! Eu estava pensando sobre isso também.",
"Interessante! O que você acha disso?"
]

# ---------------- WIKIPEDIA ----------------

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


# ---------------- DUCKDUCKGO ----------------

def pesquisar_duck(termo):

    try:

        with DDGS() as ddgs:

            resultados = ddgs.text(termo,max_results=1)

            for r in resultados:

                return f"{r['title']}\n{r['body']}\n{r['href']}"

    except:
        pass

    return None


# ---------------- IA ----------------

def frost(texto):

    texto = texto.lower()

    memoria.append(texto)

    # combos
    for c in combos:
        if c in texto:
            return combos[c]

    # psicologo
    for problema in solucoes:
        if problema in texto:
            return random.choice(solucoes[problema])

    # assuntos
    if "jogo" in texto:
        return random.choice(assuntos["jogos"])

    if "anime" in texto:
        return random.choice(assuntos["anime"])

    if "musica" in texto:
        return random.choice(assuntos["musica"])

    # sigma
    if "sigma" in texto:
        return random.choice(respostas_sigma)

    # pesquisa
    if texto.startswith("pesquisar"):

        termo = texto.replace("pesquisar","").strip()

        wiki = pesquisar_wikipedia(termo)

        if wiki:
            return wiki

        web = pesquisar_duck(termo)

        if web:
            return web

        return "Não encontrei resultados."

    return random.choice(respostas_conversa)


# ---------------- SITE ----------------

@app.route("/")
def home():
    return "Frost IA está online ❄️"

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    msg = data.get("msg","")

    resposta = frost(msg)

    return jsonify({
        "resposta": resposta
    })


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
