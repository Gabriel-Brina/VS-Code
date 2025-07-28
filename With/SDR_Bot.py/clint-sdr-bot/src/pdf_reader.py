import requests
import tempfile
import PyPDF2
import os
from dotenv import load_dotenv

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

# Acesse as variáveis de ambiente
MINHA_API_KEY = os.getenv("MINHA_API_KEY")

def ler_pdf(url):
    # Baixe o conteúdo do PDF da URL
    response = requests.get(url)
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
        temp.write(response.content)
        temp.seek(0)

        # Leia o conteúdo do PDF
        pdf_reader = PyPDF2.PdfReader(temp)
        texto = "\n\n".join(page.extract_text() or "" for page in pdf_reader.pages)

    # Aqui você pode adicionar a lógica para usar a chave da API da Mistral, se necessário
    # Por exemplo, enviar o texto para a API da Mistral para processamento adicional

    return texto