from flask import Flask, request, jsonify
import requests, urllib.parse, random
from duckduckgo_search import DDGS
from datetime import datetime

app = Flask(__name__)

# ---------------- MEMÓRIA ----------------
memoria = []

# ---------------- COMBOS ----------------
combos = {
    "combo de mahito": "Combo Mahito: 3 m1 → downslash → 1 no ar → 2 Mahito → R dash → 4 Mahito → 3 Mahito → 2x skill 2",
    "combo de itadori": "Combo Itadori: 3 m1 → uppercut → 1 Itadori → 2 Itadori → 3 Itadori no ar",
    "combo de nanami": "Combo Nanami: 3 clicks → downslash → 4-1-2-3 → depois vai pra trás do cara 😏"
}

# ---------------- RITUAIS ----------------
rituais = {
    "mahoraga": [
        "🌀 Ritual de Mahoraga iniciado...",
        "Primeiro, concentre toda a energia amaldiçoada no tesouro.",
        "Segundo, desenhe os selos de contenção ao redor do local.",
        "Terceiro, invoque a maldição antiga com seu poder máximo.",
        "Quarto, Mahoraga aparece com todo o seu poder demoníaco!",
        "⚠️ Cuidado! Este ritual é extremamente perigoso!"
    ]
}

# ---------------- ASSUNTOS ----------------
assuntos = {
    "jogos": [
        "Eu gosto bastante de jogos 🎮. Qual seu favorito?",
        "Blox Fruits, MM2, Epic Games... você já jogou algum?",
        "Jogos são ótimos para relaxar 😎"
    ],
    "anime": [
        "Jujutsu Kaisen é incrível 😄. Qual personagem você mais gosta?",
        "Anime é vida! Você já assistiu algum episódio novo?",
        "Eu adoro lutas épicas de anime!"
    ],
    "musica": [
        "Música 🎵 ajuda a relaxar. Qual você gosta?",
        "Qual foi a última música que você ouviu e gostou?",
        "Música boa deixa o dia melhor 😎"
    ],
    "filmes": [
        "Eu adoro filmes 🍿. Qual o seu favorito?",
        "Cinemas estão cheios de filmes legais, viu!",
        "Filmes de ação são os meus preferidos!"
    ]
}

# ---------------- PSICOLOGO ----------------
solucoes = {
    "triste": [
        "Quando estamos tristes, conversar com alguém ajuda muito.",
        "Tente fazer algo que você gosta ou ouvir música.",
        "Respire fundo e dê um tempo para você mesmo."
    ],
    "ansioso": [
        "Respirar devagar ajuda bastante quando se está ansioso.",
        "Focar em algo que você gosta pode distrair a mente.",
        "Tente escrever o que sente, ajuda a organizar os pensamentos."
    ],
    "roubado": [
        "Ser roubado é muito chato. Avise alguém de confiança.",
        "Verifique se seus cartões e pertences estão seguros.",
        "O melhor é sempre pedir ajuda a um adulto ou responsável."
    ],
    "terminei": [
        "Términos são difíceis. Conversar com amigos ajuda.",
        "Tente se distrair com algo que gosta.",
        "Com o tempo, a dor diminui. Foque em coisas boas."
    ],
    "briguei": [
        "Brigas acontecem. Tente conversar com calma depois.",
        "Dar um tempo ajuda a resolver melhor.",
        "Tente entender o lado da outra pessoa."
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
    return "Não encontrei na Wikipedia."

# ---------------- DUCKDUCKGO ----------------
def pesquisar_duck(termo):
    try:
        with DDGS() as ddgs:
            resultados = ddgs.text(termo,max_results=1)
            for r in resultados:
                return f"{r['title']}\n{r['body']}\n{r['href']}"
    except:
        pass
    return "Não encontrei resultados."

# ---------------- IA ----------------
def frost(texto):
    texto = texto.lower()
    memoria.append({"hora": datetime.now().strftime("%H:%M:%S"), "msg": texto})

    # Ritual Mahoraga
    for ritual in rituais:
        if ritual in texto or ("invoco" in texto and ritual in texto):
            return "\n".join(rituais[ritual])

    # Combos
    for c in combos:
        if c in texto:
            return combos[c]

    # Psicólogo
    for problema in solucoes:
        if problema in texto:
            return random.choice(solucoes[problema])

    # Assuntos
    for chave in assuntos:
        if chave in texto:
            return random.choice(assuntos[chave])

    # Sigma
    if "sigma" in texto:
        return random.choice(respostas_sigma)

    # Pesquisa
    if texto.startswith("pesquisar"):
        termo = texto.replace("pesquisar","").strip()
        wiki = pesquisar_wikipedia(termo)
        if wiki:
            return wiki
        web = pesquisar_duck(termo)
        if web:
            return web
        return "Não encontrei resultados."

    # Conversa normal
    return random.choice(respostas_conversa)

# ---------------- SITE ----------------
@app.route("/")
def home():
    return "Frost IA Supreme está online ❄️"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("msg","")
    resposta = frost(msg)
    return jsonify({"resposta": resposta, "memoria": memoria[-5:]})  # retorna últimas 5 mensagens

# ---------------- ROTA HTML ----------------
@app.route("/chatpage")
def chatpage():
    return app.send_static_file("index.html")  # arquivo index.html na pasta static

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
