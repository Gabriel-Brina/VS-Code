import os
from dotenv import load_dotenv
from graphql import buscar_mensagens_novas, enviar_resposta
from responder import gerar_resposta
from audio_handler import transcrever_audio
from pdf_reader import ler_pdf
import os
from dotenv import load_dotenv

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

# Acesse as variáveis de ambiente
CLINT_API_URL = os.getenv("CLINT_API_URL")
CLINT_BOT_KEY = os.getenv("CLINT_BOT_KEY")
CLINT_TOKEN = os.getenv("CLINT_TOKEN")

# Exemplo de uso das variáveis de ambiente
print(f"CLINT_API_URL: {CLINT_API_URL}")
print(f"CLINT_BOT_KEY: {CLINT_BOT_KEY}")
print(f"CLINT_TOKEN: {CLINT_TOKEN}")

# Inicialize o bot com as variáveis de ambiente
minha_api_client = MinhaIABot(api_key=CLINT_BOT_KEY)

def loop_automacao():
    mensagens = buscar_mensagens_novas()
    for msg in mensagens:
        conteudo = msg.get('conteudo', '')

        if msg['tipo'] == 'audio':
            conteudo = transcrever_audio(msg['url_audio'])
        elif msg['tipo'] == 'pdf':
            conteudo = ler_pdf(msg['url_pdf'])

        resposta = gerar_resposta(conteudo, msg.get('nome_contato', 'Cliente'))
        enviar_resposta(msg['contato_id'], resposta)

if __name__ == "__main__":
    loop_automacao()