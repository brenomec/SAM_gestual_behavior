# -*- coding: utf-8 -*-
"""
@author: Pierre Jacquot
@modify: Eric Rohmer
"""
#For more informations please check : http://www.coppeliarobotics.com/helpFiles/en/apiFunctions.htm
import sim,sys,time,math,os, subprocess
from naoqi import ALProxy
from manage_joints_pepper import get_first_handles,JointControl

from threading import Thread

from behavior_library import doHeadMotion,doBehavior

#opening NaoQI
#procNaoQI = subprocess.Popen(["../Choregraphe Suite 2.8/bin/naoqi-bin.exe", "-p", "9559", "../test_SAM/test_SAM.pml"])
#time.sleep(10.0)

def start():

    print ('================ Program Started ================')

    sim.simxFinish(-1)
    clientID=sim.simxStart('127.0.0.2',19999,True,True,5000,5)
    #if clientID!=-1:
    #	print 'Connected to remote API server'
    #
    #else:
    #	print 'Connection non successful'
    #	procNaoQI.kill()
    #	sys.exit('Could not connect')


    print ("================ Choregraphe's Initialization ================")
    
    global naoIP
    global naoPort

    naoIP = "127.0.0.1"
    naoPort = 9559

    global motionProxy
    global postureProxy
    global behaviorProxy

    motionProxy = ALProxy("ALMotion",naoIP, naoPort)
    postureProxy = ALProxy("ALRobotPosture", naoIP, naoPort)
    behaviorProxy = ALProxy("ALBehaviorManager", naoIP, naoPort)

    #Go to the posture StandInitZero
    posture = 'StandZero'
    print ('Posture Initialization : ') + posture
    motionProxy.stiffnessInterpolation('Body', 1.0, 1.0)
    
    postureProxy.goToPosture(posture,1.0)

    Head_Yaw=[];Head_Pitch=[];
    Hip_Roll=[];Hip_Pitch=[];Knee_Pitch=[];
    L_Shoulder_Pitch=[];L_Shoulder_Roll=[];L_Elbow_Yaw=[];L_Elbow_Roll=[];L_Wrist_Yaw=[]
    R_Shoulder_Pitch=[];R_Shoulder_Roll=[];R_Elbow_Yaw=[];R_Elbow_Roll=[];R_Wrist_Yaw=[]
    R_H=[];L_H=[];R_Hand=[];L_Hand=[];
    Body = [Head_Yaw,Head_Pitch,Hip_Roll,Hip_Pitch,Knee_Pitch,L_Shoulder_Pitch,L_Shoulder_Roll,L_Elbow_Yaw,L_Elbow_Roll,L_Wrist_Yaw,R_Shoulder_Pitch,R_Shoulder_Roll,R_Elbow_Yaw,R_Elbow_Roll,R_Wrist_Yaw,R_H,L_H,R_Hand,L_Hand]

    get_first_handles(clientID,Body)
    print ("================ Handles Initialization ================")
    commandAngles = motionProxy.getAngles('Body', False)
    print ('========== NAO is listening ==========')

    #JointControl(clientID,motionProxy,0,Body)
    #if(conversationStart):
    global motionThread 
    motionThread = Thread(target = JointControl, args = (clientID,motionProxy,0,Body))
    motionThread.start()

    for elemento in behaviorProxy.getInstalledBehaviors():
        print(elemento)

    conversationEnd = True

    
    


    print ('end')

def command(emotion, time):
    inputEmotion = emotion
    behaviorTime = float(time)
    doBehavior(behaviorProxy,motionProxy, postureProxy, inputEmotion, behaviorTime)

def stop():
    motionThread.join(timeout=10)  # Aguarda até 10 segundos pela finalização da thread
    if motionThread.is_alive():
        print("Thread ainda em execução, finalizando forçadamente.")
    else:
        print("Thread finalizada corretamente.")