# INSTRUÇÕES PARA RODAR O PROGRAMA:

# Para rodar o programa, algumas coisas precisão ser conferidas:

# 1-
Certifique-se de que o Python 3 está instalado na sua máquina.

# 2-
Crie uma pasta e um arquivo .py para começar as instalações através do próprio terminal.

# 3-
Instale a biblioteca do OpenCV e o Matplotlib utilizando os comandos abaixo:

No terminal da sua IDE:
bash
Copiar código
pip install opencv-python  
pip install matplotlib 

# 4-
Agora basta copiar e colar o arquivo na pasta criada anteriormente.

# 5-
Agora só basta rodar o programa. O mesmo irá abrir uma pequena janela onde será capturada a imagem da câmera do seu dispositivo ou algum arquivo que você deseja testar o código. Quando desejar parar de detectar, a tecla responsável por esse procedimento é a tecla "q", que finaliza a execução do programa.

# 6-
Logo após a execução do programa, ele irá gerar um gráfico com a quantidade de rastreios detectados ao longo do tempo, utilizando o 1 para quando detectar e o 0 para quando não for detectado.

# 7-
Conclusão:
Certifique-se de ter uma câmera conectada ao computador ou forneça um caminho válido para um arquivo de vídeo na função cv2.VideoCapture() caso prefira usar um vídeo salvo.