import os
from dotenv import load_dotenv
import openai
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
clint_api_key = os.getenv("CLINT_API_KEY")

# Configuração do transporte GraphQL
transport = RequestsHTTPTransport(
    url="https://app.clint.digital/chat",  # Substitua pela URL correta da Clint
    headers={"Authorization": f"Bearer {clint_api_key}"},
    use_json=True,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

def gerar_resposta(mensagem_cliente):
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é Gabriel, um atendente simpático."},
            {"role": "user", "content": mensagem_cliente}
        ]
    )
    return resposta.choices[0].message['content']

query = gql("""
query contactByPk($idCONTACT_BY_PK: uuid!)  {
  contact_by_pk(id: $idCONTACT_BY_PK){
    id
    name
    email
    ddi
    phone
    avatar
    fields
    created_at
    valid_phone
    chat_count
    instagram{
      id
      username
      follower_count
      is_verified_user
    }
    deals(where: {origin:{archived_at:{_is_null:true}},deleted_at:{_is_null:true},archived_at:{_is_null:true},archived_by:{_is_null:true}} ){
      id
      fields
      stage
      stage_id
      status
      user_id
      lost_status_id
      created_at
      archived
      origin_id
      deleted_at
      contact_id
      pos
      pos_id
      stage_item{
        id
        label
      }
      origin{
        archived_at
        currency
        group{
          currency
        }
        owner{
          currency
        }
      }
    }
    tags{
      id
      tag_id
      tags_config{
        id
        name
        color
      }
    }
    organization{
      id
      name
      fields
    }
    validation_meta
  }
}
""")

params = {"idCONTACT_BY_PK": "coloque_o_id_aqui"}
result = client.execute(query, variable_values=params)
contato = result["contact_by_pk"]
print(contato)
for mensagem in result["messages"]:
    resposta = gerar_resposta(mensagem["text"])
    # Exemplo de mutação para enviar resposta
    mutation = gql("""
    mutation sendMessage($id: ID!, $text: String!) {
      sendMessage(id: $id, text: $text) {
        success
      }
    }
    """)
    params = {"id": mensagem["id"], "text": resposta}
    client.execute(mutation, variable_values=params)