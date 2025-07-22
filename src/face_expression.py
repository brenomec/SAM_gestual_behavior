# -*- coding: utf-8 -*-
# Script para escolher uma emoção
import os

def definir_emocao(emocao_usuario):
    # Dicionário para mapear as emoções do usuário para as emoções válidas no sistema
    mapa_emocoes = {
        "Greeting": "happy",
        "Humor": "happy",
        "Confirmation": "happy",
        "Appreciation": "love",
        "Farewell": "sad",
        "Help": "sad",
        "Explanation": "think",
        "Opinion": "think",
        "Information": "think",
        "Error": "furious",
        "default": "default"
    }

    # Verifica se a emoção inserida pelo usuário está no dicionário
    if emocao_usuario not in mapa_emocoes:
        print("Emotion '{}' is not valid. Choose from: {}".format(emocao_usuario, list(mapa_emocoes.keys())))

        return

    # Mapeia a emoção do usuário para a emoção válida no sistema
    emocao_mapeada = mapa_emocoes[emocao_usuario]

    # Caminho para o arquivo de emoção
    caminho_arquivo = 'C:\\Users\\breno\\Documents\\_face animation\\emocao.txt'

    # Escreve a emoção mapeada no arquivo
    with open(caminho_arquivo, 'w') as arquivo:
        arquivo.write(emocao_mapeada)
    print("Emotion '{}' has been mapped to '{}' and set successfully.".format(emocao_usuario, emocao_mapeada))



# Exemplo de uso
# definir_emocao('happy')  # Altere para a emoção desejada
