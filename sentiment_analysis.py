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