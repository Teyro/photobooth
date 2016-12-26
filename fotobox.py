# -*- coding: utf-8 -*-
# Benötigte Module importieren unter anderen PyGame für Python3
#import RPi.GPIO as GPIO
import time, os, subprocess
import pygame
import pygame.camera
from pygame.locals import *

# GPIO setup
#GPIO.setmode(GPIO.BCM)
# Switch für Facebook
#FBSWITCH = 24
#GPIO.setup(SWITCH1, GPIO.IN)
# Switch fürs Drucken
#PRSWITCH = 25
#GPIO.setup(SWITCH4, GPIO.IN)
#PRINT = 22
#GPIO.setup(PRINT, GPIO.IN)


# Initialisieren der Module warum das beim Import nicht passiert ist mir schleierhaft ;)
pygame.init()
pygame.camera.init()

# Countdown Bilder laden und als Variabale laden, noch lange nicht final nur quasi schnell hingerotzt
counterslideshow = 0
img1 = pygame.image.load('img/1.png')
img2 = pygame.image.load('img/2.png')
img3 = pygame.image.load('img/3.png')
img4 = pygame.image.load('img/4.png')
img5 = pygame.image.load('img/5.png')
# Fotofertig soll nachher das mit Gphoto aufgenomme letzte Bild sein
fotofertig = pygame.image.load('photobooth_images/lastest_pic.jpg')
# Dieses Bild wird nachher neben dem Knopf zum teilen gesetzt
facebook = pygame.image.load('img/facebook.png')
# Indralogo ist das Logo vom Club in dem ich arbeite, das Rohbild soll nicht ediert werden von daher das Overlay Bild
indralogo = pygame.image.load('img/indralogo.png')
# Für spätere Versionen ist angedacht drucken zu implementieren
#drucken = pygame.image.load('img/drucken.png')
bittewarten = pygame.image.load('img/bittewarten.png')

# Countdown Timer
countd = 10
# Auflösung
size = (1280,720)
# Schild ist die Veriable für die Position des Countdowns wenns da ne Automatik gibt das Zentriert anzuordnen wäre ich dankbar :D
schild = (515,100)

# Liste der vorhandenen Webcams ermitteln
camlist = pygame.camera.list_cameras()
# wenn ein Kameragerät gefunden wurde ...
if camlist:
    # Erste Webcam auswählen, als Fallback für den Fall dass ich mehrere Webcams im System habe
    camname = camlist[0]
    print("Kamera gefunden: " + camname)

    # Kamera-Objekt erzeugen mit gewünschter Auflösung siehe oben....
    cam = pygame.camera.Camera(camname,size)
    # Kamera starten
    cam.start()

    # Fenster zur Darstellung der Bilder erzeugen im Vollbild weil Kiosk System
    screen = pygame.display.set_mode(size, 0)
#   Fullscreen für Kiosk Modus
#    screen = pygame.display.set_mode(size, FULLSCREEN, 16)
    #Name des Programms
    pygame.display.set_caption('Indra Fotobox')
    # Zähler für die Anzahl der gelesenen Bilder initialisieren
    i=0
    # Endlosschleife, abbrechen mit Esc oder per GPIO (gemopst aus deinem Code und angepasst)
    run = True
    while(run):
        # Zähler hochzählen und Bildnummer ausgeben
        i = i+1
        print("Foto " + str(i))
        # Bild von der Kamera auslesen
        image = cam.get_image()
        # Neues Bild in das Fenster einbinden und darstellen
        screen.blit(image,(0,0))
        # Sofern per Tastendruck der Countdown gesetzt wurde zählt der hier mit runter... Leider viel zu schnell time.sleep hält das ganze System an
        if countd == 5:
            countd = countd-1
            print("Foto in 5. Sekunden")
            screen.blit(img5,schild)
            #time.sleep (1)
        elif countd == 4:
            countd = countd-1
            screen.blit(img4,schild)
            print("Foto in 4. Sekunden")
            #time.sleep (1)
        elif countd == 3:
            countd = countd-1
            screen.blit(img3,schild)
            print("Foto in 3. Sekunden")
            #time.sleep (1)
        elif countd == 2:
            countd = countd-1
            screen.blit(img2,schild)
            print("Foto in 2. Sekunden")
            #time.sleep (1)
        elif countd == 1:
            countd = countd-1
            screen.blit(img1,schild)
            print("Foto in 1. Sekunden")
            #time.sleep (1)
        elif countd == 0:
            os.system("fswebcam -d /dev/video1 -r 1280x720 --no-banner photobooth_images/photobooth-nummer" + str(i) + ".jpg")
            os.system("yes | cp -i photobooth_images/photobooth-nummer" +str(i) +".jpg  photobooth_images/lastest_pic.jpg")
            screen.blit(bittewarten,(0,0))
            fotofertig = pygame.image.load('photobooth_images/lastest_pic.jpg')
            pygame.display.flip()
            time.sleep (1)
            countd = countd-1
            screen.blit(fotofertig,(0,0))
            screen.blit(facebook,(0,592))
            screen.blit(indralogo,(900,592))
            print("Foto wird angezeigt")
            # Blöde Frage aber warum geht das hier nicht wenn ich hier was drücke in dem Fall f oder b wills nicht
            #events = pygame.event.get()
            #for e in events:
            #    if e.type == KEYDOWN and e.key == K_d):
            #        print("Druckvorgang gestartet")
            #    if e.type == KEYDOWN and e.key == K_f):
            #        print("Facebook gestartet")

            pygame.display.flip()
            time.sleep (3)
            
        pygame.display.flip()

        # Drücken der Taste Esc im Bildfenster beendet das Programm, Leertaste oder GPIO startet Aufnahme
        events = pygame.event.get()
        for e in events:
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                # Schleife beenden
                run = False
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_SPACE):
                countd = 5
                print("Countdown gestartet")
# Kamera und Fenster schließen
    cam.stop()
    pygame.display.quit()
else:
    # wenn kein Kameragerät gefunden wurde ...
    print("Keine Kamera gefunden, Programm wird beendet Christian anrufen!")
