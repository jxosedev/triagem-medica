import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from triage import TriageEngine, NivelRisco

# Teste 1: Paciente com sintomas leves
def test_sintomas_leves():
    e = TriageEngine()
    e.avaliacao.paciente.nome = "Maria"
    e.avaliacao.paciente.idade = 30
    e.avaliacao.paciente.sexo = "F"
    e.avaliacao.sintomas = ["dor de garganta leve", "coriza"]
    e.classificar()
    assert e.avaliacao.nivel_risco == NivelRisco.VERDE, f"Esperado VERDE, obteve {e.avaliacao.nivel_risco}"
    print(f"[OK] Teste 1 - Sintomas leves: {e.avaliacao.nivel_risco.value} -> {e.avaliacao.explicacao}")

# Teste 2: Febre alta
def test_febre_alta():
    e = TriageEngine()
    e.avaliacao.paciente.idade = 40
    e.avaliacao.sintomas = ["febre", "dor no corpo"]
    e.avaliacao.sinais_vitais.temperatura = 39.5
    e.dados_dor["intensidade"] = 3
    e.classificar()
    assert e.avaliacao.nivel_risco == NivelRisco.AMARELO, f"Esperado AMARELO, obteve {e.avaliacao.nivel_risco}"
    print(f"[OK] Teste 2 - Febre alta: {e.avaliacao.nivel_risco.value} -> {e.avaliacao.explicacao}")

# Teste 3: Emergência - saturação baixa
def test_emergencia_saturacao():
    e = TriageEngine()
    e.avaliacao.paciente.idade = 60
    e.avaliacao.sintomas = ["falta de ar"]
    e.avaliacao.sinais_vitais.saturacao = 85
    e.classificar()
    assert e.avaliacao.nivel_risco == NivelRisco.VERMELHO, f"Esperado VERMELHO, obteve {e.avaliacao.nivel_risco}"
    assert e.avaliacao.emergencia, "Deveria ser emergência"
    print(f"[OK] Teste 3 - Saturação baixa (emergência): {e.avaliacao.nivel_risco.value}")

# Teste 4: Dor no peito com irradiação
def test_dor_peito():
    e = TriageEngine()
    e.avaliacao.paciente.idade = 55
    e.avaliacao.sintomas = ["dor no peito"]
    e.dados_dor["intensidade"] = 8
    e.dados_dor_peito["irradia"] = True
    e.dados_dor_peito["suando"] = True
    e.dados_dor_peito["falta_ar"] = False
    e.avaliacao.emergencia = True
    e.avaliacao.motivo_emergencia = "Dor no peito com sinais de alerta"
    e.classificar()
    assert e.avaliacao.nivel_risco == NivelRisco.VERMELHO, f"Esperado VERMELHO, obteve {e.avaliacao.nivel_risco}"
    print(f"[OK] Teste 4 - Dor no peito (emergência): {e.avaliacao.nivel_risco.value}")

# Teste 5: Paciente idoso com comorbidades
def test_idoso_comorbidades():
    e = TriageEngine()
    e.avaliacao.paciente.idade = 70
    e.avaliacao.historico.cardiopatia = True
    e.avaliacao.historico.diabetes = True
    e.avaliacao.sintomas = ["tosse persistente", "cansaço"]
    e.avaliacao.sinais_vitais.temperatura = 38.0
    e.dados_dor["intensidade"] = 2
    e.dados_tosse["tipo"] = "seca"
    e.classificar()
    assert e.avaliacao.nivel_risco == NivelRisco.AMARELO, f"Esperado AMARELO, obteve {e.avaliacao.nivel_risco}"
    print(f"[OK] Teste 5 - Idoso com comorbidades: {e.avaliacao.nivel_risco.value} -> {e.avaliacao.explicacao}")

# Teste 6: Dor abdominal intensa
def test_dor_abdominal():
    e = TriageEngine()
    e.avaliacao.paciente.idade = 35
    e.avaliacao.sintomas = ["dor abdominal forte"]
    e.dados_dor["intensidade"] = 9
    e.classificar()
    assert e.avaliacao.nivel_risco == NivelRisco.LARANJA, f"Esperado LARANJA, obteve {e.avaliacao.nivel_risco}"
    print(f"[OK] Teste 6 - Dor abdominal intensa: {e.avaliacao.nivel_risco.value}")

# Teste 7: Pressão arterial muito alta
def test_pressao_alta():
    e = TriageEngine()
    e.avaliacao.paciente.idade = 50
    e.avaliacao.historico.hipertensao = True
    e.avaliacao.sintomas = ["dor de cabeça", "tontura"]
    e.avaliacao.sinais_vitais.pressao_sistolica = 190
    e.avaliacao.sinais_vitais.pressao_diastolica = 110
    e.dados_dor["intensidade"] = 4
    e.classificar()
    assert e.avaliacao.nivel_risco == NivelRisco.LARANJA, f"Esperado LARANJA, obteve {e.avaliacao.nivel_risco}"
    print(f"[OK] Teste 7 - Pressão alta: {e.avaliacao.nivel_risco.value} -> {e.avaliacao.explicacao}")

# Teste 8: Vômitos frequentes
def test_vomitos():
    e = TriageEngine()
    e.avaliacao.paciente.idade = 25
    e.avaliacao.sintomas = ["vômitos", "náusea"]
    e.dados_vomitos["frequente"] = True
    e.dados_dor["intensidade"] = 3
    e.classificar()
    assert e.avaliacao.nivel_risco == NivelRisco.AMARELO, f"Esperado AMARELO, obteve {e.avaliacao.nivel_risco}"
    print(f"[OK] Teste 8 - Vômitos frequentes: {e.avaliacao.nivel_risco.value}")

# Teste 9: Diarreia com sangue
def test_diarreia_sangue():
    e = TriageEngine()
    e.avaliacao.paciente.idade = 40
    e.avaliacao.sintomas = ["diarreia"]
    e.dados_diarreia["com_sangue"] = True
    e.dados_dor["intensidade"] = 5
    e.classificar()
    assert e.avaliacao.nivel_risco == NivelRisco.LARANJA, f"Esperado LARANJA, obteve {e.avaliacao.nivel_risco}"
    print(f"[OK] Teste 9 - Diarreia com sangue: {e.avaliacao.nivel_risco.value}")

# Teste 10: Detecção de emergência por texto
def test_deteccao_texto():
    from triage import detectar_emergencia_texto
    assert detectar_emergencia_texto("tive uma convulsão agora")
    assert detectar_emergencia_texto("sangramento intenso na perna")
    assert detectar_emergencia_texto("perdi a consciência por alguns segundos")
    assert not detectar_emergencia_texto("estou com febre e dor de cabeça")
    assert not detectar_emergencia_texto("tosse seca há 3 dias")
    print("[OK] Teste 10 - Detecção de emergência por texto")


tests = [
    test_sintomas_leves,
    test_febre_alta,
    test_emergencia_saturacao,
    test_dor_peito,
    test_idoso_comorbidades,
    test_dor_abdominal,
    test_pressao_alta,
    test_vomitos,
    test_diarreia_sangue,
    test_deteccao_texto,
]

for t in tests:
    try:
        t()
    except Exception as e:
        print(f"[FALHOU] {t.__name__}: {e}")
        import traceback
        traceback.print_exc()

print("\n--- Todos os testes concluídos ---")
