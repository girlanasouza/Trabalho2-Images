import cv2
import os

# Carrega o vídeo
video_path = 'input/v9.mp4'
video = cv2.VideoCapture(video_path)

# Cria o diretório de saída se não existir
output_dir = 'output/v9'
os.makedirs(output_dir, exist_ok=True)

# Parâmetros
frame_rate = int(video.get(cv2.CAP_PROP_FPS))  # Quadros por segundo do vídeo
frame_interval = frame_rate * 1  # Extrai um quadro a cada 2 segundos

# Contador de quadros
frame_count = 0

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    
    # Salva o quadro a cada 'frame_interval'
    if frame_count % frame_interval == 0:
        frame_path = os.path.join(output_dir, f'frame_{frame_count}.jpg')
        cv2.imwrite(frame_path, frame)
    
    
    frame_count += 1

# Libera os recursos
video.release()
cv2.destroyAllWindows()
