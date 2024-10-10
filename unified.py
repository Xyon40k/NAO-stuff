import pygame
from pygame import *
from math import log, ceil, floor, radians
import naoqi
from os import system
from naoqi import ALProxy
from XarReader import XarReader


class Button(pygame.sprite.Sprite):
    def on_pressed(self):
        pass

    def __init__(self, size, topleft, on_pressed, color="#2596be"):
        self.image = pygame.surface.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        self.on_pressed = on_pressed
        self.name = on_pressed.__name__.replace("_", " ")
        self.color = color

    def is_pressed(self, pos):
        if self.rect.collidepoint(pos):
            print("Pressed '"+self.name+"'")
            self.on_pressed()

    def draw(self, surf, font):
        surf.blit(self.image, self.rect)
        text = font.render(self.name, True, "black")
        display.blit(text, text.get_rect(center=self.rect.center))

    def change_color(self, newcolor):
        self.color = newcolor
        self.image.fill(self.color)

    def __str__(self):
        return "<Button instance {}>".format(self.name)
    
    def __repr__(self):
        return "Button()"
    


class TextBox():
    def callback(self):
        pass

    def __init__(self, size, topleft, callback):
        self.rect = pygame.Rect(topleft, size)
        self.text = ""
        self.active = False
        self.callback = callback

    def on_click(self, pos, window):
        if self.rect.collidepoint(pos):
            self.active = True
            window.activebox = self
        else:
            self.active = False
            if window.activebox == self:
                window.activebox = None

    def write(self, event):
        if event.key == K_RETURN:
            self.callback(self.text)
            self.text = ""
        elif event.key == K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode

    def draw(self, surf, font):
        pygame.draw.rect(surf, BLACK, self.rect, 2)
        text = font.render(self.text, True, BLACK)
        surf.blit(text, (self.rect.x, self.rect.y))



class Window():
    def __init__(self, callbacks=[], types=[]):
        if(len(callbacks) != len(types)):
            raise Exception("Number of callbacks does not match number of types")
        self.bg = "white"
        self.margin = 40
        self.font = pygame.font.SysFont("arial", 50)
        self.buttons, self.textboxes = self.position_boxes(callbacks, types)
        self.activebox = None

    def position_boxes(self, callbacks, types):
        lentotal = len(callbacks)
        t = ceil(log(lentotal, 2))

        bxw = int(pow(2, floor((t+1)/2)))
        bxh = int(pow(2, floor(t/2)))

        wwm = WIDTH-self.margin*(bxw+1)
        hwm = HEIGHT-self.margin*(bxh+1)

        bw = wwm/bxw
        bh = hwm/bxh

        buttons = []
        textboxes = []
        for i in range(bxh):
            for j in range(bxw):
                index = i*bxw+j
                if index == lentotal:
                    return (buttons, textboxes)
                
                if(types[index] == 1):
                    textboxes.append(TextBox((bw, bh), (40+(j*(bw+40)), 40+(i*(bh+40))), callbacks[index]))
                elif(types[index] == 0):
                    buttons.append(Button((bw, bh), (40+(j*(bw+40)), 40+(i*(bh+40))), callbacks[index]))

        return (buttons, textboxes)

    def change_bg(self, color):
        self.bg = color

    def change_font(self, fontname, fontsize):
        self.font = pygame.font.SysFont(fontname, fontsize)

    def draw(self):
        display.fill(self.bg)
        for button in self.buttons:
            button.draw(display, self.font)
        
        for txtbox in self.textboxes:
            txtbox.draw(display, self.font)

    def check(self, pos):
        for button in self.buttons:
            button.is_pressed(pos)

        for txtbox in self.textboxes:
            txtbox.on_click(pos, self)

    def on_key(self, key):
        if self.activebox != None:
            self.activebox.write(key)



# ip = "192.168.74.74"
ip = "127.0.0.1"
# port = 9559
port = 56073

pygame.init()
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
display = pygame.display.set_mode((WIDTH, HEIGHT-50))
wt, ht = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.display.set_caption("Viva dio \\|T|/")
clock = pygame.time.Clock()

input_active = False
run = True
stiffnessStatus = True
topic = 0
animations = {}
audios = {}

