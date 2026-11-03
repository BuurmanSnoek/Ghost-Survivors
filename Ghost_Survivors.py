import pygame #Importeer modules (pygame is nodig om het scherm te kunnen maximaliseren)
import play

breedte = 1280 #Beelscherminstellingen (Automatisch fullscreen starten lijkt binnen Coderius play niet mogelijk)
hoogte = 720
play.screen.width = breedte
play.screen.height = hoogte
pygame.display.set_mode((breedte, hoogte), pygame.RESIZABLE)

#Intro-video
intro = play.new_video("Ghost_Intro.mp4", autoplay=True, controls=False)

@play.when_video_ends(intro)
def intro_klaar():
    intro.remove()

#Startscherm
play.set_backdrop_image('BG_Graveyard.jpg')
#start_knop = play.new_button(text="Start spel", border_radius=25, color='orange', text_color='black', font_size=39)


speler = play.new_image(image="spookje.png", size=6, transparency=75) #Spawn speler, muren, achtergrond
speler.start_physics(obeys_gravity=False, can_move=True, stable=False, x_speed=0, y_speed=0)
vloer = play.new_box(color='black', width=1920, height=30, y=-520)
vloer.start_physics(obeys_gravity=False, stable=True)
plafond = play.new_box(color='black', width=1920, height=30, y=350)
plafond.start_physics(obeys_gravity=False, stable=True)
muur_links = play.new_box(color='black', width=150, height=1080, x=-690)
muur_links.start_physics(obeys_gravity=False, stable=True)
muur_rechts = play.new_box(color='black', width=150, height=1080, x=940)
muur_rechts.start_physics(obeys_gravity=False, stable=True) 
#start_knop.remove
#Glitch komt waarschijnlijk doordat spookje aan 't begin springt van originele spawn positie naar gemaximaliseerde spawn.

snelheid = 250

#Beweging controller
horizontaal = 0.0 # Onthoud de huidige richting van de D-pad
verticaal = 0.0
@play.controllers.when_axis_moved(1, 0)
def dpad_horizontaal(axis, value):
    global horizontaal
    horizontaal = value
@play.controllers.when_axis_moved(1, 1)
def dpad_verticaal(axis, value):
    global verticaal
    verticaal = value
@play.when_key_pressed("a", "left") #Beweging toetsenbord, opties: 1) WASD; 2) Arrow keys
def toetsenbord_links():
    global horizontaal
    horizontaal -= 1
@play.when_key_pressed("d", "right")
def toetsenbord_rechts():
    global horizontaal
    horizontaal += 1
@play.when_key_pressed("w", "up")
def toetsenbord_boven():
    global verticaal
    verticaal -= 1
@play.when_key_pressed("s", "down")
def toetsenbord_onder():
    global verticaal
    verticaal += 1
@play.when_key_released("a", "left") #Beweging stoppen bij loslaten van een bewegingstoets
def toetsenbord_links_los():
    global horizontaal
    horizontaal += 1
@play.when_key_released("d", "right")
def toetsenbord_rechts_los():
    global horizontaal
    horizontaal -= 1
@play.when_key_released("w", "up")
def toetsenbord_boven_los():
    global verticaal
    verticaal += 1
@play.when_key_released("s", "down")
def toetsenbord_onder_los():
    global verticaal
    verticaal -= 1
@play.repeat_forever
def beweeg_speler():
    if horizontaal < -0.5:  # Horizontale beweging
        speler.physics.x_speed = snelheid*-1
    elif horizontaal > 0.5:
        speler.physics.x_speed = snelheid
    else:
        speler.physics.x_speed = 0
    if verticaal < -0.5:    # Verticale beweging
        speler.physics.y_speed = snelheid
    elif verticaal > 0.5:
        speler.physics.y_speed = snelheid*-1
    else:
        speler.physics.y_speed = 0

#Skills
@play.controllers.while_button_pressed(0, 0)
def groei(button):
    if speler.size < 11:
        speler.size = speler.size+0.15
@play.controllers.while_button_pressed(0, 1)
def krimp(button):
    if speler.size > 3:
        speler.size = speler.size-0.15

#

#Vijanden

#Vijanden

#Score

#Timer

#Wapens

#HP

play.start_program()