# clint-sdr-bot/README.md

# Clint SDR Bot

This project is an automated Sales Development Representative (SDR) integration within the Clint CRM. It is designed to read specific chats, listen to audio messages, and respond automatically using an OpenAI bot persona.

## Project Structure

```
clint-sdr-bot
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── responder.py
│   ├── graphql.py
│   ├── audio_handler.py
│   ├── pdf_reader.py
│   └── config.py
├── .env
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Set Up Environment**:
   - Create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```
       source venv/bin/activate
       ```
   - Install the dependencies:
     ```
     pip install -r requirements.txt
     ```

2. **Configure API Keys**:
   - Fill in the `.env` file with your Clint API URL, Clint token, and OpenAI API key:
     ```
     CLINT_API_URL=https://app.clint.digital/api/graphql
     CLINT_TOKEN=your_clint_token
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

- Run the application by executing the `main.py` file:
  ```
  python src/main.py
  ```

## Functionality

- **Message Handling**: The bot fetches unread messages from the Clint CRM.
- **Audio Processing**: It can transcribe audio messages using the Whisper model.
- **PDF Processing**: It can read and extract text from PDF files.
- **Response Generation**: The bot generates empathetic and strategic responses using the OpenAI API.

## Testing

- Test the integration by sending messages through the Clint CRM and observing the bot's responses. Adjust the logic in `responder.py` to refine the bot's persona and response style.

## Iteration

- Based on testing feedback, iterate on the bot's response logic to better match your desired communication style.

For further guidance on specific parts of the implementation or additional features, please specify your needs.