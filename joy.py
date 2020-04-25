import subprocess
import pygame
import os,sys

# headless
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame.display
pygame.display.init()
screen = pygame.display.set_mode((0,0))
print("screen ok")

# buffer of <1024 makes sounds distorted on RPi ver 1.
pygame.mixer.pre_init(frequency=44100,  size=-16, channels=1, buffer=1024)

# Very arbitrary
pygame.init()
kick_sound = pygame.mixer.Sound("/usr/share/hydrogen/data/drumkits/The Black Pearl 1.0/PearlKick-Softest.wav")
snare_sound = pygame.mixer.Sound("/usr/share/hydrogen/data/drumkits/The Black Pearl 1.0/PearlSnare-Soft.wav")
tom_sound = pygame.mixer.Sound("/usr/share/hydrogen/data/drumkits/The Black Pearl 1.0/PearlTom1-Med.wav")
hihat_sound=pygame.mixer.Sound("/usr/share/hydrogen/data/drumkits/The Black Pearl 1.0/SabianHatSwish-Soft.wav")
cymbal_sound=pygame.mixer.Sound("/usr/share/hydrogen/data/drumkits/The Black Pearl 1.0/SabianCrash-Soft.wav")

clock = pygame.time.Clock() #added line
ps3 = pygame.joystick.Joystick(0)
ps3.init()
print("Initialized ps3")

from queue import Queue
from threading import Thread

# init all queues and threads per actor
qKick = Queue()
qhiHat = Queue()
qSnare = Queue()
qTom = Queue()
qCymbal = Queue()

def playDrumWorker(sound, q):
    buttonBefore=0
    while True:
        hit = q.get()
        #print("Got hit")
        if hit == 1 and buttonBefore == 0:
            buttonBefore = 1;
            pygame.mixer.Sound.play(sound)
            clock.tick(50)  #added line
            buttonBefore = 0
            print("Played")
        #clock.tick(10)


print("Strating workers")
t = Thread(target=playDrumWorker, args = (kick_sound, qKick))
t.daemon = True
t.start()

t2 = Thread(target=playDrumWorker, args = (snare_sound, qSnare))
t2.daemon = True
t2.start()

t3 = Thread(target=playDrumWorker, args = (tom_sound, qTom))
t3.daemon = True
t3.start()

t4 = Thread(target=playDrumWorker, args = (hihat_sound, qhiHat))
t4.daemon = True
t4.start()

t5 = Thread(target=playDrumWorker, args = (cymbal_sound, qCymbal))
t5.daemon = True
t5.start()
print("Main loop starting")

kick=0

while True:
        try:
 #
    # EVENT PROCESSING STEP
    #
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
                for event in pygame.event.get(): # User did something
                        buttons = [ps3.get_button(0),ps3.get_button(1),ps3.get_button(2),ps3.get_button(3),ps3.get_button(4)]
                        if event.type == pygame.QUIT:
                                done = True # Flag that we are done so we exit this loop.
                        elif event.type == pygame.JOYBUTTONDOWN:
                                if buttons[4]==1 and kick==0:
                                        kick = 1
                                        qKick.put(buttons[4])
                                        print("Put kick")
                                elif buttons[2]==1:
                                        qhiHat.put(buttons[2])
                                        print("Put Hihat")
                                elif buttons[3]==1:
                                        qSnare.put(buttons[3])
                                        print("Put Snare")
                                elif buttons[0]==1:
                                        qTom.put(buttons[0])
                                        print("Put Tom")
                                elif buttons[1]==1:
                                        qCymbal.put(buttons[1])
                                        print("Put Cymbal")
                        elif event.type == pygame.JOYBUTTONUP:
                                # print("Joystick button released.")
                                if buttons[4]==0 and kick == 1:
                                        kick = 0
                                        print("Kick released")


                #removed refs to buttons 13-16 in the following line
                #buttons = [ps3.get_button(0),ps3.get_button(1),ps3.get_button(2),ps3.get_button(3),ps3.get_button(4),ps3.get_button(5),ps3.get_button(6),ps3.get_button(7),ps3.get_button(8),ps3.get_button(9),ps3.get_button(10),ps3.get_button(11),ps3.get_button(12)]
                #print(buttons)
                #subprocess.call("clear")
        except KeyboardInterrupt:
                print("Exiting")
                raise
q.join()
