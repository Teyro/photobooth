# -*- coding: utf-8 -*-
# Load the needed modules for the photoboothy
import RPi.GPIO as GPIO
import time, os,  pygame,  pygame.camera
from pygame.locals import *
# debug is for debug output...0 is disabled 1 is enabled
debug = 0

# GPIO setup auf dem Port 17 und 22 liegen je ein Taster welche entweder fürs Foto benutzt wird (17) und (22) für das teilen auf Facebook per Skript
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(22, GPIO.IN)
# Module initaliserien
pygame.init()
pygame.camera.init()
#set cp als var
os.system("alias cp=cp")
# Countdown Bilder laden und als Variabale laden, noch lange nicht final nur quasi schnell hingerotzt, einige Variablen sind noch ohne Funktion
img1 = pygame.image.load('img/1.png')
img2 = pygame.image.load('img/2.png')
img3 = pygame.image.load('img/3.png')
img4 = pygame.image.load('img/4.png')
img5 = pygame.image.load('img/5.png')
# Fotofertig soll nachher das mit Gphoto aufgenomme letzte Bild sein
#fotofertig = pygame.image.load('/home/teyro/fotobox/photobooth_images/lastest_pic.jpg')
# Dieses Bild wird nachher neben dem Knopf zum teilen gesetzt
facebook = pygame.image.load('img/facebook.png')
# Indralogo ist das Logo vom Club in dem ich arbeite, das Rohbild soll nicht ediert werden von daher das Overlay Bild
indralogo = pygame.image.load('img/indralogo.png')
# Für spätere Versionen ist angedacht drucken zu implementieren
#drucken = pygame.image.load('img/drucken.png')
# Das bitte Warten Schild welches gezeigt wird falls die Datenschieberei auf dem Pi zu lange dauert...
bittewarten = pygame.image.load('img/bittewarten.png')
cheese = pygame.image.load('img/cheese.jpg')

# Countdown Timer, auf 10 gesetzt da der erst bei 5 auslöst....
countd = 10
countdown = 0
# Auflösung des Videostreams, entspricht dann der späteren Bildschirmauflösung....
size = (1280,720)
# Schild ist die Veriable für die Position des Countdowns , wird kurzfristig durch pygame.text ausgetauscht sodass Text statt Grafiken gerendet werden, spart Leistung
schild = (515,100)
posten = 0
# font
font = pygame.font.SysFont("comicsansms", 72)
text = font.render(countd, True, (0, 128, 0))

# Liste der vorhandenen Webcams ermitteln
camlist = pygame.camera.list_cameras()
# wenn ein Kameragerät gefunden wurde ...
if camlist:
    # Erste Webcam auswählen, als Fallback für den Fall dass ich mehrere Webcams im System habe, ist nicht mehr geplant aber wer weiss
    camname = camlist[0]
    if debug == 1:
        print("Kamera gefunden: " + camname)
    # Kamera-Objekt erzeugen mit gewünschter Auflösung siehe oben....
    cam = pygame.camera.Camera(camname,size)
    # Kamera starten
    cam.start()

    # Fenster zur Darstellung der Bilder erzeugen im Vollbild weil Kiosk System
    if debug == 1:
        screen = pygame.display.set_mode(size, 0)
    else:
        screen = pygame.display.set_mode(size, FULLSCREEN, 16)
    #Name des Programms
    pygame.display.set_caption('Indra Fotobox')
    # Zähler für die Anzahl der gelesenen Bilder initialisieren
    i=0
    # Endlosschleife, abbrechen ist nicht vorgesehen nur über kill in konsole
    run = True
    preview  = True
    knipse = False
    while(run):
        pygame.display.flip()
        while(preview):
        # Zähler hochzählen und Bildnummer ausgeben sofern debug = 1
            i = i+1
            if debug == 1:
                print("Foto " + str(i))
        # Bild von der Kamera auslesen
            image = cam.get_image()
        # Neues Bild in das Fenster einbinden und darstellen
            screen.blit(image,(0,0))
        # Drücken der GPIO 17 startet Aufnahme
            if GPIO.input(17) == True or debug == 1:
                countd = 5
                preview = False
                knipse = True
            pygame.display.flip()


