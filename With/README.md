# Bot WhatsApp + OpenAI

## Descrição
Este projeto integra o WhatsApp Business Cloud (via Make) com a OpenAI para responder automaticamente clientes, simulando o atendimento do Gabriel.

## Estrutura de Diretórios

```
With/
├── main.py
├── memory.py
├── prompt.py
├── requirements.txt
├── .env
├── README.md
└── Dados/
    ├── audio.wav
    ├── documento.pdf
    └── imagem.png
```

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/Gabriel-Brina/VS-Code.git
   cd VS-Code/With
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
   Ou manualmente:
   ```
   pip install flask openai python-dotenv
   ```

## Configuração

1. Crie um arquivo `.env` na raiz do diretório `With/` com:
   ```
   OPENAI_API_KEY=sua_chave_openai
   ```

## Execução

1. Execute o bot (dentro da pasta With):
   ```
   python main.py
   ```
2. Em outro terminal, rode o ngrok:
   ```
   ngrok http 5000
   ```
3. Copie a URL gerada pelo ngrok e configure no Make (módulo HTTP).
4. No Make, use a URL do ngrok para enviar requisições POST para o endpoint `/webhook` do seu bot.
5. No Make, use o módulo **Watch Messages** do WhatsApp Business Cloud para receber mensagens e o módulo **Send a Message** para responder.

## Segurança

- O arquivo `.env` está protegido pelo `.gitignore` e não será enviado ao GitHub.
- Nunca compartilhe suas chaves de API.

## Funcionamento

- O bot recebe mensagens do WhatsApp via Make (Watch Messages).
- Gera respostas automáticas usando a OpenAI.
- Envia as respostas de volta para o WhatsApp via Make.

## Autor

Gabriel Brina