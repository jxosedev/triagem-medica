# SIS-TRIAGEM — Sistema de Classificação de Risco Médico com IA

Sistema de triagem médica virtual que auxilia na classificação inicial de risco de pacientes antes do atendimento por um profissional de saúde.

> **Aviso:** Este é um sistema de apoio à decisão. Não substitui avaliação médica profissional. Em caso de emergência, ligue SAMU 192.

---

## Funcionalidades

- **Triagem interativa** com formulário passo a passo (web) ou conversacional (terminal)
- **Detecção automática de emergências** — sintomas críticos interrompem a entrevista e classificam como VERMELHO
- **Classificação de risco** em 4 níveis:
  - **VERDE** — Baixa urgência (UBS / consulta agendada)
  - **AMARELO** — Urgência moderada (atendimento em horas)
  - **LARANJA** — Alta prioridade (atendimento imediato)
  - **VERMELHO** — Emergência (SAMU 192 / hospital)
- **Análise por pontuação** considerando: intensidade da dor, temperatura, saturação, pressão arterial, comorbidades, idade, gravidez
- **Possíveis causas** geradas via modelo local (Ollama phi3:mini) quando disponível
- **Interface web** responsiva com design hospitalar, painel de monitor com cores dinâmicas, animação ECG, sidebar do paciente e relógio ao vivo
- **Interface CLI** para uso em terminal
- **Saída em JSON** padronizada para integração com outros sistemas

---

## Estrutura do Projeto

```
triagem-medica/
├── app.py              # Servidor Flask (interface web)
├── triage.py           # Motor de triagem (classificação de risco)
├── ollama_client.py    # Integração com Ollama (LLM local)
├── main.py             # Interface CLI (terminal)
├── test_triage.py      # Testes automatizados (10 cenários)
├── templates/
│   └── index.html      # Frontend web (HTML/CSS/JS)
├── .gitignore
└── README.md
```

---

## Requisitos

- Python 3.10+
- Flask
- (Opcional) [Ollama](https://ollama.com/) com modelo `phi3:mini` para geração de possíveis causas

---

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/jxosedev/triagem-medica.git
cd triagem-medica

# Instalar dependências
pip install flask
```

---

## Execução

### Interface Web (recomendado)

```bash
python app.py
```

Acesse http://localhost:5000 no navegador.

### Interface Terminal (CLI)

```bash
python main.py
```

---

## Uso com Ollama (opcional)

Para que o sistema sugira **possíveis causas** usando IA local:

1. Instale o [Ollama](https://ollama.com/)
2. Baixe o modelo: `ollama pull phi3:mini`
3. Certifique-se de que o Ollama está rodando em `localhost:11434`
4. Inicie o sistema normalmente — ele detectará o Ollama automaticamente

---

## Classificação de Risco

| Nível | Cor | Urgência | Orientação |
|-------|-----|----------|------------|
| VERDE | ![#2e7d32](https://via.placeholder.com/12/2e7d32/000000?text=+) | Baixa | UBS / consulta agendada |
| AMARELO | ![#f57f17](https://via.placeholder.com/12/f57f17/000000?text=+) | Moderada | Atendimento nas próximas horas |
| LARANJA | ![#e65100](https://via.placeholder.com/12/e65100/000000?text=+) | Alta | Emergência hospitalar imediata |
| VERMELHO | ![#c62828](https://via.placeholder.com/12/c62828/000000?text=+) | Emergência | SAMU 192 / hospital mais próximo |

### Sintomas que classificam como EMERGÊNCIA (VERMELHO)

- Dor intensa no peito
- Falta de ar grave
- Convulsão
- Perda de consciência
- Sangramento intenso
- Saturação abaixo de 90%
- Confusão mental
- Fraqueza súbita em um lado do corpo
- Dificuldade para falar
- Queimaduras extensas
- Trauma grave
- Tentativa de suicídio
- Reação alérgica grave

---

## API

O servidor Flask expõe um endpoint:

```
POST /api/triagem
Content-Type: application/json
```

**Exemplo de requisição:**

```json
{
  "paciente": {
    "nome": "João Silva",
    "idade": 45,
    "sexo": "M",
    "peso": 80,
    "altura": 175
  },
  "historico": {
    "diabetes": true,
    "hipertensao": false,
    "asma": false,
    "cardiopatia": false,
    "doenca_pulmonar": false,
    "doenca_renal": false,
    "gravidez": false,
    "alergias": "",
    "medicamentos": "metformina 500mg",
    "cirurgias": ""
  },
  "sintomas": {
    "descricao": "febre e tosse há 3 dias",
    "temperatura": "38.5",
    "febre_dias": "3",
    "tempo": "3 dias"
  }
}
```

**Exemplo de resposta:**

```json
{
  "paciente": { "nome": "João Silva", "idade": 45, "sexo": "M" },
  "nivel_risco": "AMARELO",
  "prioridade": "MODERADA",
  "explicacao": "URGÊNCIA MODERADA (AMARELO). febre alta, tosse, comorbidade(s) presente(s).",
  "orientacao": "Procure atendimento médico nas PRÓXIMAS HORAS.",
  "possiveis_causas": ["Infecção respiratória", "Gripe"],
  "emergencia": false,
  "necessita_hospital": true,
  "confianca": 0.85
}
```

---

## Testes

```bash
python test_triage.py
```

Executa 10 cenários automatizados cobrindo: sintomas leves, febre alta, saturação baixa, dor no peito, idoso com comorbidades, dor abdominal, pressão alta, vômitos, diarreia com sangue e detecção de emergência por texto.

---

## Tecnologias

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **IA (opcional):** Ollama + phi3:mini
- **Testes:** Python (asserts)

---

## Licença

MIT
