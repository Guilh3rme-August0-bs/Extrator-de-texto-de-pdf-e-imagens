import PyPDF2
import shutil
import os

while True:
    # Solicita o caminho do arquivo PDF original
    caminho_arquivo = input("Digite o endereço do arquivo PDF (ou digite 'sair' para encerrar):\n")

    if caminho_arquivo.lower() == "sair":
        print("Encerrando o programa.")
        break

    # Verifica se o arquivo existe
    if not os.path.isfile(caminho_arquivo):
        print("Erro: Arquivo não encontrado. Verifique o caminho e tente novamente.\n")
        continue

    try:
        # Tenta abrir e extrair o texto do PDF
        with open(caminho_arquivo, "rb") as arquivo:
            leitor_pdf = PyPDF2.PdfReader(arquivo)
            texto = ""
            for pagina in leitor_pdf.pages:
                texto += pagina.extract_text()

        print("\nConteúdo do arquivo PDF:\n")
        print(texto)
        print("-" * 40 + "\n")

        # Solicita o diretório onde a cópia deve ser salva
        destino_pasta = input("Digite o caminho da pasta onde deseja salvar a cópia do PDF:\n")

        # Verifica se a pasta existe
        if not os.path.isdir(destino_pasta):
            print("Erro: A pasta de destino não existe. Verifique o caminho e tente novamente.\n")
            continue

        # Define novo nome para a cópia
        nome_arquivo_original = os.path.basename(caminho_arquivo)
        novo_nome = "COPIA_" + nome_arquivo_original
        caminho_novo_arquivo = os.path.join(destino_pasta, novo_nome)

        # Copia o PDF
        shutil.copy2(caminho_arquivo, caminho_novo_arquivo)
        print(f"Arquivo copiado com sucesso para:\n{caminho_novo_arquivo}\n")

    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}\n")

        #PRÓXIMO PASSO: IMPLEMENTAR FUNCIONALIDADE DE EXTRAIR TEXTO DAS IMAGENS CONTIDAS NO PDF