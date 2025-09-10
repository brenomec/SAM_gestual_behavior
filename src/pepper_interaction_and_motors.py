# -*- coding: utf-8 -*-

import sys
import time
import math
from threading import Thread
from naoqi import ALProxy
from dynamixel_sdk import *
from behavior_library import doBehavior

# ========== CONFIGURAÇÃO DOS MOTORES DYNAMIXEL ==========
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
PROTOCOL_VERSION = 1.0
DXL_IDS = list(range(1, 16))  # ID 0 é slave, então excluído
BAUDRATE = 57600
DEVICENAME = 'COM5'
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

# Mapeamento: ID do Dynamixel → Índice de commandAngles
dynamixel_joint_map = {
    1: 10,  # KneePitch
    2: 9,   # HipPitch
    3: 8,   # HipRoll (INVERTIDO)
    4: 0,   # HeadYaw
    5: 1,   # HeadPitch
    6: 2,   # LShoulderPitch
    7: 3,   # LShoulderRoll
    8: 4,   # LElbowYaw
    9: 5,   # LElbowRoll
    10: 6,  # LWristYaw
    11: 11, # RShoulderPitch (INVERTIDO)
    12: 12, # RShoulderRoll
    13: 13, # RElbowYaw
    14: 14, # RElbowRoll
    15: 15  # RWristYaw
}

# ========== VARIÁVEIS GLOBAIS ==========
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
running = True
dynamixelThread = None

# ========== FUNÇÕES DE CONTROLE ==========
def rad_to_steps(radians):
    return int(2048 + (radians * 2048 / math.pi))

def initialize_motors():
    print("Inicializando torque dos motores...")
    if not portHandler.openPort():
        raise RuntimeError("Falha ao abrir a porta")
    if not portHandler.setBaudRate(BAUDRATE):
        raise RuntimeError("Falha ao configurar a taxa de transmissão")
    for dxl_id in DXL_IDS:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
            portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            raise RuntimeError("Erro de comunicação ID {}: {}".format(dxl_id, packetHandler.getTxRxResult(dxl_comm_result)))
        if dxl_error != 0:
            raise RuntimeError("Erro do Dynamixel ID {}: {}".format(dxl_id, packetHandler.getRxPacketError(dxl_error)))

def send_motor_positions(radian_positions):
    groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_GOAL_POSITION, 4)
    for dxl_id, radians in zip(DXL_IDS, radian_positions):
        steps = rad_to_steps(radians)
        param_goal_position = [
            steps & 0xFF,
            (steps >> 8) & 0xFF,
            (steps >> 16) & 0xFF,
            (steps >> 24) & 0xFF,
        ]
        groupSyncWrite.addParam(dxl_id, param_goal_position)
    dxl_comm_result = groupSyncWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        raise RuntimeError("Erro de comunicação: {}".format(packetHandler.getTxRxResult(dxl_comm_result)))
    groupSyncWrite.clearParam()

def finalize_motors():
    print("Desabilitando torque dos motores...")
    for dxl_id in DXL_IDS:
        packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    portHandler.closePort()
    print("Porta fechada.")

def update_dynamixel_motors(motionProxy):
    global running
    while running:
        try:
            commandAngles = motionProxy.getAngles('Body', False)
            radian_positions = []
            for dxl_id in DXL_IDS:
                idx = dynamixel_joint_map.get(dxl_id)
                if idx is not None:
                    angle = commandAngles[idx]
                    # Corrigir sentido invertido do motor ID 11 e 3
                    if dxl_id in [3, 11]:  # HipRoll (3) e RShoulderPitch (11)
                        angle = -angle
                    radian_positions.append(angle)
            send_motor_positions(radian_positions)
            time.sleep(0.1)
        except Exception as e:
            print("Erro na thread de controle Dynamixel: {}".format(e))
            break

# ========== INTERFACE PÚBLICA ==========
def start():
    global motionProxy, postureProxy, behaviorProxy, dynamixelThread, running

    print('================ Program Started ================')
    naoIP = "127.0.0.1"
    naoPort = 9559
    motionProxy = ALProxy("ALMotion", naoIP, naoPort)
    postureProxy = ALProxy("ALRobotPosture", naoIP, naoPort)
    behaviorProxy = ALProxy("ALBehaviorManager", naoIP, naoPort)

    posture = 'StandZero'
    print('Posture Initialization: {}'.format(posture))
    motionProxy.stiffnessInterpolation('Body', 1.0, 1.0)
    postureProxy.goToPosture(posture, 1.0)

    try:
        initialize_motors()
        print("Motores Dynamixel inicializados.")
    except RuntimeError as e:
        print("Erro ao inicializar motores Dynamixel: {}".format(e))
        finalize_motors()
        return

    print("Iniciando controle contínuo dos motores Dynamixel.")
    running = True
    dynamixelThread = Thread(target=update_dynamixel_motors, args=(motionProxy,))
    dynamixelThread.start()

def command(emotion, time_interval):
    print("Executando comportamento: {} por {} segundos.".format(emotion, time_interval))
    doBehavior(behaviorProxy, motionProxy, postureProxy, emotion, time_interval)

def stop():
    global running, dynamixelThread
    running = False
    if dynamixelThread is not None and dynamixelThread.is_alive():
        dynamixelThread.join(timeout=10)
    finalize_motors()
    print("Sistema finalizado corretamente.")
