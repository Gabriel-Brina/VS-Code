import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcrever_audios(pasta="../dados"):
    saida = []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".mp3") or arquivo.endswith(".wav"):
            caminho = os.path.join(pasta, arquivo)
            with open(caminho, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
                saida.append(transcript["text"])
    # Salva tudo em audios_txt.txt
    with open(os.path.join(pasta, "audios_txt.txt"), "w", encoding="utf-8") as f:
        f.write("\n\n".join(saida))

if __name__ == "__main__":
    transcrever_audios()