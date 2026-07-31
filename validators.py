VALID_SEXOS = ["M", "F", "O"]
VALID_NIVEIS_RISCO = ["VERDE", "AMARELO", "LARANJA", "VERMELHO"]


def validar_paciente(paciente):
    erros = []

    if not paciente.get("nome"):
        erros.append("Nome é obrigatório")

    idade = paciente.get("idade", 0)
    if not idade or idade < 0 or idade > 150:
        erros.append("Idade inválida")

    sexo = paciente.get("sexo", "")
    if sexo and sexo not in VALID_SEXOS:
        erros.append(f"Sexo deve ser um de: {VALID_SEXOS}")

    peso = paciente.get("peso", 0)
    if peso and (peso < 0 or peso > 500):
        erros.append("Peso inválido")

    altura = paciente.get("altura", 0)
    if altura and (altura < 0 or altura > 300):
        erros.append("Altura inválida")

    return erros


def validar_sintomas(sintomas):
    erros = []

    if not sintomas.get("descricao"):
        erros.append("Descrição dos sintomas é obrigatória")

    temperatura = sintomas.get("temperatura", "")
    if temperatura:
        try:
            temp = float(temperatura)
            if temp < 30 or temp > 45:
                erros.append("Temperatura fora do range válido (30-45°C)")
        except ValueError:
            erros.append("Temperatura deve ser um número")

    saturacao = sintomas.get("sv_saturacao", "")
    if saturacao:
        try:
            sat = int(saturacao)
            if sat < 0 or sat > 100:
                erros.append("Saturação deve estar entre 0-100%")
        except ValueError:
            erros.append("Saturação deve ser um número")

    return erros


def validar_dados_triagem(dados):
    erros = []

    if not dados:
        return ["Dados não fornecidos"]

    paciente = dados.get("paciente", {})
    erros.extend(validar_paciente(paciente))

    sintomas = dados.get("sintomas", {})
    erros.extend(validar_sintomas(sintomas))

    return erros