# Kamera und Fenster schließen
        while(knipse):
            i = i+1
            if debug == 1:
                print("Foto " + str(i))
# Bild von der Kamera auslesen
            image = cam.get_image()
        # Neues Bild in das Fenster einbinden und darstellen
            screen.blit(image,(0,0)) 
            pygame.display.flip()
            if countd == 5:
                countd = countd-1
                if debug == 1:
                    print("Foto in 5. Sekunden")
                screen.blit(text, 1280- text.get_width() // 2, 240 - text.get_height() // 2)
#                time.sleep (0.05)
                pygame.display.flip()
            elif countd == 4:
                countd = countd-1
                screen.blit(text, 1280- text.get_width() // 2, 240 - text.get_height() // 2)
                if debug == 1:
                    print("Foto in 4. Sekunden")
#                time.sleep (0.05)
                pygame.display.flip()
            elif countd == 3:
                countd = countd-1
                screen.blit(img3,schild)
                if debug == 1:
                    print("Foto in 3. Sekunden")
#                time.sleep (0.05)
                pygame.display.flip()
            elif countd == 2:
                countd = countd-1
                screen.blit(img2,schild)
                if debug == 1:
                    print("Foto in 2. Sekunden")
#                time.sleep (0.05)
                pygame.display.flip()
            elif countd == 1:
                countd = countd-1
                screen.blit(img1,schild)
                if debug == 1:
                    print("Foto in 1. Sekunden")
#                time.sleep (0.05)
                pygame.display.flip()
            elif countd == 0:
                #os.system("fswebcam -d /dev/video1 -r 1280x720 --no-banner photobooth_images/photobooth-nummer" + str(i) + ".jpg")
                # Das selbe fuer ne DSLR Betrieb
                screen.blit(cheese, (0, 0))
                pygame.display.flip()
                os.system("rm /home/teyro/fotobox/photobooth_images/photobooth-nummer" + str(i) + ".jpg")
                os.system("gphoto2 --capture-image-and-download --filename /home/teyro/fotobox/photobooth_images/photobooth-nummer" + str(i) + ".jpg")
                #time.sleep(0.25)
                # Ab hier wird es schmutzig... Da ich über cp immer ne Nachfrage bekomme und über nen y | cp .... nur nen broken Pipe Fehler bekomme ist das der schmutzige fix
                os.system("rm /home/teyro/fotobox/photobooth_images/lastest_pic.jpg")
                os.system("rm /home/teyro/fotobox/photobooth_images/lastest_pic-preview.jpg")
                #time.sleep (0.25)
                os.system("cp -f /home/teyro/fotobox/photobooth_images/photobooth-nummer" +str(i) + ".jpg  /home/teyro/fotobox/photobooth_images/lastest_pic.jpg")
                os.system("/usr/bin/convert -colorspace rgb /home/teyro/fotobox/photobooth_images/lastest_pic.jpg -geometry 1280x -quality 85 /home/teyro/fotobox/photobooth_images/lastest_pic-preview.jpg")
                fotofertig = pygame.image.load("/home/teyro/fotobox/photobooth_images/lastest_pic-preview.jpg")
                time.sleep (1) 
                screen.blit(fotofertig,(0,0))
                screen.blit(facebook,(0,592))
                screen.blit(indralogo,(900,592))
                pygame.display.flip()
                print("Foto wird angezeigt")
                if GPIO.input(22)  == True or debug == 1:
                    os.system("cp -f /home/teyro/fotobox/photobooth_images/lastest_pic.jpg /home/teyro/fotobox/photobooth_images/facebook/upload.jpg")
                    time.sleep (0.5)
                    os.system("/usr/bin/rclone move /home/teyro/fotobox/photobooth_images/facebook/upload.jpg dropbox:/Indra")
                time.sleep (10)
                pygame.display.flip()
                
                #os.system(rm /home/teyro/fotobox/photobooth_images/lastest_pic.jpg)
                knipse = False
                preview = True
        pygame.display.flip()
    pygame.display.flip()
     
    cam.stop()
    pygame.display.quit()
    #GPIO.cleanup()
else:
    # wenn kein Kameragerät gefunden wurde ...
    print("Keine Kamera gefunden, Programm wird beendet Christian anrufen!")
