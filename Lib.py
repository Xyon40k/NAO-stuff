"""
Librerie utilizzate per la Libreria NaoLib.
"""
from naoqi import ALProxy
import os
import math
from math import radians
import time
from XarReader import XarReader

class NaoLib:
    """
    Questo e' il costruttore della classe NaoLib.
    Argomenti:
    - IPAddress: Indirizzo IP del Nao (si ottiene cliccando il pulsante nel petto del Nao)
    - Port: Porta del Nao. e' solitamente impostata di default a: 9559
    - ClearLog: Bool. e' dichiarato True se si vuole cancellare la console dopo che si e' inizializzata la libreria.
    - IsRealRobot: Bool. Utilizzato per capire se si sta utilizzando un Nao reale, oppure tramite simulazione con Choregraphe.
    """
    def __init__(self, IPAddress, Port, ClearLog, IsRealRobot):
        """
        Questa e' la lista completa di tutti gli arti del Nao che si possono muovere, e i rispettivi valori minimi e massimi.
        Potete trovare la lista completa di tutti gli arti del corpo del Nao qui:
        http://doc.aldebaran.com/2-1/family/robots/joints_robot.html
        """
        self.angoli = {
            "HeadPitch": {"Avanti": radians(-38.5), "Dietro": radians(29.5)},
            "HeadYaw": {"Destra": radians(-119.5), "Sinistra": radians(119.5)},
            "ShoulderRoll": {"Fuori": radians(-76), "Dentro": radians(18)},
            "ElbowRoll": {"Fuori": radians(2), "Dentro": radians(88.5)},
            "ElbowYaw": {"Sinistra": radians(-119.5), "Destra": radians(119.5)},
            "WristYaw": {"Sinistra": radians(-104.5), "Destra": radians(104.5)},
            "ShoulderPitch": {"Avanti": radians(-119.5), "Dietro": radians(119.5)},
            "HipYawPitch": {"Avanti": radians(42.4), "Dietro": radians(-65.6)},
            "HipPitch": {"Avanti": radians(-88), "Dietro": radians(27.7)},
            "KneePitch": {"Avanti": radians(-5.2), "Dietro": radians(121)},
            "AnklePitch": {"Avanti": radians(-68.1), "Dietro": radians(52.8)},
            "HipRoll": {"Fuori": radians(45.2), "Dentro": radians(-21.7)},
            "AnkleRoll": {"Fuori": radians(44), "Dentro": radians(-22.7)}
        }
        """
        Dichiaro l'indirizzo IP e la Porta del Nao
        """
        self.NaoIP = IPAddress
        self.NaoPort = Port
        # Tutti i Proxy necessari per i vari metodo della libreria.
        self.tts = ALProxy("ALTextToSpeech", self.NaoIP, self.NaoPort)
        self.motion = ALProxy("ALMotion", self.NaoIP, self.NaoPort)
        self.posture = ALProxy("ALRobotPosture", self.NaoIP, self.NaoPort)
        self.dialog = ALProxy("ALDialog", self.NaoIP, self.NaoPort)
        self.memory = ALProxy("ALMemory", self.NaoIP, self.NaoPort)
        """
        Qui come si puo' vedere, creiamo i seguenti Proxy solamente se e' un Nao reale 
        (Moduli come ALPhotoCapture, etc. etc., non sono supportati su simulazioni).
        """
        if(IsRealRobot == True):
            self.face = ALProxy("ALFaceDetection", self.NaoIP, self.NaoPort)
            self.record = ALProxy("ALVideoRecorder", self.NaoIP, self.NaoPort)     
            self.video = ALProxy("ALVideoDevice", self.NaoIP, self.NaoPort)  
            self.photo = ALProxy("ALPhotoCapture",self.NaoIP,self.NaoPort)

        self.got_face = False
        if(ClearLog == True):
            os.system("cls")
        
        self.animations = {}

    """
    Questo metodo viene utilizzato per "resettare" la posizione del Nao.
    - La postura del Nao e' in piedi.
    - Chiude entrambe le mani.
    - Il Nao diventa rigido.
    """
    def reset(self):
        self.SetPostura("Stand",2.0)
        self.ChiudiMani()
        self.motion.stiffnessInterpolation("Body", 1.0, 0.01)
        
    """
    Il Nao parla utilizzando il Proxy "ALTextToSpeech".
    Argomento:
    - Frase. Deve essere una stringa ed e' cio' che il Nao pronunciera'.
    """
    def Parla(self, Frase):
        self.tts.say(Frase)  


    """
    Il Nao si muove utilizzando il Proxy "ALMotion".
    Argomenti:
    - CoordinataX: Deve essere una grandezza espressa in metri.
    - CoordinataY: Deve essere una grandezza espressa in metri.
    - RotazioneGradi: Indica di quanti gradi il Nao dovra' girare. Il metodo converte il valore automaticamente in radianti.
    """
    def Muovi(self, CoordinataX, CoordinataY, RotazioneGradi):
        return self.motion.moveTo(CoordinataX, CoordinataY, math.radians(RotazioneGradi))


    """
    Questo metodo modifica la resistenza che ha ogni parte del corpo del Nao.
    Argomenti:
    - PartiCorpo: e' una stringa.
    - Resistenza: e' un valore che varia da 0 a 1, in base a quanta resistenza si vuole avere.
    - TempoEsecuzione: varia da 0 a 1, in base all'arco di tempo in cui eseguira' l'azione
    """
    def setResistenza(self, PartiCorpo, Resistenza, TempoEsecuzione):
        self.motion.stiffnessInterpolation(PartiCorpo, Resistenza, TempoEsecuzione)  

    """
    Il metodo scrive sulla console il sommario dei valori di resistenza di tutto il corpo del Nao.
    """
    def SommarioResistenza(self):
        print(self.motion.getSummary())


    """
    Questo metodo fara' piegare un arto del Nao utilizzando il Proxy "ALMotion".
    Argomenti:
    - PartiCorpo: e' una stringa, rappresenta la parte del corpo che si vuole muovere.
    - GradiRotazione: valore della rotazione dell'arto. e' diverso per ogni arto.
    - Tempo: tempo di esecuzione dell'azione. Varia da 0 a 1.
    Esempio di codice:
    nao = NaoLib(0, 0, True, True)
    nao.PiegaArti("LShoulderPitch", nao.angoli["ShoulderPitch"]["Avanti"], 2.0, True)
    Come possiamo vedere, il valore della rotazione e' contenuto nella lista con tutti gli arti del corpo (linea 22).

    Potete trovare la lista completa di tutti gli arti del corpo del Nao qui:
    http://doc.aldebaran.com/2-1/family/robots/joints_robot.html
    """
    def PiegaArti(self, PartiCorpo, GradiRotazione, Tempo):
        self.motion.angleInterpolation(PartiCorpo, GradiRotazione, Tempo, True)

    """
    Apre una delle due mani del Nao.
    Argomenti:
    - Mano: e' una stringa. Puo' essere "LHand" oppure "RHand".
    """
    def ApriMano(self, Mano):            
        self.motion.openHand(Mano)
        self.motion.waitUntilMoveIsFinished() # Aspetta che il movimento sia terminato

    """
    Chiude una delle due mani del Nao.
    - Mano: e' una stringa. Puo' essere "LHand" oppure "RHand".
    """
    def ChiudiMano(self, Mano):
        self.motion.closeHand(Mano)
        self.motion.waitUntilMoveIsFinished() # Aspetta che il movimento sia terminato

    """
    Apre entrambe le mani del Nao.
    """
    def ApriMani(self):
        self.motion.openHand("LHand") #Mano sinistra
        self.motion.openHand("RHand") #Mano destra

    """
    Chiude entrambe le mani del Nao.
    """
    def ChiudiMani(self):
        self.motion.closeHand("LHand")
        self.motion.closeHand("RHand")


    """
    Questo metodo e' utilizzato per il riconoscimento vocale del Nao.
    Argomenti:
    DomandeRisposte: e' una stringa. Contiene le varie frasi che l'utente pronunciera', e le risposte del Nao.
    Lingua: e' una stringa e rappresenta la lingua con la quale il Nao rispondera'.

    Ecco un esempio di come deve essere la stringa di input:

    InputDomandeRisposte = ('topic: ~example_topic_content()\n'
                       'language: Italian\n'
                       'u: (ti voglio bene) Anche io!\n'
                       'u: (dove vivi) Vivo nel laboratorio dell\'Istituto Carlo Zuccante!\n')

    Potete trovare maggiori informazioni qui:
    http://doc.aldebaran.com/2-5/naoqi/interaction/dialog/aldialog.html
    """
    def RiconoscimentoVocale(self, DomandeRisposte, Lingua):
        self.dialog.setLanguage(Lingua)
        topic = self.dialog.loadTopicContent(DomandeRisposte)
        self.dialog.activateTopic(topic)
        input() #Input per capire quando bisogna terminare la conversazione.
        # Molto importante chiamare il metodo "unloadTopic". 
        # Se non si esegue e si termina il processo, il Nao potrebbe sollevare delle eccezioni per quanto riguarda il riconoscimento vocale.
        self.dialog.unloadTopic(topic)


    """
    Stabilisce la posizione del Nao.
    Argomenti:
    - NomePostura: e' una stringa e rappresenta la postura che deve avere.
    """
    def SetPostura(self, NomePostura, Tempo):
        self.posture.goToPosture(NomePostura, Tempo)

    """
    Traccia il viso della persona che ha davanti.
    Argomenti:
    - BooleanTracciaViso: e' un Bool. Il valore sara' "True" se il Nao dovra' tracciare il viso delle persone, "False" se dovra' smettere di tracciarlo.
    """
    def TracciaViso(self, BooleanTracciaViso):  
        self.face.enableTracking(BooleanTracciaViso)   

    """
    Questo metodo aspetta che il Nao abbia finito di muoversi / eseguire movimenti.
    """
    def AspettaFineMossa(self):
        self.motion.waitUntilMoveIsFinished()
        return

    """
    Questo metodo ritorna una stringa, ed e' la lista di tutti i sensori del Nao.
    """
    def GetSensor(self):
        return self.motion.getSensorNames()
    

    """
    Questo metodo fa ritornare il viso del Nao nella sua posizione iniziale.
    """
    def FixHead(self):
        self.motion.angleInterpolationWithSpeed(["HeadYaw", "HeadPitch"], [0.0, 0.0], 1.0)


    """
    Questo metodo registra un video tramite la fotocamera del Nao.
    Argomenti:
    - Secondi: durata che il video avra'. e' un intero.
    - NomeVideo: il nome che il video dovra' avere. e' una stringa. 
    """
    def RegistraVideo(self, Secondi, NomeVideo):
            self.record.setResolution(1)
            self.record.setFrameRate(10)
            self.record.setVideoFormat("avi")
            self.record.startRecording(r"/home/nao/recordings/cameras", NomeVideo)
            time.sleep(Secondi)
            videoInfo = self.record.stopRecording()
        
    """
    Questo metodo scatta una foto tramite la fotocamera del Nao.
    Andra' nella cartella: home/nao/recordings/cameras/
    Argomenti:
    - NomeFoto: il nome che la foto dovra' avere. e' una stringa.
    """
    def ScattaFoto(self, NomeFoto):
        self.photo.setPictureFormat("png")
        self.photo.takePicture("home/nao/recordings/cameras",NomeFoto)


    def Animazione(self, nome, fps=25):
        """
        Il nome dell'animazione va in inglese
        Tai Chi Chuan funziona solo a 5 fps
        """
        if(not nome in self.animations.keys()):
            try:
                self.animations[nome] = XarReader(".\\animations\\"+nome+".xar", 1.0/fps).get_data()
            except:
                print("Animazione non disponibile")
                return

        self.SetPostura("Stand",0.5)
        joints, times, angles = self.animations[nome]
        self.motion.angleInterpolationBezier(joints, times, angles)
        self.SetPostura("Stand",0.5)