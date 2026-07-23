import json
import sys
import os

from triage import (
    TriageEngine,
    NivelRisco,
    detectar_emergencia_texto,
)

try:
    from ollama_client import gerar_possiveis_causas
    OLLAMA_DISPONIVEL = True
except Exception:
    OLLAMA_DISPONIVEL = False


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def input_sim_nao(pergunta):
    while True:
        r = input(f"{pergunta} (s/n): ").strip().lower()
        if r in ("s", "sim"):
            return True
        if r in ("n", "nao", "não"):
            return False
        print("Responda com 's' ou 'n'.")


def input_numero(pergunta, funcao=float, min_v=None, max_v=None):
    while True:
        try:
            r = input(f"{pergunta}: ").strip().replace(",", ".")
            if not r:
                return None
            v = funcao(r)
            if min_v is not None and v < min_v:
                print(f"Valor mínimo é {min_v}.")
                continue
            if max_v is not None and v > max_v:
                print(f"Valor máximo é {max_v}.")
                continue
            return v
        except ValueError:
            print("Valor inválido. Digite um número.")


def etapa_identificacao(engine):
    print("\n" + "=" * 50)
    print("ETAPA 1 — IDENTIFICAÇÃO")
    print("=" * 50)

    engine.avaliacao.paciente.nome = input("Nome completo: ").strip()
    engine.avaliacao.paciente.idade = input_numero("Idade", int, 0, 150)

    while True:
        s = input("Sexo (M/F): ").strip().upper()
        if s in ("M", "F"):
            engine.avaliacao.paciente.sexo = s
            break
        print("Responda M ou F.")

    engine.avaliacao.paciente.peso = input_numero(
        "Peso (kg) — opcional, Enter para pular", float, 0, 500
    )
    engine.avaliacao.paciente.altura = input_numero(
        "Altura (cm) — opcional, Enter para pular", float, 0, 250
    )


def etapa_historico(engine):
    print("\n" + "=" * 50)
    print("ETAPA 2 — HISTÓRICO DE SAÚDE")
    print("=" * 50)
    print("Informe se possui ou não as condições abaixo:")

    h = engine.avaliacao.historico
    h.diabetes = input_sim_nao("Diabetes?")
    h.hipertensao = input_sim_nao("Hipertensão?")
    h.asma = input_sim_nao("Asma?")
    h.cardiopatia = input_sim_nao("Doença cardíaca?")
    h.doenca_pulmonar = input_sim_nao("Doença pulmonar?")
    h.doenca_renal = input_sim_nao("Doença renal?")

    if engine.avaliacao.paciente.sexo == "F":
        h.gravidez = input_sim_nao("Está grávida?")

    alergias = input("Alergias (separadas por vírgula) — Enter se não tiver: ").strip()
    if alergias:
        h.alergias = [a.strip() for a in alergias.split(",")]

    medicamentos = input(
        "Medicamentos de uso contínuo (separados por vírgula) — Enter se não usar: "
    ).strip()
    if medicamentos:
        h.medicamentos = [m.strip() for m in medicamentos.split(",")]

    cirurgias = input(
        "Cirurgias recentes (separadas por vírgula) — Enter se não teve: "
    ).strip()
    if cirurgias:
        h.cirurgias_recentes = [c.strip() for c in cirurgias.split(",")]


def verificar_emergencia(engine, texto):
    if detectar_emergencia_texto(texto):
        engine.avaliacao.emergencia = True
        engine.avaliacao.motivo_emergencia = texto
        return True
    return False


