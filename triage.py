import json
import re
from enum import Enum


class NivelRisco(Enum):
    VERDE = "VERDE"
    AMARELO = "AMARELO"
    LARANJA = "LARANJA"
    VERMELHO = "VERMELHO"


class Prioridade(Enum):
    BAIXA = "BAIXA"
    MODERADA = "MODERADA"
    ALTA = "ALTA"
    EMERGENCIA = "EMERGENCIA"


SINTOMAS_EMERGENCIA = [
    "dor intensa no peito",
    "falta de ar grave",
    "convulsão",
    "perda de consciência",
    "sangramento intenso",
    "confusão mental",
    "fraqueza súbita",
    "dificuldade para falar",
    "queimaduras extensas",
    "trauma grave",
    "tentativa de suicídio",
    "reação alérgica grave",
    "choque elétrico",
    "afogamento",
]


def detectar_emergencia_texto(texto):
    t = texto.lower()
    for s in SINTOMAS_EMERGENCIA:
        if s in t:
            return True

    padroes_adicionais = [
        ("consciência", "perda de consciência"),
        ("consciencia", "perda de consciência"),
        ("desmaio", "perda de consciência"),
        ("desmaiou", "perda de consciência"),
        ("convulsão", "convulsão"),
        ("convulsao", "convulsão"),
        ("hemorragia", "sangramento intenso"),
        ("desorientado", "confusão mental"),
        ("desorientada", "confusão mental"),
        ("paralis", "fraqueza súbita"),
        ("entorpecimento", "fraqueza súbita"),
        ("formigamento", "fraqueza súbita"),
    ]
    for palavra, emergencia in padroes_adicionais:
        if palavra in t:
            return True
    return False


class Paciente:
    def __init__(self):
        self.nome = ""
        self.idade = 0
        self.sexo = ""
        self.peso = 0
        self.altura = 0

    def preenchido(self):
        return bool(self.nome and self.idade and self.sexo)

    def to_dict(self):
        return {
            "nome": self.nome,
            "idade": self.idade,
            "sexo": self.sexo,
            "peso": self.peso,
            "altura": self.altura,
        }


class Historico:
    def __init__(self):
        self.diabetes = False
        self.hipertensao = False
        self.asma = False
        self.cardiopatia = False
        self.doenca_pulmonar = False
        self.doenca_renal = False
        self.gravidez = False
        self.alergias = []
        self.medicamentos = []
        self.cirurgias_recentes = []

    def to_dict(self):
        return {
            "diabetes": self.diabetes,
            "hipertensao": self.hipertensao,
            "asma": self.asma,
            "cardiopatia": self.cardiopatia,
            "doenca_pulmonar": self.doenca_pulmonar,
            "doenca_renal": self.doenca_renal,
            "gravidez": self.gravidez,
            "alergias": self.alergias,
            "medicamentos": self.medicamentos,
            "cirurgias_recentes": self.cirurgias_recentes,
        }


class SinaisVitais:
    def __init__(self):
        self.temperatura = None
        self.pressao_sistolica = None
        self.pressao_diastolica = None
        self.frequencia_cardiaca = None
        self.saturacao = None


class Avaliacao:
    def __init__(self):
        self.paciente = Paciente()
        self.historico = Historico()
        self.sintomas = []
        self.sinais_vitais = SinaisVitais()
        self.tempo_sintomas = ""
        self.emergencia = False
        self.motivo_emergencia = ""
        self.nivel_risco = NivelRisco.VERDE
        self.prioridade = Prioridade.BAIXA
        self.possiveis_causas = []
        self.explicacao = ""
        self.orientacao = ""
        self.necessita_hospital = False
        self.confianca = 0.0

    def to_dict(self):
        pa = None
        if self.sinais_vitais.pressao_sistolica:
            pa = f"{self.sinais_vitais.pressao_sistolica}/{self.sinais_vitais.pressao_diastolica}"
        return {
            "paciente": self.paciente.to_dict(),
            "historico": self.historico.to_dict(),
            "sintomas": self.sintomas,
            "tempo_sintomas": self.tempo_sintomas,
            "sinais_vitais": {
                "temperatura": self.sinais_vitais.temperatura,
                "pressao_arterial": pa,
                "frequencia_cardiaca": self.sinais_vitais.frequencia_cardiaca,
                "saturacao": self.sinais_vitais.saturacao,
            },
            "nivel_risco": self.nivel_risco.value,
            "prioridade": self.prioridade.value,
            "possiveis_causas": self.possiveis_causas,
            "explicacao": self.explicacao,
            "orientacao": self.orientacao,
            "necessita_hospital": self.necessita_hospital,
            "emergencia": self.emergencia,
            "confianca": self.confianca,
        }


