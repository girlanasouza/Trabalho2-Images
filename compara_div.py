import os

def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        tempos = [linha.strip() for linha in arquivo if linha.strip()]
    return tempos

def comparar_tempos(arquivo1, arquivo2):
    tempos1 = ler_arquivo(arquivo1)
    tempos2 = ler_arquivo(arquivo2)

    falsos_positivos = []
    falsos_negativos = []

    for tempo1 in tempos1:
        encontrado = False
        for tempo2 in tempos2:
            if abs(converter_tempo(tempo1) - converter_tempo(tempo2)) <= 1:
                encontrado = True
                break
        if not encontrado:
            falsos_positivos.append(tempo1)

    for tempo2 in tempos2:
        encontrado = False
        for tempo1 in tempos1:
            if abs(converter_tempo(tempo1) - converter_tempo(tempo2)) <= 1:
                encontrado = True
                break
        if not encontrado:
            falsos_negativos.append(tempo2)

    return falsos_positivos, falsos_negativos

def converter_tempo(tempo):
    partes = tempo.split(':')
    if len(partes) == 2:
        minutos, segundos = partes
        return int(minutos) * 60 + int(segundos)
    else:
        raise ValueError("Formato de tempo inválido: {}".format(tempo))

def compara_arquivos(arquivo1, arquivo2):
    falsos_positivos, falsos_negativos = comparar_tempos(arquivo1, arquivo2)

    total_tempos_arquivo1 = len(ler_arquivo(arquivo1))
    total_tempos_arquivo2 = len(ler_arquivo(arquivo2))

    acuracia = (total_tempos_arquivo1 - len(falsos_positivos)) / total_tempos_arquivo1

    with open("resultados.txt", "a") as arquivo_resultados:
        arquivo_resultados.write("\nComparando Video " + arquivo2.split("/")[-1] + " com limiar de " + arquivo2.split("/")[1].split("_")[1] + "\n")
        arquivo_resultados.write("Acurácia: {:.2%}\n".format(acuracia))
        arquivo_resultados.write("Quantidade Total " + str(total_tempos_arquivo1) + "\n")
        arquivo_resultados.write("Quantidade de Erros " + str(len(falsos_positivos)) + "\n")

    print("Resultados salvos no arquivo 'resultados.txt'.")











arquivos_algoritmo = []
arquivos_manuais = []

pasta_algoritmo = 'Divisões algoritmo'

def percorrer_diretorios(pasta, lista_arquivos):
    for raiz, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(raiz, arquivo)
            lista_arquivos.append(caminho_arquivo)

percorrer_diretorios(pasta_algoritmo, arquivos_algoritmo)

pasta_manuais = 'Divisões manuais'
arquivos = os.listdir(pasta_manuais)
for arquivo in arquivos:
    caminho_arquivo = os.path.join(pasta_manuais, arquivo)
    if os.path.isfile(caminho_arquivo):
        arquivos_manuais.append(caminho_arquivo)

for arquivo_manual in arquivos_manuais:
    for arquivo_algoritmo in arquivos_algoritmo:
        if(arquivo_algoritmo.split("/")[-1].split(".")[0] == arquivo_manual.split("/")[-1]):
            print("///")
            print(arquivo_manual)
            print(arquivo_algoritmo)
            print("///")
            compara_arquivos(arquivo_manual, arquivo_algoritmo)
