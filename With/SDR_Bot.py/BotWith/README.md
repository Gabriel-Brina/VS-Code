# 🤖 BotWith - Gabriel AI SDR

Sistema de automação SDR com IA, treinamento personalizado e integração Clint.

## ✨ O que faz

- **Chat inteligente**: Responde como SDR experiente
- **Treinamento simples**: Aprende com suas conversas  
- **Multimodal**: Processa texto, áudio, imagem, documentos
- **Integração Clint**: Conecta com seu CRM

## 🚀 Como usar

### 1. Instalar dependências
```bash
python setup.py
```

### 2. Treinar o Gabriel
```bash
python run_upload.py
```
- Edite `data/mensagens_simples.txt` com suas conversas
- Use formato: `cliente: "pergunta"` e `gabriel: "resposta"`

### 3. Testar no terminal  
```bash
python terminal_bot.py
cd "c:\Users\gabri\OneDrive\Geral\Programação\VSCode\With\SDR_Bot.py\BotWith"
# Para testar respostas específicas:
C:/Users/gabri/OneDrive/Geral/Programação/VSCode/venv/Scripts/python.exe test_responses.py

# Para usar o terminal bot interativo:
C:/Users/gabri/OneDrive/Geral/Programação/VSCode/venv/Scripts/python.exe terminal_bot.py
```

### 4. Integrar com Clint
- Configure `.env` com suas chaves
- Gabriel processará leads automaticamente

## 📁 Arquivos importantes

- **`terminal_bot.py`** - Chat para testar
- **`run_upload.py`** - Treinar com suas mensagens  
- **`data/mensagens_simples.txt`** - Suas conversas de treinamento
- **`config.py`** - Configurações gerais
- **`setup.py`** - Script de instalação

## 💡 Dica rápida

1. Execute `python setup_simples.py` para instalar tudo
2. Copie suas melhores conversas como SDR
3. Cole em `mensagens_simples.txt` no formato cliente/gabriel
4. Execute `python run_upload.py` e teste com `python terminal_bot.py`
5. Gabriel responderá como você!

---

**Gabriel AI** - Seu clone digital de SDR 🚀