def etapa_sintomas(engine):
    print("\n" + "=" * 50)
    print("ETAPA 3 — SINTOMAS")
    print("=" * 50)

    sintomas_relatados = input(
        "Descreva seus sintomas principais (ex.: dor, febre, tosse, falta de ar...): "
    ).strip()
    engine.avaliacao.sintomas.append(sintomas_relatados)

    if verificar_emergencia(engine, sintomas_relatados):
        return

    t = sintomas_relatados.lower()

    if "febre" in t:
        temp = input_numero(
            "Temperatura (opcional, Enter se não sabe) — ex.: 38.5", float, 34, 43
        )
        if temp:
            engine.avaliacao.sinais_vitais.temperatura = temp
        dias = input_numero("Há quantos dias está com febre?", int, 0, 60)
        if dias:
            engine.dados_febre["dias"] = dias

    if "dor" in t:
        parte = input("Em qual parte do corpo? ").strip()
        engine.dados_dor["local"] = parte
        intensidade = input_numero(
            "Intensidade da dor (0 a 10, Enter se não sabe)", int, 0, 10
        )
        if intensidade is not None:
            engine.dados_dor["intensidade"] = intensidade

        if engine.dados_dor["intensidade"] is not None:
            engine.avaliacao.sintomas.append(
                f"dor {engine.dados_dor.get('local', '')} intensidade {engine.dados_dor['intensidade']}/10"
            )

        if "peito" in t or "peito" in parte.lower() or "torácica" in t:
            print("\n--- Sobre a dor no peito ---")
            irradia = input(
                "A dor irradia para braço, costas ou mandíbula? (s/n): "
            ).strip().lower() in ("s", "sim")
            suando = input("Está suando? (s/n): ").strip().lower() in ("s", "sim")
            falta_ar = input("Está com falta de ar? (s/n): ").strip().lower() in (
                "s",
                "sim",
            )
            engine.dados_dor_peito["irradia"] = irradia
            engine.dados_dor_peito["suando"] = suando
            engine.dados_dor_peito["falta_ar"] = falta_ar

            if engine.dados_dor.get("intensidade", 0) >= 7 or (
                irradia and (suando or falta_ar)
            ):
                engine.avaliacao.emergencia = True
                engine.avaliacao.motivo_emergencia = (
                    "Dor no peito com sinais de alerta"
                )
                return

    if "falta de ar" in t or "falta" in t or "respir" in t:
        frases = input("Consegue falar frases completas ou precisa pausar? ").strip()
        repouso = input("A falta de ar ocorre mesmo em repouso? (s/n): ").strip().lower() in ("s", "sim")
        engine.dados_falta_ar["repouso"] = repouso
        if repouso or "não" in frases.lower() or "pausa" in frases.lower():
            engine.dados_falta_ar["grave"] = True
            engine.avaliacao.emergencia = True
            engine.avaliacao.motivo_emergencia = "Falta de ar grave"
            return
        engine.dados_falta_ar["moderada"] = True

    if "tosse" in t:
        tipo = input("Tosse seca ou com catarro? ").strip().lower()
        engine.dados_tosse["tipo"] = tipo

    if "vômit" in t or "vomit" in t or "enjo" in t:
        vezes = input_numero(
            "Quantas vezes vomitou nas últimas 24h (Enter se não sabe)?", int, 0, 100
        )
        if vezes and vezes > 5:
            engine.dados_vomitos["frequente"] = True
        else:
            engine.dados_vomitos["frequente"] = False
        agua = input("Consegue beber água sem vomitar? (s/n): ").strip().lower() in (
            "s",
            "sim",
        )
        if not agua:
            engine.dados_vomitos["frequente"] = True

    if "diarreia" in t or "diarréia" in t:
        sangue = input("Há sangue nas fezes? (s/n): ").strip().lower() in ("s", "sim")
        engine.dados_diarreia["com_sangue"] = sangue
        vezes = input_numero("Quantas evacuações por dia?", int, 0, 100)
        if vezes and vezes > 6:
            engine.dados_diarreia["frequente"] = True


def etapa_tempo_sintomas(engine):
    print("\n" + "=" * 50)
    print("ETAPA 4 — TEMPO DOS SINTOMAS")
    print("=" * 50)
    engine.avaliacao.tempo_sintomas = input(
        "Há quanto tempo os sintomas começaram? (ex.: 2 dias, 5 horas, 1 semana): "
    ).strip()


