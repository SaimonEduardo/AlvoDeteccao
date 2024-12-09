import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

# Carrega o vídeo ou arquivo de sua escolha
cap = cv2.VideoCapture(0)

# Defina as coordenadas (x, y) e o tamanho (largura, altura) da área de detecção
x_start, y_start, width, height = 100, 100, 400, 300  # Exemplo de área de detecção

# Variáveis para análise de tempo
timestamps = []
frames_with_x = []

start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Limita a área de detecção ao retângulo definido
    roi = frame[y_start:y_start+height, x_start:x_start+width]

    # Converte o quadro para escala de cinza e aplica desfoque
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    # Detecta círculos na área limitada
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=50,
        param1=50,
        param2=50,
        minRadius=10,
        maxRadius=80
    )

    x_identified = False

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        for (x, y, r) in circles:
            # Ajusta as coordenadas do círculo para o quadro original
            x_global = x + x_start
            y_global = y + y_start

            # Máscara para focar no círculo
            mask = np.zeros_like(gray)
            cv2.circle(mask, (x, y), r, 255, -1)
            cropped = cv2.bitwise_and(gray, gray, mask=mask)

            # Detecta bordas e linhas dentro do círculo
            edges = cv2.Canny(cropped, 50, 150, apertureSize=3)
            lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

            if lines is not None:
                # Armazena os ângulos das linhas detectadas

                angles = []
                for rho, theta in lines[:, 0]:
                    angles.append(theta)

                # Ordena os ângulos para calcular a diferença
                angles.sort()

                # Verifica se há duas linhas com ângulos próximos de 90° (π/2 radianos)
                if len(angles) >= 2:
                    for i in range(len(angles) - 1):
                        angle_diff = abs(angles[i + 1] - angles[i])

                        # Se a diferença entre os ângulos for próxima de 90° (π/2)
                        if np.isclose(angle_diff, np.pi / 2, atol=np.pi / 18):
                            x_identified = True  # Confirma que o "X" foi encontrado

                            # Desenha as linhas detectadas no quadro original
                            for rho, theta in lines[:, 0]:
                                a, b = np.cos(theta), np.sin(theta)
                                x0, y0 = a * rho, b * rho
                                x1 = int(x_global + r * (-b))
                                y1 = int(y_global + r * (a))
                                x2 = int(x_global - r * (-b))
                                y2 = int(y_global - r * (a))
                                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Linha vermelha

                            # Desenha o círculo identificado
                            cv2.circle(frame, (x_global, y_global), r, (0, 255, 0), 4)  # Círculo verde
                            cv2.circle(frame, (x_global, y_global), 2, (0, 0, 255), 3)  # Centro do círculo

    # Atualiza os dados de tempo
    elapsed_time = time.time() - start_time
    timestamps.append(elapsed_time)
    frames_with_x.append(1 if x_identified else 0)

    # Exibe o quadro com os desenhos identificados
    cv2.imshow("Detected Patterns in Video", frame)

    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera o vídeo e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()

# Gera o gráfico com matplotlib
plt.figure(figsize=(10, 5))
plt.plot(timestamps, frames_with_x, label="Círculos com X Identificados", color="green")
plt.xlabel("Tempo (s)")
plt.ylabel("Detecção (1 = Sim, 0 = Não)")
plt.title("Detecção de Círculos com X ao longo do tempo")
plt.legend()
plt.grid(True)
plt.show()