tts = ALProxy("ALTextToSpeech", ip, port)
motion = ALProxy("ALMotion", ip, port)
posture = ALProxy("ALRobotPosture", ip, port)
audio = ALProxy("ALAudioPlayer", ip, port)
dialog = ALProxy("ALDialog", ip, port)
life = ALProxy("ALAutonomousLife", ip, port)

life.setState("solitary")

dialog.setLanguage("Italian")
# system("cls")
topics = dialog.getLoadedTopics("Italian")
if len(topics) != 0:
    dialog.unloadTopic(topics[0])

print("Connected...")


def Animazione(nome, fps=25):
    """
    Il nome dell'animazione va in inglese.
    Tai Chi Chuan va a 5 fps
    """
    audioid = -1
    if(not nome in animations.keys()):
        try:
            animations[nome] = XarReader(".\\media\\animations\\"+nome+".xar", 1.0/fps).get_data()
            try:
                if nome in audios.keys():
                    audioid = audios[nome]
                else:
                    s = eval('"/home/nao/music/'+nome+'.mp3"') # Disgustoso ma funziona solo cosi
                    audioid = audio.loadFile(s) # FIXME: 
                    audios[nome] = audioid
            except Exception as e:
                print(e)
                print("Nessun audio disponibile")
        except:
            print("Animazione non disponibile")
            return
        
    Alzati()
    joints, times, angles = animations[nome]
    if(audioid != -1):
        audio.post.play(audioid)
    motion.angleInterpolationBezier(joints, times, angles)
    Alzati()

def Attiva_comandi_vocali():
    with open("comandi_vocali.vcm", "r") as f:
        content = "".join(f.readlines())

    topic = dialog.loadTopicContent(content)
    dialog.activateTopic(topic)

def Disattiva_comandi_vocali():
    try:
        dialog.unloadTopic(topic)
    except:
        pass

def Accovacciati():
    posture.goToPosture("Crouch", 0.5)

def Siediti():
    posture.goToPosture("Sit", 0.5)

def Alzati():
    posture.goToPosture("Stand", 0.5)

def Raddrizza_la_testa():
    motion.angleInterpolationWithSpeed(["HeadYaw", "HeadPitch"], [0.0, 0.0], 1.0)

def Attiva_muscoli():
    motion.stiffnessInterpolation("Body", 1.0, 0.01)

def Disattiva_muscoli():
    motion.stiffnessInterpolation("Body", 0.0, 0.01)

def Dormi():
    motion.rest()

def Sveglia():
    motion.wakeUp()

def Chiudi_mani():
    motion.post.closeHand("LHand")
    motion.closeHand("RHand")

def Apri_mani():
    motion.post.openHand("LHand")
    motion.openHand("RHand")

def Traccia_Viso():
    face.enableTracking(True)

def Parla(Frase):
    tts.say(str(Frase))

def Stop_Traccia_Viso():
    face.enableTracking(False)

def Lista_posizioni():
    print(posture.getPostureList())

def Mossa_dell_elefante():
    Animazione("elephant")

def Gorilla():
    Animazione("gorilla")

def Balla():
    Animazione("disco")

def Tai_Chi():
    Animazione("taichi", 5)

def Animazione_better(nome):
    if nome == "taichi":
        fps = 5
    else:
        fps = 25
    Animazione(nome, fps)

def Muovi(metri):
    motion.moveTo(float(metri), 0, 0)

def Disconnetti():
    pygame.event.post(pygame.event.Event(QUIT))
    print("Disconnessione...")

callbacks = [Accovacciati, Siediti, Alzati, Raddrizza_la_testa, Attiva_muscoli, Disattiva_muscoli, Dormi, Sveglia, Chiudi_mani, Apri_mani, Attiva_comandi_vocali, Disattiva_comandi_vocali, Parla, Animazione_better, Disconnetti]
# type: 0 = button, 1 = textbox
types = [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0]
window = Window(callbacks, types) 

while run:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            window.check(pygame.mouse.get_pos())
        elif event.type == pygame.QUIT:
            if topic != 0:
                dialog.unloadTopic(topic)
            run = False
            break
        elif event.type == KEYDOWN:
            window.on_key(event)

    clock.tick(30)
    window.draw()
    pygame.display.flip()