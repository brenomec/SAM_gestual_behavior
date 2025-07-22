# -*- coding: utf-8 -*-

import pepper_interaction  # Importa o script onde as funções start, command e stop estão
import face_expression
from pynput import keyboard
import time

# Variável global para controle do loop
running = True

# Função para detectar quando a tecla "Esc" é pressionada
def on_press(key):
    global running
    if key == keyboard.Key.esc:
        print("Tecla Esc pressionada. Saindo do loop.")
        running = False  # Muda o estado da variável para parar o loop
        return False  # Interrompe o listener

# Função para iniciar o listener de teclado
def start_listener():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # Inicia o listener em uma thread separada
    return listener

# Loop principal
try:
    # Chama a função start() para inicializar o robô
    print("Iniciando pepper_interaction...")
    pepper_interaction.start()

    # Inicia o listener de teclado
    listener = start_listener()

    while running:
        # Solicita ao usuário os valores para emotion e time
        emotion = raw_input("Digite a emoção (ex: alegria, tristeza): ").strip()
        
        if not emotion:  # Verifica se a entrada de emoção está vazia
            print("A emoção não pode estar vazia. Tente novamente.")
            continue  # Reinicia o loop

        try:
            time_interval = float(raw_input("Digite o tempo de intervalo (em segundos): ").strip())
        except ValueError:
            print("Por favor, insira um valor numérico válido para o tempo.")
            continue  # Pula para a próxima iteração se o valor for inválido

        # Chama a função command() para executar o comportamento do robô
        print("Executing command on the robot with emotion '{}' and interval of {} seconds...".format(emotion, time_interval))
        face_expression.definir_emocao(emotion)
        pepper_interaction.command(emotion, time_interval)
        face_expression.definir_emocao('default')

        # Intervalo para evitar sobrecarga (ajuste conforme necessário)
        time.sleep(2)

finally:
    # Quando sair do loop, chama a função stop() para finalizar o robô corretamente
    print("Finalizando pepper_interaction...")
    pepper_interaction.stop()

    # Para o listener, se ainda estiver rodando
    listener.stop()

print("Programa encerrado.")
