import pytesseract
from PIL import Image
import re
import os
import shutil

def configurar_tesseract():
    """Detecta automaticamente onde o Tesseract está instalado"""
    # 1 - Tentar detectar no PATH
    caminho = shutil.which("tesseract")
    if caminho:
        pytesseract.pytesseract.tesseract_cmd = caminho
        print(f"✅ Tesseract encontrado no PATH: {caminho}")
        return

    # 2 - Procurar nos locais mais comuns do Windows
    caminhos_possiveis = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    ]

    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            pytesseract.pytesseract.tesseract_cmd = caminho
            print(f"✅ Tesseract encontrado: {caminho}")
            return

    # 3 - Se não encontrou, pedir manualmente
    print("⚠️ Não consegui localizar o Tesseract automaticamente.")
    caminho_manual = input("Digite o caminho completo do tesseract.exe: ").strip()
    if os.path.exists(caminho_manual):
        pytesseract.pytesseract.tesseract_cmd = caminho_manual
        print(f"✅ Tesseract configurado: {caminho_manual}")
    else:
        raise FileNotFoundError("❌ Tesseract não encontrado. Verifique a instalação.")

def processar_imagem():
    """Lê JPEG/JPG, extrai texto e renomeia conforme regras"""
    # Pergunta o arquivo da imagem
    caminho_img = input("Digite o caminho completo da imagem (JPG/JPEG): ").strip()
    
    # Pergunta a pasta de destino
    pasta_destino = input("Digite o caminho da pasta de destino: ").strip()

    # Abre a imagem e extrai texto
    imagem = Image.open(caminho_img)
    texto_extraido = pytesseract.image_to_string(imagem, lang="por")

    # Extrair K-número
    k_match = re.search(r'K-?(\d+)', texto_extraido, re.IGNORECASE)
    k_numero = k_match.group(1) if k_match else "SEM_K"

    # Extrair valor total
    valor_match = re.search(r'valor\s*total\s*[:\-]?\s*([\d\.,]+)', texto_extraido, re.IGNORECASE)
    valor_total = valor_match.group(1) if valor_match else "SEM_VALOR"

    # Extrair data de impressão
    data_match = re.search(r'(\d{2}/\d{2}/\d{4})', texto_extraido)
    if data_match:
        data = data_match.group(1).replace("/", "")
    else:
        data = "SEM_DATA"

    # Nome final
    extensao = os.path.splitext(caminho_img)[1]
    novo_nome = f"K{k_numero}-{valor_total}-{data}{extensao}"
    novo_caminho = os.path.join(pasta_destino, novo_nome)

    os.rename(caminho_img, novo_caminho)

    print(f"✅ Arquivo renomeado para: {novo_nome}")

if __name__ == "__main__":
    configurar_tesseract()
    processar_imagem()

#c:\Users\usuario\Downloads\teste extrator de texto savio.jpg

#c:\Users\usuario\Downloads\tesseract-ocr-w64-setup-5.5.0.20241111.exe
#c:\Users\usuario\Downloads

#RESOLVER ERROS DO TESSERACT