# -*- coding: utf-8 -*-

import pepper_interaction_and_motors  # Importa o script onde as funções start, command e stop estão
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
listener = None
try:
    # Chama a função start() para inicializar o robô
    print("Iniciando pepper_interaction_and_motors...")
    pepper_interaction_and_motors.start()

    # Inicia o listener de teclado
    listener = start_listener()

    while running:
        # Solicita ao usuário os valores para emotion e time
        emotion = raw_input("Digite a emoção (ex: alegria, tristeza): ").strip()
        if not running:
            break  # Sai do loop se "Esc" foi pressionada
        if not emotion:  # Verifica se a entrada de emoção está vazia
            print("A emoção não pode estar vazia. Tente novamente.")
            continue  # Reinicia o loop

        try:
            time_interval = float(raw_input("Digite o tempo de intervalo (em segundos): ").strip())
        except ValueError:
            print("Por favor, insira um valor numérico válido para o tempo.")
            continue  # Pula para a próxima iteração se o valor for inválido

        # Chama a função command() para executar o comportamento do robô
        print("Executando comando com emoção '{}' por {} segundos...".format(emotion, time_interval))
        pepper_interaction_and_motors.command(emotion, time_interval)

        # Intervalo entre execuções
        time.sleep(2)

finally:
    # Quando sair do loop, chama a função stop() para finalizar corretamente
    print("Finalizando pepper_interaction_and_motors...")
    pepper_interaction_and_motors.stop()

    # Para o listener, se ainda estiver rodando
    if listener is not None:
        listener.join()

print("Programa encerrado.")
