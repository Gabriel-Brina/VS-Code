from flask import Flask, request, jsonify
import openai
from memory import Memory
from prompt import build_dynamic_prompt
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
memory = Memory()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    user_id = data.get('usuario')
    user_message = data.get('mensagem')

    # Comando para corrigir a última resposta
    if user_message.startswith('/corrigir '):
        correcao = user_message.replace('/corrigir ', '', 1)
        memory.corrigir_ultima_resposta(user_id, correcao)
        return jsonify({"resposta": "Resposta corrigida e salva!"})

    # Comando para atualizar prompt
    if user_message.startswith('/prompt '):
        novo_prompt = user_message.replace('/prompt ', '', 1)
        memory.set_prompt(user_id, novo_prompt)
        return jsonify({"resposta": "Prompt atualizado!"})

    # Validação básica dos campos esperados
    if not user_id or not user_message:
        return jsonify({"erro": "Campos 'usuario' e 'mensagem' são obrigatórios."}), 400

    # Atualiza o histórico de conversa
    memory.update_conversation_history(user_id, {"role": "user", "content": user_message})

    # Exemplo de atualização de estado (pode expandir conforme regras do seu bot)
    if "me chamo" in user_message.lower():
        nome = user_message.split("me chamo")[-1].strip().split()[0]
        memory.set_client_detail(user_id, "nome_cliente", nome)
    # Adicione outras regras para atualizar situacao, area, etc.

    # Monta o prompt dinâmico
    state = memory.get_state(user_id)
    history = memory.get_conversation_history(user_id)
    prompt = build_dynamic_prompt(state, history)

    # Chamada para OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        assistant_message = response.choices[0].message.content
    except Exception as e:
        return jsonify({"erro": f"Erro ao chamar OpenAI: {str(e)}"}), 500

    # Salva a resposta no histórico
    memory.update_conversation_history(user_id, {"role": "assistant", "content": assistant_message})

    # Retorna a resposta para o Make enviar ao WhatsApp
    return jsonify({"resposta": assistant_message})

if __name__ == "__main__":
    app.run()