def etapa_sinais_vitais(engine):
    print("\n" + "=" * 50)
    print("ETAPA 5 — SINAIS VITAIS (opcional)")
    print("=" * 50)
    print("Se tiver os equipamentos em casa, me informe. Senão, pressione Enter.")

    sv = engine.avaliacao.sinais_vitais

    t = input_numero("Temperatura (°C) — Enter para pular", float, 34, 43)
    if t is not None:
        sv.temperatura = t

    pa = input("Pressão arterial (ex.: 120/80) — Enter para pular: ").strip()
    if pa:
        match = __import__("re").match(r"(\d+)\s*/\s*(\d+)", pa)
        if match:
            sv.pressao_sistolica = int(match.group(1))
            sv.pressao_diastolica = int(match.group(2))
        else:
            print("Formato inválido. Use ex.: 120/80")

    fc = input_numero(
        "Frequência cardíaca (bpm) — Enter para pular", int, 30, 250
    )
    if fc is not None:
        sv.frequencia_cardiaca = fc

    sat = input_numero(
        "Saturação de oxigênio (%) — Enter para pular", int, 50, 100
    )
    if sat is not None:
        sv.saturacao = sat


def gerar_possiveis_causas_ollama(engine):
    if not OLLAMA_DISPONIVEL:
        engine.avaliacao.possiveis_causas = [
            "Módulo Ollama não disponível. Consulte um médico para avaliação."
        ]
        return

    if not engine.avaliacao.emergencia:
        print("\nConsultando modelo local (phi3:mini) para possíveis causas...")
        try:
            causas = gerar_possiveis_causas(engine.avaliacao.to_dict())
            engine.avaliacao.possiveis_causas = causas
        except Exception as e:
            engine.avaliacao.possiveis_causas = [
                f"Erro ao consultar Ollama: {e}"
            ]
    else:
        engine.avaliacao.possiveis_causas = [
            "Emergência identificada. Priorizar atendimento de urgência."
        ]


def resultado_final(engine):
    print("\n" + "=" * 50)
    print("RESULTADO DA TRIAGEM")
    print("=" * 50)

    dados = engine.avaliacao.to_dict()
    print(json.dumps(dados, ensure_ascii=False, indent=2))

    arquivo = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "resultado_triagem.json"
    )
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"\nResultado salvo em: {arquivo}")

    if engine.avaliacao.emergencia:
        print("\n🚨 EMERGÊNCIA DETECTADA!")
        print(f"Motivo: {engine.avaliacao.motivo_emergencia}")
    print(f"Nível de risco: {engine.avaliacao.nivel_risco.value}")
    print(f"Prioridade: {engine.avaliacao.prioridade.value}")
    print(f"\n{engine.avaliacao.explicacao}")
    print(f"\nORIENTAÇÃO: {engine.avaliacao.orientacao}")


def main():
    limpar_tela()
    print("=" * 50)
    print("SISTEMA DE TRIAGEM MÉDICA")
    print("Assistente de Classificação de Risco")
    print("=" * 50)
    print(
        "\nEste sistema auxilia na triagem inicial de pacientes.\nNão substitui avaliação médica profissional."
    )
    input("\nPressione Enter para iniciar...")

    engine = TriageEngine()

    etapa_identificacao(engine)

    if not engine.avaliacao.emergencia:
        etapa_historico(engine)

    if not engine.avaliacao.emergencia:
        etapa_sintomas(engine)

    if not engine.avaliacao.emergencia:
        etapa_tempo_sintomas(engine)

    if not engine.avaliacao.emergencia:
        etapa_sinais_vitais(engine)

    engine.classificar()
    gerar_possiveis_causas_ollama(engine)
    resultado_final(engine)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTriagem interrompida pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        sys.exit(1)