class TriageEngine:
    def __init__(self):
        self.avaliacao = Avaliacao()
        self.dados_dor = {}
        self.dados_febre = {}
        self.dados_tosse = {}
        self.dados_falta_ar = {}
        self.dados_vomitos = {}
        self.dados_diarreia = {}
        self.dados_dor_peito = {}

    def classificar(self):
        a = self.avaliacao

        if a.emergencia:
            a.nivel_risco = NivelRisco.VERMELHO
            a.prioridade = Prioridade.EMERGENCIA
            a.necessita_hospital = True
            a.confianca = 0.98
            a.orientacao = "LIGUE IMEDIATAMENTE para o SAMU (192) ou vá ao hospital mais próximo. Não espere."
            a.explicacao = f"EMERGÊNCIA (VERMELHO). Motivo: {a.motivo_emergencia}."
            return

        sat = a.sinais_vitais.saturacao
        if sat is not None and sat < 90:
            a.emergencia = True
            a.motivo_emergencia = "Saturação de oxigênio abaixo de 90%"
            self.classificar()
            return

        laranja = False
        motivos_laranja = []

        if sat is not None and 90 <= sat <= 94:
            laranja = True
            motivos_laranja.append("saturação entre 90% e 94%")

        sist = a.sinais_vitais.pressao_sistolica
        diast = a.sinais_vitais.pressao_diastolica
        if sist is not None and (sist >= 180 or diast >= 110):
            laranja = True
            motivos_laranja.append("pressão arterial muito elevada")

        temp = a.sinais_vitais.temperatura
        if temp is not None and temp >= 40:
            laranja = True
            motivos_laranja.append("febre muito alta")

        if self.dados_dor.get("intensidade", 0) >= 8:
            laranja = True
            motivos_laranja.append("dor intensa")

        if self.dados_falta_ar.get("moderada"):
            laranja = True
            motivos_laranja.append("falta de ar moderada")

        if self.dados_diarreia.get("com_sangue"):
            laranja = True
            motivos_laranja.append("diarreia com sangue")

        if temp is not None and temp >= 39:
            if a.paciente.idade >= 60 or a.historico.cardiopatia or a.historico.diabetes:
                laranja = True
                motivos_laranja.append("febre alta associada a fatores de risco")

        if laranja:
            a.nivel_risco = NivelRisco.LARANJA
            a.prioridade = Prioridade.ALTA
            a.necessita_hospital = True
            a.confianca = 0.9
            a.explicacao = (
                "ALTA PRIORIDADE (LARANJA). "
                + ". ".join(motivos_laranja)
                + "."
            )
            a.orientacao = "Procure atendimento médico IMEDIATAMENTE. Vá a uma emergência hospitalar agora."
            return

        score = 0
        fatores = []

        if temp is not None and temp >= 39:
            score += 3
            fatores.append("febre alta")
        elif temp is not None and temp >= 37.5:
            score += 2
            fatores.append("febre")

        dor_int = self.dados_dor.get("intensidade", 0)
        if 5 <= dor_int <= 7:
            score += 2
            fatores.append("dor moderada")
        elif 1 <= dor_int <= 4:
            score += 1
            fatores.append("dor leve")

        if self.dados_vomitos.get("frequente"):
            score += 3
            fatores.append("vômitos frequentes")

        if self.dados_diarreia.get("frequente"):
            score += 2
            fatores.append("diarreia frequente")

        if self.dados_falta_ar.get("leve"):
            score += 2
            fatores.append("falta de ar leve")

        if self.dados_tosse.get("tipo"):
            score += 1
            fatores.append("tosse")

        num_comorb = 0
        if a.historico.cardiopatia:
            num_comorb += 1
        if a.historico.diabetes:
            num_comorb += 1
        if a.historico.hipertensao:
            num_comorb += 1
        if a.historico.asma:
            num_comorb += 1
        if a.historico.doenca_pulmonar:
            num_comorb += 1
        if a.historico.doenca_renal:
            num_comorb += 1

        if num_comorb > 0:
            score += num_comorb
            fatores.append(f"comorbidade(s) presente(s)")

        if a.paciente.idade >= 65:
            score += 1
            fatores.append("idade avançada")

        if a.historico.gravidez:
            score += 1
            fatores.append("gestante")

        if self.dados_vomitos.get("frequente") is False:
            if not self.avaliacao.historico.gravidez:
                pass

        if score >= 3:
            a.nivel_risco = NivelRisco.AMARELO
            a.prioridade = Prioridade.MODERADA
            a.necessita_hospital = True
            a.confianca = 0.85
            a.orientacao = "Procure atendimento médico nas PRÓXIMAS HORAS. Vá a uma UPA ou pronto-socorro."
        else:
            a.nivel_risco = NivelRisco.VERDE
            a.prioridade = Prioridade.BAIXA
            a.necessita_hospital = False
            a.confianca = 0.8
            a.orientacao = "Pode procurar uma Unidade Básica de Saúde (UBS) ou agendar consulta. Não há urgência."

        if not fatores:
            fatores.append("sintomas leves sem fatores de risco relevantes")

        nivel_nome = a.nivel_risco.value
        if a.nivel_risco == NivelRisco.AMARELO:
            prefixo = "URGÊNCIA MODERADA (AMARELO)"
        else:
            prefixo = "BAIXA URGÊNCIA (VERDE)"
        a.explicacao = f"{prefixo}. " + ", ".join(fatores) + "."
