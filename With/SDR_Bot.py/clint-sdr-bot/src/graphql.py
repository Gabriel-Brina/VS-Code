import os
import requests
from dotenv import load_dotenv

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

# Acesse as variáveis de ambiente
CLINT_API_URL = os.getenv("CLINT_API_URL")
CLINT_TOKEN = os.getenv("CLINT_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {CLINT_TOKEN}",
    "Content-Type": "application/json"
}

def buscar_mensagens_novas():
    query = """
    {
        mensagensNaoRespondidas {
            id
            tipo
            conteudo
            url_audio
            url_pdf
            nome_contato
            contato_id
        }
    }
    """
    response = requests.post(CLINT_API_URL, json={"query": query}, headers=HEADERS)
    data = response.json()
    mensagens = []
    for m in data["data"]["mensagensNaoRespondidas"]:
        mensagens.append({
            "id": m["id"],
            "tipo": m["tipo"],
            "conteudo": m["conteudo"],
            "url_audio": m.get("url_audio"),
            "url_pdf": m.get("url_pdf"),
            "nome_contato": m["nome_contato"],
            "contato_id": m["contato_id"]
        })
    return mensagens

def enviar_resposta(contato_id, mensagem):
    mutation = """
    mutation($contatoId: ID!, $mensagem: String!) {
        enviarMensagem(contatoId: $contatoId, mensagem: $mensagem) {
            sucesso
        }
    }
    """
    variables = {
        "contatoId": contato_id,
        "mensagem": mensagem
    }
    response = requests.post(CLINT_API_URL, json={"query": mutation, "variables": variables}, headers=HEADERS)
    return response.json()