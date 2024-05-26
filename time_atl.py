import cv2
import pygame
import time
import os

# Inicializar Pygame
pygame.init()

# Configurações da janela Pygame
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Gravação de Vídeo com Cronômetro")

# Inicializar mixer para som de tiro de largada
pygame.mixer.init()
start_sound_path = 'start_sound.mp3'  # Certifique-se de que este arquivo está no mesmo diretório

# Configurações de captura de vídeo
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None

# Variáveis de controle
recording = False
start_time = None
end_time = None

def overlay_timer_on_video(output_path, duration):
    cap = cv2.VideoCapture('output.avi')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Definir codec e criador de vídeo
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    # Ajuste do tempo final do vídeo para corresponder à duração real da gravação
    end_frame = int(duration * fps)
    
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Ler e escrever frames
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_count >= end_frame:
            break
        
        # Calcular o tempo de exibição do cronômetro
        elapsed_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        # Desenhar cronômetro no canto inferior direito
        cv2.putText(frame, f"Tempo: {elapsed_time:.2f}s", (width - 200, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        out.write(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1

    # Liberar recursos
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not recording:
                # Iniciar gravação
                recording = True
                start_time = time.time()
                out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
                pygame.mixer.music.load(start_sound_path)
                pygame.mixer.music.play()
                print("Gravação iniciada")
            else:
                # Parar gravação
                recording = False
                end_time = time.time()
                duration = end_time - start_time
                out.release()
                cap.release()
                print("Gravação parada")
                overlay_timer_on_video('output_with_timer.avi', duration)
                cap = cv2.VideoCapture(0)  # Reabrir a captura de vídeo
                print("Vídeo salvo com cronômetro")

    if recording:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('frame', frame)
            # Desenhar cronômetro na janela Pygame
            elapsed_time = time.time() - start_time
            screen.fill((0, 0, 0))  # Limpar a tela antes de desenhar o texto
            font = pygame.font.Font(None, 36)
            text = font.render(f"Tempo: {elapsed_time:.2f}s", True, (255, 255, 255))
            screen.blit(text, (10, 10))

    pygame.display.flip()

cap.release()
cv2.destroyAllWindows()
pygame.quit()
