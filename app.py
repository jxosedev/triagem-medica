import json
import os
from flask import Flask, render_template, request, jsonify

from triage import TriageEngine, NivelRisco, detectar_emergencia_texto

try:
    from ollama_client import gerar_possiveis_causas as ollama_causas
    OLLAMA_OK = True
except Exception:
    OLLAMA_OK = False

app = Flask(__name__)
app.secret_key = os.urandom(32).hex()


def montar_engine(dados):
    e = TriageEngine()

    p = dados.get("paciente", {})
    e.avaliacao.paciente.nome = p.get("nome", "")
    e.avaliacao.paciente.idade = int(p.get("idade", 0) or 0)
    e.avaliacao.paciente.sexo = p.get("sexo", "")
    try:
        e.avaliacao.paciente.peso = float(p.get("peso", 0) or 0)
    except ValueError:
        pass
    try:
        e.avaliacao.paciente.altura = float(p.get("altura", 0) or 0)
    except ValueError:
        pass

    h = dados.get("historico", {})
    eh = e.avaliacao.historico
    eh.diabetes = h.get("diabetes", False)
    eh.hipertensao = h.get("hipertensao", False)
    eh.asma = h.get("asma", False)
    eh.cardiopatia = h.get("cardiopatia", False)
    eh.doenca_pulmonar = h.get("doenca_pulmonar", False)
    eh.doenca_renal = h.get("doenca_renal", False)
    eh.gravidez = h.get("gravidez", False)
    eh.alergias = [x.strip() for x in h.get("alergias", "").split(",") if x.strip()]
    eh.medicamentos = [x.strip() for x in h.get("medicamentos", "").split(",") if x.strip()]
    eh.cirurgias_recentes = [x.strip() for x in h.get("cirurgias", "").split(",") if x.strip()]

    s = dados.get("sintomas", {})
    sintomas_texto = s.get("descricao", "")
    e.avaliacao.sintomas.append(sintomas_texto)

    if detectar_emergencia_texto(sintomas_texto):
        e.avaliacao.emergencia = True
        e.avaliacao.motivo_emergencia = sintomas_texto
        return e

    t = sintomas_texto.lower()

    if "febre" in t or s.get("temperatura"):
        temp_str = s.get("temperatura", "").strip()
        if temp_str:
            try:
                e.avaliacao.sinais_vitais.temperatura = float(temp_str)
            except ValueError:
                pass
        dias = s.get("febre_dias", "")
        if dias:
            try:
                e.dados_febre["dias"] = int(dias)
            except ValueError:
                pass

    if "dor" in t or s.get("dor_local"):
        e.dados_dor["local"] = s.get("dor_local", "")
        try:
            e.dados_dor["intensidade"] = int(s.get("dor_intensidade", 0) or 0)
        except ValueError:
            pass

        if "peito" in t or "peito" in e.dados_dor.get("local", "").lower():
            e.dados_dor_peito["irradia"] = s.get("dor_peito_irradia", False)
            e.dados_dor_peito["suando"] = s.get("dor_peito_suando", False)
            e.dados_dor_peito["falta_ar"] = s.get("dor_peito_falta_ar", False)

            intensidade = e.dados_dor.get("intensidade", 0)
            irradia = e.dados_dor_peito.get("irradia", False)
            suando = e.dados_dor_peito.get("suando", False)
            falta_ar = e.dados_dor_peito.get("falta_ar", False)
            if intensidade >= 7 or (irradia and (suando or falta_ar)):
                e.avaliacao.emergencia = True
                e.avaliacao.motivo_emergencia = "Dor no peito com sinais de alerta"
                return e

    falta_ar = s.get("falta_ar", "")
    if "falta de ar" in t or falta_ar:
        if s.get("falta_ar_repouso"):
            e.dados_falta_ar["grave"] = True
            e.avaliacao.emergencia = True
            e.avaliacao.motivo_emergencia = "Falta de ar grave"
            return e
        if s.get("falta_ar_moderada"):
            e.dados_falta_ar["moderada"] = True

    if "tosse" in t:
        e.dados_tosse["tipo"] = s.get("tosse_tipo", "seca")

    if "vômit" in t or "vomit" in t:
        try:
            vezes = int(s.get("vomitos_vezes", 0) or 0)
            if vezes > 5:
                e.dados_vomitos["frequente"] = True
        except ValueError:
            pass
        if not s.get("vomitos_agua"):
            e.dados_vomitos["frequente"] = True

    if "diarreia" in t or "diarréia" in t:
        if s.get("diarreia_sangue"):
            e.dados_diarreia["com_sangue"] = True

    e.avaliacao.tempo_sintomas = s.get("tempo", "")

    sv = e.avaliacao.sinais_vitais
    try:
        t_val = s.get("sv_temperatura", "").strip()
        if t_val:
            sv.temperatura = float(t_val)
    except ValueError:
        pass

    pa = s.get("sv_pressao", "").strip()
    if pa:
        match = __import__("re").match(r"(\d+)\s*/\s*(\d+)", pa)
        if match:
            sv.pressao_sistolica = int(match.group(1))
            sv.pressao_diastolica = int(match.group(2))

    try:
        fc_val = s.get("sv_fc", "").strip()
        if fc_val:
            sv.frequencia_cardiaca = int(fc_val)
    except ValueError:
        pass

    try:
        sat_val = s.get("sv_saturacao", "").strip()
        if sat_val:
            sv.saturacao = int(sat_val)
    except ValueError:
        pass

    return e


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/triagem", methods=["POST"])
def api_triagem():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados não fornecidos"}), 400

    engine = montar_engine(dados)
    engine.classificar()

    if not engine.avaliacao.emergencia and OLLAMA_OK:
        try:
            causas = ollama_causas(engine.avaliacao.to_dict())
            engine.avaliacao.possiveis_causas = causas
        except Exception:
            engine.avaliacao.possiveis_causas = ["Consulte um médico para avaliação diagnóstica."]
    else:
        engine.avaliacao.possiveis_causas = ["Consulte um médico para avaliação diagnóstica."]

    return jsonify(engine.avaliacao.to_dict())


if __name__ == "__main__":
    print("Servidor rodando em http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
