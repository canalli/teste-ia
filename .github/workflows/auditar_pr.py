import os
import re
import requests

# Configurações Locais
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "qwen2.5-coder:1.5b"  # Ajuste para o seu modelo ou Persona do Open WebUI

# Variáveis do GitHub Actions
GITHUB_TOKEN = os.getenv("INPUT_GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

def obter_codigo_alterado():
    if os.path.exists("pr.diff"):
        with open("pr.diff", "r", encoding="utf-8") as f:
            return f.read()
    return None

def analisar_com_ia(codigo_diff):
    # Ajustamos o prompt para garantir que a IA use termos exatos fáceis de rastrear por código
    prompt = f"""Você é um especialista em DevSecOps e auditoria de código. 
Analise o seguinte arquivo de 'diff' (linhas alteradas em um Pull Request) em busca de falhas graves de segurança (OWASP Top 10).

Para cada vulnerabilidade encontrada, você DEVE incluir obrigatoriamente a linha de classificação exatamente neste formato:
- **Severidade:** CRÍTICA
- **Severidade:** ALTA
- **Severidade:** MÉDIA
- **Severidade:** BAIXA

Seja direto e apresente o resultado estruturado em tópicos Markdown.

Código Diff para Análise:
{codigo_diff}"""
    
    payload = {"model": MODELO, "prompt": prompt, "stream": False}
    resposta = requests.post(OLLAMA_URL, json=payload).json()
    return resposta.get("response")

def calcular_resumo_criticidade(parecer_ia):
    """
    Usa Expressões Regulares (Regex) para rastrear e contar as marcações de severidade
    geradas pela IA, ignorando diferenças de maiúsculas/minúsculas ou acentuação.
    """
    # Converte para maiúsculo para simplificar a busca
    texto_processado = parecer_ia.upper()
    
    # Padrões de busca regex para identificar as tags da IA
    criticas = len(re.findall(r'SEVERIDADE:\s*\*?\*?CRÍ|CRITICA', texto_processado))
    altas = len(re.findall(r'SEVERIDADE:\s*\*?\*?ALTA', texto_processado))
    medias = len(re.findall(r'SEVERIDADE:\s*\*?\*?MÉD|MEDIA', texto_processado))
    baixas = len(re.findall(r'SEVERIDADE:\s*\*?\*?BAIXA', texto_processado))
    
    total = criticas + altas + medias + baixas
    
    # Se nenhuma vulnerabilidade foi achada pelas tags, define um bloco padrão amigável
    if total == 0 and ("NENHUMA VULNERABILIDADE" in texto_processado or "CÓDIGO SEGURO" in texto_processado):
        bloco_resumo = "### 🎉 Resumo de Segurança\n- **Status:** 🛡️ Nenhum risco crítico detectado nas linhas analisadas!\n\n"
        return bloco_resumo

    # Monta uma tabela visual em Markdown para o topo do comentário do GitHub
    bloco_resumo = f"""### 📊 Painel de Vulnerabilidades Encontradas

| Nível de Risco | Quantidade Detectada |
| :--- | :---: |
| 🔴 **CRÍTICA** | {criticas} |
| 🟠 **ALTA** | {altas} |
| 🟡 **MÉDIA** | {medias} |
| 🟢 **BAIXA** | {baixas} |
| **TOTAL** | **{total}** |

---
"""
    return bloco_resumo

def postar_comentario_no_github(comentario_final):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comentario_final}
    requests.post(url, headers=headers, json=data)

if __name__ == "__main__":
    diff = obter_codigo_alterado()
    if diff and len(diff.strip()) > 0:
        print("🔍 Analisando alterações com o Ollama...")
        parecer_ia = analisar_com_ia(diff)
        
        print("📊 Calculando métricas de criticidade...")
        tabela_resumo = calcular_resumo_criticidade(parecer_ia)
        
        # Consolida a tabela resumo ANTES do texto explicativo da IA
        comentario_final = f"## 🤖 Parecer do WAP DevSecOps Copilot\n\n{tabela_resumo}{parecer_ia}"
        
        print("✉️ Enviando relatório consolidado para o GitHub...")
        postar_comentario_no_github(comentario_final)
    else:
        print("ℹ️ Nenhuma alteração significativa detectada no código.")
