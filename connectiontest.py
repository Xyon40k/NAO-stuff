import naoqi
from naoqi import ALProxy

ip = "127.0.0.1"
# ip = "192.168.74.74"
port = 56073
# port = 9559

tts = ALProxy("ALTextToSpeech", ip, port)

tts.say("Hello, world!")

