import cv2
import numpy as np,numpy
import os
import sys



if len(sys.argv) == 3:
    nome = sys.argv[1]
    limiar = sys.argv[2]
else:
    print("Error, passe o nome do video como primeiro parâmetro")
    print("Error passe limiar como segundo parâmetro")



def histograma(img):
    hist = numpy.zeros(64)
    for i in range(len(img)):
        for j in range(len(img[0])):
            hist[img[i][j]] += 1
    return hist

def histogramaAcumulado(hist):
    histBase = hist
    histResultado = numpy.zeros(768)
    histResultado[0] = histBase[0]
    for i in range(1,768):
        histResultado[i] = histResultado[i-1] + histBase[i]
    return histResultado


def particionaImagem5x5(img):
    divI = int(len(img)/5)
    divJ = int(len(img[0])/5)
    inicioJ = 0
    fimJ = divJ
    particoes = []
    for i in range(5):
        for j in range(5):
            inicioI = j*divI
            fimI = (j + 1)*divI
            particoes.append(img[inicioI:fimI, inicioJ:fimJ])
        inicioJ += divJ
        fimJ += divJ
    return particoes

def histograma5x5(img):
    histogramas = [ histograma(particionaImagem5x5(img)[x]) for x in range (25) ]
    return histogramas

def comparaHistogramas5x5(img,img2):
    hists1 = histograma5x5(img)
    hists2 = histograma5x5(img2)
    total = []
    for i in range(25):
        total.append(comparaHistogramas(hists1[i],hists2[i]))
    total.sort()
    total5meio = total[10:14]
    total = np.sum(total5meio)
    return total/5     #pegar 9 valores do meio do rol e fazer a média
        
def comparaHistogramasBIC5x5(img,img2):
    parts1 = particionaImagem5x5(img)
    parts2 = particionaImagem5x5(img2)
    total = []
    for i in range(25):
        total.append(comparaHistogramasBIC(parts1[i],parts2[i]))
    total.sort()
    total5meio = total[10:14]
    total = np.sum(total5meio)
    return total/5


def comparaHistogramasBIC(img1,img2):
    histB1, histI1 = bic(img1,True)
    histB2, histI2 = bic(img2,True)
    totalInterior = comparaHistogramas(histI1,histI2)
    totalBordas = comparaHistogramas(histB1, histB2)
    return (totalInterior + totalBordas)/2


def somatorio(lista):
    total = 0
    for elemento in lista:
        total += elemento
    return total

'''
def comparaHistogramas(hist1, hist2):
    # Verifica se os histogramas têm o mesmo número de bins
    if len(hist1) != len(hist2):
        raise ValueError("Os histogramas têm tamanhos diferentes.")
    
    # Converte as listas em arrays numpy
    hist1 = np.array(hist1)
    hist2 = np.array(hist2)

    # Normaliza os histogramas
    somatorio1 = np.sum(hist1)
    if(somatorio1==0): somatorio1+=1 
    somatorio2 = np.sum(hist2)
    if(somatorio2==0): somatorio2+=1
    hist1 = hist1 / somatorio1
    hist2 = hist2 / somatorio2

    # Calcula a distância de Bhattacharyya
    distance = np.sqrt(np.sum(hist1 * hist2))

    return 1 - distance

'''
def comparaHistogramas(hist1,hist2):
    total = 0 #fazer em relacao ao tamanho total 
    for i in range(len(hist1)):
        if(hist1[i] + hist2[i] == 0):
            total += 1
        else:
            total += 1 - (abs(hist1[i] -hist2[i])/(hist1[i] + hist2[i]))
    return total/len(hist1) 


def quantizacao(img): #faz a quantização da imagem para 64 cores
    img2 = numpy.zeros((len(img),len(img[0])),int)
    for i in range(len(img)):
        for j in range(len(img[0])):
            for x in range(3):
                img2[i][j] += (4**x) * (round(int(img[i][j][x]) * 3/float(255)))
                #print(img2[i][j][x])
            #print(img2[i][j])
    return img2

def bic(img,jaTaQuantizada):
    if(jaTaQuantizada):
        quantizada = img
    else:
        quantizada = quantizacao(img)
    histogramaBorda = [0 for i in range(64)]
    histogramaInterior = [0 for i in range(64)]

    for i in range(1,len(quantizada)-1): 
        for j in range(1,len(quantizada[0])-1):
                v1 = int(quantizada[i][j])
                v3 = int(quantizada[i-1][j])
                v5 = int(quantizada[i][j-1])
                v6 = int(quantizada[i][j+1])
                v8 = int(quantizada[i+1][j])
                if( v1 != v3 or v1 != v5 or v1 != v6 or v1 != v8):
                    histogramaBorda[quantizada[i][j]] += 1
                else:
                    histogramaInterior[quantizada[i][j]] += 1

    return histogramaBorda, histogramaInterior

# Abrir o vídeo
nomeVideo = "input/v10.mp4"
video = cv2.VideoCapture(nomeVideo)
contadorFrames=0
achou = True
frames = 0
cortes = []
quadrosChave = []

frame_cont = 0

while True:
    # Ler o próximo frame do vídeo
    ret, frame = video.read()

    print("frame atual")
    print(frame_cont)
    frame_cont += 1
    # Se não houver mais frames, sair do loop
    if not ret:
        break

    
    #cv2.imshow('video',frame)

    if contadorFrames == 2:
        frame1 = frame.copy()
        #contadorFrames = 0
        #achou = False
    elif contadorFrames == 8:
        quadroChave = frame.copy()
    elif contadorFrames==17 :
        contadorFrames = 1
        
        #print('comparando frames')
        frame2 = frame.copy()
        qf1 = quantizacao(frame1)
        qf2 = quantizacao(frame2)
        #cv2.imshow('frame1',frame1)
        #cv2.imshow('frame2',frame2)
        hist1 = histograma(qf1)
        hist2 = histograma(qf2)
        comparacaoHistogramas = comparaHistogramas(hist1,hist2)
        comparacaoHistogramasLocais = comparaHistogramas5x5(qf1,qf2)
        comparacaoBIC = comparaHistogramasBIC(qf1,qf2)
        comparacaoBICLocais = comparaHistogramasBIC5x5(qf1,qf2) 
        semelhança = min(comparacaoHistogramas,comparacaoHistogramasLocais,comparacaoBIC,comparacaoBICLocais)
        #qprint(comparacaoHistogramas,comparacaoHistogramasLocais,comparacaoBIC,comparacaoBICLocais)
        if(semelhança < float(limiar)):
            print("corte: " + str(frames) + "frames")
            cortes.append(frames)
            quadrosChave.append(quadroChave)
            #achou = True
            
    
    contadorFrames+=1
    frames += 1
    

    # Aguardar a tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar os recursos
video.release()
cv2.destroyAllWindows()


nomeDiretorio="quadrosChave-{}".format(nomeVideo)
if(not os.path.exists(nomeDiretorio)):
    os.makedirs(nomeDiretorio)

c = 0

arquivo = open(f'{nomeDiretorio}/resultadosclipe.txt','w')
for corte in cortes:
    segundos = int(corte/30)
    minutos = int(segundos/60)
    segundos = segundos % 60
    arquivo.write(f"{minutos}:{segundos:02}\n")
arquivo.close()


for quadro in quadrosChave:
    cv2.imwrite(f'{nomeDiretorio}/quadroChave{c}.jpg',quadro)
    c+=1

