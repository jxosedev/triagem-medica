import json
import urllib.request
import urllib.error


OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO = "phi3:mini"


def gerar_possiveis_causas(dados_avaliacao):
    prompt = f"""
Com base nos dados abaixo, liste as POSSÍVEIS CAUSAS para os sintomas.
NÃO dê diagnóstico definitivo. Use linguagem como "possível causa", "pode estar relacionado a".

Dados do paciente:
- Idade: {dados_avaliacao['paciente']['idade']}
- Sexo: {dados_avaliacao['paciente']['sexo']}
- Sintomas: {', '.join(dados_avaliacao['sintomas'])}
- Tempo dos sintomas: {dados_avaliacao['tempo_sintomas']}
- Histórico: {json.dumps(dados_avaliacao['historico'], ensure_ascii=False)}
- Sinais vitais: {json.dumps(dados_avaliacao['sinais_vitais'], ensure_ascii=False)}

Responda APENAS com um array JSON de strings, sem texto extra:
["possível causa 1", "possível causa 2", ...]
"""

    payload = json.dumps(
        {
            "model": MODELO,
            "messages": [{"role": "user", "content": prompt.strip()}],
            "stream": False,
        }
    ).encode("utf-8")

    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result["message"]["content"].strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[-1]
                content = content.rsplit("```", 1)[0]
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return [content]
    except (urllib.error.URLError, ConnectionRefusedError):
        return [
            "Não foi possível conectar ao modelo local. Verifique se o Ollama está rodando."
        ]
    except Exception as e:
        return [f"Erro ao consultar Ollama: {str(e)}"]
