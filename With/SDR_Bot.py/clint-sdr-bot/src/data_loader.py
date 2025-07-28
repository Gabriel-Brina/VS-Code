import os
import PyPDF2

def carregar_conversas(arquivo="../dados/conversas.txt"):
    exemplos = []
    if os.path.exists(arquivo):
        with open(arquivo, encoding="utf-8") as f:
            texto = f.read()
            exemplos = [bloco.strip() for bloco in texto.split("\n\n") if bloco.strip()]
    return exemplos

def carregar_audios_txt(arquivo="../dados/audios_txt.txt"):
    exemplos = []
    if os.path.exists(arquivo):
        with open(arquivo, encoding="utf-8") as f:
            texto = f.read()
            exemplos = [bloco.strip() for bloco in texto.split("\n\n") if bloco.strip()]
    return exemplos

def carregar_pdfs():
    pasta = os.path.join(os.path.dirname(__file__), '..', 'dados', 'pdfs')
    pasta = os.path.abspath(pasta)
    exemplos_pdfs = []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.pdf') or arquivo.endswith('.txt'):
            with open(os.path.join(pasta, arquivo), 'r', encoding='utf-8') as f:
                exemplos_pdfs.append(f.read())
    return exemplos_pdfs