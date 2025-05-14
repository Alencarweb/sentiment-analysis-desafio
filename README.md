# 📚 **Tutorial: Análise de Sentimentos com Azure AI**

Este guia educativo explica como criar um projeto de **Análise de Sentimentos** utilizando os serviços de **Azure AI Speech** e **Azure AI Language**. Vamos passar pelo processo passo a passo, desde a configuração no Azure até a implementação do código em Python.  

---

## 🎯 **Objetivo do Projeto**
Criar um sistema que:  
✅ Converte **áudio em texto** com o **Azure AI Speech**  
✅ Analisa **sentimentos** em textos usando o **Azure AI Language**  
✅ Gera relatórios estruturados dos resultados  

---

# 🔹 **1️⃣ Criar e Configurar Recursos no Azure**

## 🌐 **Criando um Recurso de Fala (Speech Service)**
O **Azure AI Speech** permite a conversão de áudio em texto. Para configurá-lo:

1. **Acesse o [Azure Speech Studio](https://speech.microsoft.com/)** e faça login.  
2. Vá até **Configurações → Criar um recurso**.  
3. Configure:  
   - **Nome:** Nome único do recurso  
   - **Assinatura:** Selecione sua assinatura do Azure  
   - **Região:** Escolha uma região suportada  
   - **Nível de preço:** **F0 (grátis)** ou **S0 (pago)**  
   - **Grupo de Recursos:** Selecione um existente ou crie um novo  
4. Clique em **Criar recurso** e aguarde a ativação.  

## 📝 **Testando a Conversão de Áudio em Texto**
1. **Baixe** [este arquivo de áudio](https://aka.ms/mslearn-speech-files).  
2. Vá até **Speech to Text** e clique em **Try out Real-time speech to text**.  
3. Selecione o arquivo **WhatAICanDo.m4a**.  
4. O serviço transcreverá o áudio e mostrará o texto convertido.  

---

## 🧠 **Criando um Recurso de Análise de Sentimentos (Language Service)**
1. **Acesse o [Portal do Azure](https://portal.azure.com/)** e faça login.  
2. Clique em **+ Criar um recurso** e pesquise por **Serviço de Idioma**.  
3. Clique em **Criar** e configure:  
   - **Assinatura:** Selecione sua assinatura  
   - **Grupo de recursos:** Escolha ou crie um  
   - **Região:** Escolha a mais próxima (Ex: East US 2)  
   - **Nome:** Nome único  
   - **Nível de preço:** **F0 (grátis)** ou **S (pago)**  
4. Clique em **Revisar + Criar** e depois **Criar**.  

## 🔬 **Testando a Análise de Sentimentos**
1. Acesse o [Language Studio](https://language.cognitive.azure.com/).  
2. No menu **Classificar Texto**, clique em **Analisar Sentimento e Extrair Opiniões**.  
3. Insira frases como:  
   ```
   O hotel era ótimo, mas o serviço foi ruim.
   A comida estava deliciosa e o ambiente incrível!
   ```
4. Execute e veja os **níveis de positividade, neutralidade e negatividade**.  

---

# 🖥 **2️⃣ Criando o Código em Python**

## 📂 **Estrutura do Projeto**
📁 **sentiment-analysis**  
├── 📂 inputs  
│   ├── sentencas.txt _(Arquivo com frases para análise)_  
├── 📂 outputs  
│   ├── resultados.json _(Arquivo gerado com os resultados)_  
├── 📜 .env _(Credenciais do Azure)_  
├── 📜 sentiment_analysis.py _(Script principal)_  
├── 📜 README.md _(Documentação do projeto)_  

---

## 📌 **1. Criando o Ambiente Virtual**
```bash
python -m venv venv  
source venv/bin/activate  # Linux/Mac  
venv\Scripts\activate     # Windows
```

## 📌 **2. Instalando as Dependências**
```bash
pip install requests python-dotenv
```

## 📌 **3. Configurando as Credenciais do Azure**
Crie um arquivo `.env` e adicione:

```dotenv
AZURE_ENDPOINT="https://<seu-endpoint>.cognitiveservices.azure.com/"  
AZURE_KEY="<sua-chave>"  
AZURE_REGION="<sua-região>"
```

---

## 📝 **4. Criando o Script `sentiment_analysis.py`**
Este código lê frases, envia para o Azure AI Language e salva os resultados.

```python
import os
import json
import requests
from dotenv import load_dotenv

def load_env():
    """Carrega as variáveis de ambiente do arquivo .env"""
    load_dotenv()
    return {
        "endpoint": os.getenv("AZURE_ENDPOINT"),
        "key": os.getenv("AZURE_KEY"),
        "region": os.getenv("AZURE_REGION")
    }

def analyze_sentiment(text, config):
    """Envia uma requisição para a API de análise de sentimentos do Azure."""
    url = f"{config['endpoint']}/text/analytics/v3.1/sentiment"
    headers = {
        "Ocp-Apim-Subscription-Key": config["key"],
        "Content-Type": "application/json"
    }
    payload = {
        "documents": [{"id": "1", "language": "pt", "text": text}]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

def process_input_file(input_file, output_file, config):
    """Lê um arquivo de texto e analisa os sentimentos de cada linha."""
    results = []
    
    with open(input_file, "r", encoding="utf-8") as file:
        sentences = file.readlines()
    
    for sentence in sentences:
        result = analyze_sentiment(sentence.strip(), config)
        results.append({"sentence": sentence.strip(), "analysis": result})
    
    with open(output_file, "w", encoding="utf-8") as out_file:
        json.dump(results, out_file, indent=4, ensure_ascii=False)
    
    print(f"Análise concluída! Resultados salvos em {output_file}")

if __name__ == "__main__":
    config = load_env()
    input_path = "inputs/sentencas.txt"
    output_path = "outputs/resultados.json"
    
    os.makedirs("outputs", exist_ok=True)
    
    print("Iniciando análise de sentimentos...")
    process_input_file(input_path, output_path, config)
    print("Processo finalizado. Confira os resultados no diretório 'outputs'.")
```

---

## 📌 **5. Criando um Arquivo de Entrada**
Crie o arquivo `inputs/sentencas.txt` e adicione frases:

```
Eu amo este produto!
O serviço foi muito ruim.
Estou muito feliz com a compra.
A experiência foi péssima.
```

---

## ▶ **6. Executando o Script**
```bash
python sentiment_analysis.py
```
Isso gerará um arquivo `outputs/resultados.json` com:

```json
[
    {
        "sentence": "Eu amo este produto!",
        "analysis": {
            "sentiment": "positive",
            "confidenceScores": {"positive": 0.99, "neutral": 0.01, "negative": 0.00}
        }
    }
]
```

---

# 🔄 **3️⃣ Subindo o Projeto para o GitHub**
1. Crie um **repositório no GitHub**.  
2. No terminal, rode:
   ```bash
   git init
   git add .
   git commit -m "Projeto de Análise de Sentimentos com Azure AI"
   git branch -M main
   git remote add origin https://github.com/seu-usuario/seu-repositorio.git
   git push -u origin main
   ```

---

# 🚀 **4️⃣ Insights e Próximos Passos**
✅ Automação para análise de sentimentos em redes sociais  
✅ Integração com **chatbots e assistentes virtuais**  
✅ Criação de **dashboards para visualização de sentimentos**  

Agora você tem um sistema funcional de **Análise de Sentimentos com Azure AI**! 🔥🚀# sentiment-analysis-desafio