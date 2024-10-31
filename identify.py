import cv2

# Carrega o vídeo
video_path = 'input/v10.mp4'
video = cv2.VideoCapture(video_path)

# Parâmetros
frame_rate = int(video.get(cv2.CAP_PROP_FPS))  # Quadros por segundo do vídeo
frame_interval = frame_rate * 2  # Extrai um quadro a cada 2 segundos

# Contador de quadros
frame_count = 0

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    
    # Salva o quadro a cada 'frame_interval'
    if frame_count % frame_interval == 0:
        cv2.imwrite(f'frame_{frame_count}.jpg', frame)
    
    frame_count += 1

# Libera os recursos
video.release()
cv2.destroyAllWindows()
