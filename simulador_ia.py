REGRAS_SINTOMAS = {
    "febre": {
        "causas": [
            "Infecção viral (gripe, resfriado comum)",
            "Infecção bacteriana",
            "Reação inflamatória",
        ],
        "associados": {
            "tosse": ["Infecção respiratória", "Pneumonia", "Bronquite"],
            "dor de cabeça": ["Enxaqueca febril", "Sinusite", "Gripe"],
            "dor no corpo": ["Dengue", "Gripe forte", "Infecção viral sistêmica"],
            "mal estar": ["Infecção viral", "Mononucleose", "Infecção urinária"],
            "calafrios": ["Malária", "Infecção bacteriana grave", "Sepse inicial"],
            "sudorese": ["Infecção viral", "Climatérico", "Hipoglicemia"],
        },
        "por_idade": {
            "crianca": ["Dengue", "Gripe", "Infecção respiratória aguda"],
            "idoso": ["Pneumonia", "Infecção urinária", "Infecção bacteriana"],
        },
    },
    "tosse": {
        "causas": [
            "Infecção respiratória superior",
            "Irritação das vias aéreas",
            "Resfriado comum",
        ],
        "associados": {
            "febre": ["Gripe", "COVID-19", "Pneumonia"],
            "catarro": ["Bronquite", "Pneumonia bacteriana", "Sinusite crônica"],
            "falta de ar": ["Asma", "Bronquite", "Pneumonia"],
            "dor no peito": ["Bronquite", "Pleurite", "Pneumonia"],
            "chiado": ["Asma", "DPOC", "Bronquite obstrutiva"],
        },
    },
    "dor de cabeça": {
        "causas": [
            "Enxaqueca",
            "Cefaleia tensional",
            "Sinusite",
        ],
        "associados": {
            "febre": ["Gripe", "Sinusite", "Meningite"],
            "visão turva": ["Enxaqueca com aura", "Hipertensão arterial", "Crise hipertensiva"],
            "náusea": ["Enxaqueca", "Hipertensão", "Concussão"],
            "rigidez no pescoço": ["Meningite", "Tensão muscular", "Hérnia de disco cervical"],
        },
    },
    "dor no corpo": {
        "causas": [
            "Dor muscular por esforço",
            "Fibromialgia",
            "Infecção viral sistêmica",
        ],
        "associados": {
            "febre": ["Dengue", "Zika", "Chikungunya", "Gripe"],
            "fadiga": ["Fibromialgia", "Síndrome de fadiga crônica", "Hipotireoidismo"],
            "edema": ["Lesão articular", "Artrite", "Insuficiência venosa"],
        },
    },
    "dor abdominal": {
        "causas": [
            "Gastroenterite",
            "Indigestão",
            "Cólica intestinal",
        ],
        "associados": {
            "vômito": ["Gastroenterite aguda", "Intoxicação alimentar", "Apendicite"],
            "diarreia": ["Gastroenterite", "Infecção intestinal", "Síndrome do intestino irritável"],
            "febre": ["Apendicite", "Diverticulite", "Infecção urinária com complicação"],
            "inchaço": ["Obstrução intestinal", "Ascite", "Gases intestinais"],
            "urinar": ["Infecção urinária", "Cálculo renal", "Cistite"],
        },
    },
    "dor no peito": {
        "causas": [
            "Dor muscular esquelética",
            "Ansiedade/ataque de pânico",
            "Refluxo gastroesofágico",
        ],
        "associados": {
            "falta de ar": ["Infarto do miocárdio", "Embolia pulmonar", "Pneumotórax"],
            "suando": ["Infarto do miocárdio", "Crise hipertensiva", "Sepse"],
            "irradia": ["Infarto do miocárdio", "Diseção aórtica", "Pericardite"],
            "tosse": ["Pneumonia", "Pleurite", "Embolia pulmonar"],
        },
    },
    "falta de ar": {
        "causas": [
            "Crise de ansiedade",
            "Asma",
            "Bronquite",
        ],
        "associados": {
            "febre": ["Pneumonia", "COVID-19", "Bronquite aguda"],
            "chiado": ["Asma", "DPOC", "Edema pulmonar"],
            "dor no peito": ["Embolia pulmonar", "Pneumotórax", "Pneumonia"],
            "inchaço nas pernas": ["Insuficiência cardíaca", "Embolia pulmonar", "DPOC avançada"],
        },
    },
    "vômito": {
        "causas": [
            "Gastroenterite",
            "Intoxicação alimentar",
            "Náusea gestacional",
        ],
        "associados": {
            "diarreia": ["Gastroenterite viral", "Infecção bacteriana intestinal", "Toxinfecção alimentar"],
            "febre": ["Gastroenterite", "Apendicite", "Meningite"],
            "dor abdominal": ["Apendicite", "Obstrução intestinal", "Pancreatite"],
            "tontura": ["Labirintite", "Vertigem", "Desidratação"],
        },
    },
    "diarreia": {
        "causas": [
            "Gastroenterite viral",
            "Síndrome do intestino irritável",
            "Má absorção intestinal",
        ],
        "associados": {
            "febre": ["Infecção bacteriana", "Dissenteria", "Parasitose"],
            "sangue": ["Colite", "Hemorragia digestiva", "Dissenteria bacilar"],
            "dor abdominal": ["Enterite", "Doença inflamatória intestinal", "Apendicite"],
            "deshidratação": ["Cólera", "Gastroenterite grave", "Rotavírus"],
        },
    },
    "tontura": {
        "causas": [
            "Labirintite",
            "Hipoglicemia",
            "Desidratação",
        ],
        "associados": {
            "dor de cabeça": ["Enxaqueca vestibular", "Hipertensão", "TIA"],
            "náusea": ["Labirintite", "Vertigem posicional", "Concussão"],
            "zumbido no ouvido": ["Tinnitus", "Otite média", "Presbioacusia"],
            "visão turva": ["Hipertensão", "AVC", "Crise hipoglicêmica"],
        },
    },
    "dor de garganta": {
        "causas": [
            "Faringite viral",
            "Amigdalite",
            "Laringite",
        ],
        "associados": {
            "febre": ["Amigdalite bacteriana", "Mononucleose", "Faringite estreptocócica"],
            "tosse": ["Laringite", "Faringite", "COVID-19"],
            "manchas brancas": ["Amigdalite bacteriana", "Mononucleose", "Abscesso periamigdaliano"],
        },
    },
    "dor nas costas": {
        "causas": [
            "Contractura muscular",
            "Hérnia de disco",
            "Lombalgia mecânica",
        ],
        "associados": {
            "dor na perna": ["Ciática", "Hérnia de disco lombar", "Estenose espinal"],
            "dormência": ["Hérnia de disco", "Neuropatia periférica", "Estenose espinal"],
            "febre": ["Abscesso epidural", "Osteomielite", "Infecção renal"],
        },
    },
    "dor articular": {
        "causas": [
            "Artrite reumatoide",
            "Osteoartrose",
            "Gota",
        ],
        "associados": {
            "inchaço": ["Artrite", "Bursite", "Lesão ligamentar"],
            "vermelhidão": ["Gota", "Artrite séptica", "Celulite"],
            "rigidez matinal": ["Artrite reumatoide", "Lupus", "Fibromialgia"],
        },
    },
    "coceira": {
        "causas": [
            "Dermatite de contato",
            "Reação alérgica",
            "Xerose cutânea",
        ],
        "associados": {
            "manchas na pele": ["Urticária", "Eczema", "Psoríase"],
            "inchaço": ["Angioedema", "Reação alérgica sistêmica", "Celulite"],
        },
    },
    "dor no ouvido": {
        "causas": [
            "Otite média",
            "Otite externa",
            "Dor referida da mandíbula",
        ],
        "associados": {
            "febre": ["Otite média aguda", "Mastoidite", "Otite externa complicada"],
            "perda auditiva": ["Otite média com efusão", "Otosclerose", "Perda auditiva súbita"],
            "drenagem": ["Otite média perforada", "Otite externa", "Trauma timpânico"],
        },
    },
}


