import time

def doHeadMotion(motionProxy):
    print "in doHeadMotion start"

    ### Example showing how to set angles, using a fraction of max speed
    names  = ["HeadYaw", "HeadPitch"]
    angles  = [-0.4, -0.4]
    fractionMaxSpeed  = 0.2
    motionProxy.setAngles(names, angles, fractionMaxSpeed)

    time.sleep(3.0)
    motionProxy.setStiffnesses("Head", 0.0)
    print "in doHello end"

def doBehavior(behaviorProxy, motionProxy, postureProxy, inputEmotion, behaviorTime):
    behaviorProxy.stopAllBehaviors()
    motionProxy.stiffnessInterpolation('Body', 1.0, 1.0)
    rndVer = 1
    print 'Behavior Initialization'
    behaviorProxy.startBehavior('.lastUploadedChoregrapheBehavior/'+inputEmotion+'_0'+str(rndVer))
    time.sleep(behaviorTime)
    behaviorProxy.stopBehavior('.lastUploadedChoregrapheBehavior/'+inputEmotion+'_0'+str(rndVer))
    postureProxy.goToPosture('Stand',1.0)
    print "Behavior end"
