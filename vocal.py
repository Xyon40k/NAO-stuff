import naoqi
from naoqi import ALProxy, ALModule, ALBroker
import time
from os import system as cmd
from random import randint
#http://doc.aldebaran.com/2-8/naoqi-eventindex.html
ip = "192.168.211.74"
ttsproxy = ALProxy("ALTextToSpeech", ip, 9559)
dialog = ALProxy("ALDialog", ip, 9559)
motion = ALProxy("ALMotion", ip, 9559)
life = ALProxy("ALAutonomousLife", ip, 9559)
motion.wakeUp()
life.setState("solitary")

dialog.setLanguage("Italian")

def readfile(path):
    with open(path, "r") as f:
        return "".join(f.readlines())

content = readfile("comandi_vocali.vcm")

topic = dialog.loadTopicContent(content)

dialog.activateTopic(topic)
    
try:
    raw_input("Parla e di qualcosa...\nPremi il tasto invio quando hai finito...")
finally:
    dialog.unloadTopic(topic)


