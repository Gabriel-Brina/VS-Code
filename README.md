# Bot Clint + OpenAI

## Descrição
Este projeto integra a API da Clint (GraphQL) com a OpenAI para responder automaticamente clientes, simulando o atendimento do Gabriel.

## Instalação

1. Clone o repositório: https://github.com/Gabriel-Brina/VS-Code.git

2. Instale as dependências: pip install -r requirements.txt
    Ou instale manualmente: pip install openai gql python-dotenv requests

## Configuração

1. Crie um arquivo `.env` na raiz do projeto com: OPENAI_API_KEY=sua_chave_openai CLINT_API_KEY=sua_chave_clint

## Execução

1. Execute o bot: python main.py

## Segurança

- O arquivo `.env` está protegido pelo `.gitignore` e não será enviado ao GitHub.
- Nunca compartilhe suas chaves de API.

## Funcionamento

- O bot busca mensagens via GraphQL na Clint.
- Gera respostas automáticas usando a OpenAI.
- Envia as respostas de volta para a Clint.

## Autor

Gabriel Brina