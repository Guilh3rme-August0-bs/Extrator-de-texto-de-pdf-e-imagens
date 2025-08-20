import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import shutil
import ctypes
import sys
import subprocess

# ---------------------------
# Elevação para Administrador
# ---------------------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def win_quote(s: str) -> str:
    """Coloca entre aspas se necessário (para caminhos com espaços)."""
    return f'"{s}"' if any(c in s for c in ' \t"') else s

if not is_admin():
    print("Reiniciando com privilégios de administrador...")
    try:
        script_path = os.path.abspath(__file__)
        # Preserva argumentos passados ao script
        extra_args = " ".join(win_quote(a) for a in sys.argv[1:])
        # Monta a linha de comando para o cmd manter a janela aberta (/k)
        cmdline = f'/k {win_quote(sys.executable)} {win_quote(script_path)} {extra_args}'.strip()

        # Abre um novo cmd elevado e executa o script
        subprocess.run([
            "powershell",
            "-NoProfile",
            "Start-Process", "cmd",
            "-ArgumentList", cmdline,
            "-Verb", "runAs"
        ])
    except Exception as e:
        print(f"Não foi possível solicitar privilégios de administrador: {e}")
    sys.exit()

# ---------------------------
# Configuração do Tesseract
# ---------------------------
# Ajuste o caminho conforme sua instalação:
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\usuario\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# ---------------------------
# Loop principal
# ---------------------------
while True:
    caminho_arquivo = input("Digite o endereço do arquivo PDF (ou 'sair' para encerrar):\n")

    if caminho_arquivo.lower() == "sair":
        print("Encerrando o programa.")
        break

    if not os.path.isfile(caminho_arquivo):
        print("Erro: Arquivo não encontrado. Tente novamente.\n")
        continue

    try:
        texto_extraido = ""

        # Abre o PDF
        pdf = fitz.open(caminho_arquivo)

        for num_pagina, pagina in enumerate(pdf, start=1):
            # Extrai texto "digital" da página
            texto_normal = pagina.get_text()
            if texto_normal and texto_normal.strip():
                texto_extraido += f"\n[Texto página {num_pagina}]\n{texto_normal}"

            # Extrai imagens e faz OCR nelas
            imagens = pagina.get_images(full=True)
            if imagens:
                for img_index, img in enumerate(imagens, start=1):
                    xref = img[0]
                    base_image = pdf.extract_image(xref)
                    imagem_bytes = base_image["image"]

                    # Converte bytes para PIL.Image
                    imagem = Image.open(io.BytesIO(imagem_bytes))

                    # OCR (português). Adapte 'lang' se precisar de mais idiomas.
                    texto_ocr = pytesseract.image_to_string(imagem, lang="por")
                    if texto_ocr and texto_ocr.strip():
                        texto_extraido += f"\n[Texto OCR - Página {num_pagina}, Imagem {img_index}]\n{texto_ocr}"

        pdf.close()

        # Saída no console
        print("\nConteúdo extraído:\n")
        print(texto_extraido if texto_extraido.strip() else "(Nenhum texto encontrado)")
        print("-" * 40)

        # Pergunta onde salvar a cópia do PDF
        destino_pasta = input("Digite o caminho da pasta onde deseja salvar a cópia do PDF:\n")
        if not os.path.isdir(destino_pasta):
            print("A pasta não existe. Criando...")
            os.makedirs(destino_pasta, exist_ok=True)

        nome_original = os.path.basename(caminho_arquivo)
        novo_nome = "COPIA_" + nome_original
        caminho_copia = os.path.join(destino_pasta, novo_nome)

        shutil.copy2(caminho_arquivo, caminho_copia)
        print(f"Arquivo copiado para: {caminho_copia}\n")

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}\n")

# Evita fechamento imediato quando rodar por duplo clique
input("\nPressione Enter para sair...")

#Endereço Tesseract: C:\Users\usuario\AppData\Local\Programs\Tesseract-OCR
#c:\Users\usuario\Downloads\CNH-e.pdf.pdf
#CONSEERTAR ERRO DO ACESSO NEGADO WIN 5 e argumento