def _classificar_idade(idade):
    if idade <= 12:
        return "crianca"
    elif idade >= 60:
        return "idoso"
    return "adulto"


def _analisar_sintomas(texto):
    texto_lower = texto.lower()
    sintomas_encontrados = []
    for sintoma in REGRAS_SINTOMAS:
        if sintoma in texto_lower:
            sintomas_encontrados.append(sintoma)
    return sintomas_encontrados


def _buscar_causas(sintomas_texto, dados):
    texto_lower = sintomas_texto.lower()
    paciente = dados.get("paciente", {})
    idade = int(paciente.get("idade", 0) or 0)
    sexo = paciente.get("sexo", "")
    historico = dados.get("historico", {})

    causas_todas = []
    causas_por_sintoma = {}

    sintomas_encontrados = _analisar_sintomas(texto_lower)

    for sintoma in sintomas_encontrados:
        regra = REGRAS_SINTOMAS[sintoma]

        for causa in regra.get("causas", []):
            if causa not in causas_todas:
                causas_todas.append(causa)
            if sintoma not in causas_por_sintoma:
                causas_por_sintoma[sintoma] = []
            if causa not in causas_por_sintoma[sintoma]:
                causas_por_sintoma[sintoma].append(causa)

        for associado, causas_assoc in regra.get("associados", {}).items():
            if associado in texto_lower:
                for causa in causas_assoc:
                    if causa not in causas_todas:
                        causas_todas.append(causa)

        faixa = _classificar_idade(idade)
        causas_idade = regra.get("por_idade", {}).get(faixa, [])
        for causa in causas_idade:
            if causa not in causas_todas:
                causas_todas.append(causa)

    if "febre" in texto_lower and "tosse" in texto_lower:
        extras = ["COVID-19", "Pneumonia atípica", "Bronquiolite"]
        for e in extras:
            if e not in causas_todas:
                causas_todas.append(e)

    if "dor" in texto_lower and "peito" in texto_lower and "falta de ar" in texto_lower:
        extras = ["Infarto agudo do miocárdio", "Embolia pulmonar"]
        for e in extras:
            if e not in causas_todas:
                causas_todas.append(e)

    if "diarreia" in texto_lower and "sangue" in texto_lower:
        extras = ["Colite ulcerativa", "Doença de Crohn", "Dissenteria"]
        for e in extras:
            if e not in causas_todas:
                causas_todas.append(e)

    if "vômit" in texto_lower and "dor abdominal" in texto_lower:
        if "gravidez" in str(historico).lower() or historico.get("gravidez"):
            extras = ["Hiperêmese gravídica", "Pré-eclâmpsia"]
        else:
            extras = ["Apendicite aguda", "Pancreatite"]
        for e in extras:
            if e not in causas_todas:
                causas_todas.append(e)

    if "tontura" in texto_lower and "dor de cabeça" in texto_lower:
        extras = ["Crise hipertensiva", "AVC isquêmico", "Enxaqueca vestibular"]
        for e in extras:
            if e not in causas_todas:
                causas_todas.append(e)

    sinais = dados.get("sinais_vitais", {})
    if isinstance(sinais, dict):
        temp = sinais.get("temperatura")
        saturacao = sinais.get("saturacao")
    else:
        temp = None
        saturacao = None

    if temp:
        try:
            t = float(temp)
            if t >= 39.5 and "Pneumonia" not in causas_todas:
                causas_todas.insert(0, "Pneumonia")
        except (ValueError, TypeError):
            pass

    if saturacao:
        try:
            s = int(saturacao)
            if s < 92 and "Insuficiência respiratória" not in causas_todas:
                causas_todas.insert(0, "Insuficiência respiratória aguda")
        except (ValueError, TypeError):
            pass

    if not causas_todas:
        causas_todas = [
            "Condição autolimitada",
            "Possível infecção viral leve",
        ]

    return causas_todas[:4]


def gerar_possiveis_causas(dados_avaliacao):
    sintomas = dados_avaliacao.get("sintomas", [])
    texto_sintomas = " ".join(sintomas) if isinstance(sintomas, list) else str(sintomas)
    tempo = dados_avaliacao.get("tempo_sintomas", "")

    if tempo:
        texto_sintomas += f" há {tempo}"

    causas = _buscar_causas(texto_sintomas, dados_avaliacao)

    return causas
