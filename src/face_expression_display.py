# -*- coding: utf-8 -*-
from __future__ import print_function  # permite usar print() no Python 2
import requests
import sys

def definir_emocao(emocao_usuario):
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
        "Error": "furious"
    }

    if emocao_usuario not in mapa_emocoes:
        print("Emotion '{}' is not valid. Choose from: {}".format(emocao_usuario, mapa_emocoes.keys()))
        return

    emocao_mapeada = mapa_emocoes[emocao_usuario]
    gif_path = "animations/{}.gif".format(emocao_mapeada)

    url = "http://10.1.2.172:5000/start_animation"
    payload = {
        "animation": gif_path
    }

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print("✅ Emotion '{}' mapped to '{}', animation sent successfully.".format(emocao_usuario, emocao_mapeada))
        else:
            print("❌ Server returned error: {} - {}".format(response.status_code, response.text))

    except requests.exceptions.RequestException as e:
        print("❌ Failed to send request: {}".format(e))


# Entrada pela linha de comando
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python face_expression_display.py <Emotion>")
    else:
        definir_emocao(sys.argv[1])
