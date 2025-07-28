import os
import openai
from dotenv import load_dotenv
from data_loader import carregar_conversas, carregar_pdfs, carregar_audios_txt

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

exemplos_conversas = carregar_conversas()
exemplos_audios = carregar_audios_txt()
exemplos_pdfs = carregar_pdfs()

def gerar_resposta(input_usuario, nome="Gabriel"):
    exemplos = "\n\n".join(exemplos_conversas[:2] + exemplos_audios[:1])
    contexto_pdf = "\n\n".join(exemplos_pdfs[:1])

    prompt = f"""
Você é Gabriel, um SDR especialista. Responda sempre como Gabriel, usando seu estilo, vocabulário e abordagem, conforme os exemplos abaixo.

Exemplos de conversas reais:
{exemplos}

Informações de referência:
{contexto_pdf}

Mensagem recebida:
\"\"\"{input_usuario}\"\"\"

Responda de forma personalizada, natural e alinhada ao estilo dos exemplos, como Gabriel faria.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message["content"]

if __name__ == "__main__":
    print("Inicie a conversa com o bot Gabriel! (Digite 'sair' para encerrar)\n")
    while True:
        entrada = input("Cliente: ")
        if entrada.lower() == "sair":
            break
        resposta = gerar_resposta(entrada)
        print(f"Gabriel: {resposta}\n")