from flask import Flask, render_template, request
import random

app = Flask(__name__)

def texto_para_jogadores(texto):
    jogadores = []
    linhas = texto.strip().splitlines()
    for linha in linhas:
        partes = linha.strip().split()
        if len(partes) != 3:
            continue
        nome = partes[0].capitalize()
        try:
            nota = int(partes[1])
            pos = partes[2].lower()
            posicao = 1 if pos == "defesa" else 2 if pos == "ataque" else None
            if posicao and 5 <= nota <= 10:
                jogadores.append({"nome": nome, "nota": nota, "posicao": posicao})
        except ValueError:
            continue
    return jogadores

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sortear', methods=['POST'])
def sortear():
    texto = request.form.get('jogadores')
    jogadores = texto_para_jogadores(texto)

    defensores = [j for j in jogadores if j['posicao'] == 1]
    atacantes = [j for j in jogadores if j['posicao'] == 2]

    min_def = len(defensores) // 2
    min_ata = len(atacantes) // 2

    combinacoes_validas = []

    for _ in range(5000):
        random.shuffle(defensores)
        random.shuffle(atacantes)

        time1 = defensores[:min_def] + atacantes[:min_ata]
        time2 = defensores[min_def:2*min_def] + atacantes[min_ata:2*min_ata]

        if len(time1) != len(time2):
            continue

        soma1 = sum(j['nota'] for j in time1)
        soma2 = sum(j['nota'] for j in time2)

        if abs(soma1 - soma2) <= 2:
            combinacoes_validas.append((time1, time2))

    if combinacoes_validas:
        time1, time2 = random.choice(combinacoes_validas)
        usados = time1 + time2
        reservas = [j for j in jogadores if j not in usados]
    else:
        time1 = time2 = []
        reservas = jogadores

    total_time1 = sum(j['nota'] for j in time1)
    total_time2 = sum(j['nota'] for j in time2)

    return render_template('index.html', time1=time1, time2=time2, reservas=reservas, texto=texto, total_time1=total_time1, total_time2=total_time2)

if __name__ == '__main__':
    app.run(debug=True)
