import pygame #Importeer modules (pygame is nodig om het scherm te kunnen maximaliseren)
import play
import random

breedte = 1280 #Beelscherminstellingen (Automatisch fullscreen starten lijkt binnen Coderius play niet mogelijk)
hoogte = 720
play.screen.width = breedte
play.screen.height = hoogte
pygame.display.set_mode((breedte, hoogte), pygame.RESIZABLE)

intro = play.new_video("Ghost_Intro.mp4", autoplay=True, controls=False) #Intro-video
play.set_backdrop('black')
bgm = play.new_sound("Pumpkin_Village.mp3", loops=-1) #Achtergrondmuziek

@play.when_video_ends(intro)
def intro_klaar():
    intro.remove()
    bgm.play()
    toon_menu()

#Globals
score = 0
hp = 5
spel_actief = False
pompoen_actief = False
heksen = 0

#Spawn elementen hoofdmenu
titel = play.new_image(image="Title_Image.jpg", y=175)
tip = play.new_text(words="Tip: Maximaliseer het scherm voor de beste spelervaring.", color='ivory', font_size=42, y=-300)
start_knop = play.new_button(text="Start Spel", border_radius=25, height=175, width=350, color='orange', hover_color='darkorange', text_color='black', font_size=75, x=-275, y=-125)
settings_knop = play.new_button(text="Opties", border_radius=25, height=175, width=350, color='orange', hover_color='darkorange', text_color='black', font_size=75, x=275, y=-125)

#Spawn elementen settings
menu_knop = play.new_button(text="Hoofdmenu", border_radius=25, height=175, width=350, color='orange', hover_color='darkorange', text_color='black', font_size=75, x=-350, y=275)
video_knop = play.new_button(text="Intro Video", border_radius=25, height=175, width=350, color='orange', hover_color='darkorange', text_color='black', font_size=75, x=350, y=275)
schuif = play.new_slider(min_value=0, max_value=10, width=600, height=25, value=10, y=20)
schuif2 = play.new_slider(min_value=0, max_value=10, width=600, height=25, value=10, y=-130)
volume_muziek = play.new_text(words="Volume muziek", color='ivory', font_size=42, y=75)
volume_effecten = play.new_text(words="Volume effecten", color='ivory', font_size=42, y=-75)
uitleg_besturing = play.new_text(words="Bewegen kan met WASD, de pijltoetsen", color='ivory', font_size=42, y=-250)
uitleg_besturing2 = play.new_text(words="of de D-pad van een SNES-controller", color='ivory', font_size=42, y=-300)
uitleg_bonus = play.new_text(words="Spelers met een SNES-controller hebben een speciale bonus-kracht", color='ivory', font_size=42, y=-375)

#Spawn elementen gameplay
speler = play.new_image(image="spookje.png", transparency=75) #Spawn speler, muren, achtergrond
pompoen = play.new_image(image="Pumpkin.png", x=2000, y=2000)
heks1 = play.new_image(image="Enemy_Witch.png", x=-2000, y=-2000)
heks2 = play.new_image(image="Enemy_Witch_Mirror.png", x=-2000, y=2000)
vloer = play.new_box(color='black', width=1920, height=30, y=-430)
plafond = play.new_box(color='black', width=1920, height=60, y=430)
muur_links = play.new_box(color='black', width=150, height=1080, x=-815)
muur_rechts = play.new_box(color='black', width=150, height=1080, x=815)

#Spawn elementen gameplay UI
score_tekst = play.new_text(words="0", color='ivory', font_size=20, x=-475, y=420)
timer_tekst = play.new_text(words="00:00", color='ivory', font_size=20, y=420 )
hpbalk = play.new_progress_bar(min_value=0, max_value=5, value=5, bar_color='crimson', background_color='darkgrey', x=475, y=423)

#Audio
spawn_geluid = play.new_sound("Wave.wav")
pompoen_pickup = play.new_sound("laserShoot.wav")
heks_geluid = play.new_sound("Witch_Laugh.mp3")

#Verberg ongebruikte elementen
def verberg_menu():
    titel.hide() #Verberg hoofdmenu
    tip.hide()
    start_knop.hide()
    settings_knop.hide()

def verberg_settings():
    menu_knop.hide()
    video_knop.hide()
    schuif.hide()
    schuif2.hide()
    volume_muziek.hide()
    volume_effecten.hide()
    uitleg_besturing.hide()
    uitleg_besturing2.hide()
    uitleg_bonus.hide()

def verberg_gameplay():
    speler.hide()
    pompoen.hide()
    heks1.hide()
    heks2.hide()
    vloer.hide()
    plafond.hide()
    muur_links.hide()
    muur_rechts.hide()

def verberg_gameplay_ui():
    score_tekst.hide()
    timer_tekst.hide()
    hpbalk.hide()

verberg_menu()
verberg_settings()
verberg_gameplay()
verberg_gameplay_ui()

def toon_menu(): #Functies om verschillende game states te tonen
    titel.show()
    tip.show()
    start_knop.show()
    settings_knop.show()

def toon_settings():
    menu_knop.show()
    video_knop.show()
    schuif.show()
    schuif2.show()
    volume_muziek.show()
    volume_effecten.show()
    uitleg_besturing.show()
    uitleg_besturing2.show()
    uitleg_bonus.show()

def toon_gameplay():
    play.set_backdrop_image('BG_Graveyard.jpg')
    speler.x = 0
    speler.y = 0
    speler.show()
    vloer.show()
    plafond.show()
    muur_links.show()
    muur_rechts.show()
    speler.start_physics(obeys_gravity=False, can_move=True, stable=False, x_speed=0, y_speed=0) #Start gameplay physics
    vloer.start_physics(obeys_gravity=False, stable=True)
    plafond.start_physics(obeys_gravity=False, stable=True)
    muur_links.start_physics(obeys_gravity=False, stable=True)
    muur_rechts.start_physics(obeys_gravity=False, stable=True)

def toon_gameplay_ui():
    score_tekst.show()
    timer_tekst.show()
    hpbalk.show()
    @play.repeat_forever
    async def timer_bijhouden():
        waarde_timer = 0
        while True:
            await play.timer(seconds=1)
            waarde_timer += 1
            timer_tekst.words = (f"{waarde_timer//60}:{waarde_timer%60}")

@start_knop.when_clicked #Input menu
def klik_start():
    toon_gameplay()
    toon_gameplay_ui()
    verberg_menu()
    global spel_actief
    spel_actief = True

@settings_knop.when_clicked
def klik_settings():
    toon_settings()
    verberg_menu()

@schuif.when_changed #Input settings
def volume_slider(waarde):
    bgm.volume = (waarde/10)

@menu_knop.when_clicked
def klik_menu():
    toon_menu()
    verberg_settings()

@video_knop.when_clicked
def klik_video():
    verberg_settings()
    bgm.volume = 0
    replay = play.new_video("Ghost_Intro.mp4", autoplay=True, controls=False)
    @play.when_video_ends(replay)
    def replay_klaar():
        replay.remove()
        toon_settings()
        bgm.volume = 1

#Gebeurtenissen gameplay
def verhoog_score(punten):
    global score
    score += punten
    score_tekst.words = str(score)

def verlies_hp():
    global hp
    hp -= 1
    hpbalk.value = hp

@play.repeat_forever
async def controleer_pompoenen():
    global pompoen_actief
    if not spel_actief or not pompoen_actief:
        return
    if speler.is_touching(pompoen):
        await play.timer(seconds=0.15)
        pompoen.hide()
        pompoen_actief = False
        verhoog_score(100)
        pompoen_pickup.play()

@play.repeat_forever
async def pompoen_spawn():
    global spel_actief
    global pompoen_actief
    minimum_afstand = 250
    while True:
        if spel_actief == True and pompoen_actief == False:
            await play.timer(seconds=10)
            spawn_x = play.random_number(-680, 680)
            spawn_y = play.random_number(-350, 350)
            while speler.distance_to(x=spawn_x, y=spawn_y) < minimum_afstand:
                spawn_x = play.random_number(-680, 680)
                spawn_y = play.random_number(-350, 350)
            pompoen.x = spawn_x
            pompoen.y = spawn_y
            pompoen.show()
            pompoen.start_physics(obeys_gravity=False, sensor=True)
            pompoen_actief = True
            spawn_geluid.play()
        else:
            await play.timer(seconds=0.2)

@play.repeat_forever
async def heks_spawn1():
    global spel_actief
    global heksen
    minimum_afstand = 500
    while True:
        if spel_actief == True and heksen == 0:
            await play.timer(seconds=10)
            spawn_x = play.random_number(-600, 600)
            spawn_y = play.random_number(-300, 300)
            while speler.distance_to(x=spawn_x, y=spawn_y) < minimum_afstand:
                spawn_x = play.random_number(-600, 600)
                spawn_y = play.random_number(-300, 300)
            pompoen.x = spawn_x
            pompoen.y = spawn_y
            pompoen.show()
            pompoen.start_physics(obeys_gravity=False, sensor=True)
            pompoen_actief = True
            heks_geluid.play()
        else:
            await play.timer(seconds=0.2)

@play.repeat_forever
async def passieve_score():
    while True:
        await play.timer(seconds=1.5)
        if spel_actief:
            verhoog_score(1)

#Beweging controller
horizontaal = 0.0 # Onthoud de huidige richting van de D-pad
verticaal = 0.0
snelheid = 250
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

#@play.controllers.while_button_pressed(0, 0) #Skills
#def groei(button):
#    if speler.size < 50:
#        speler.size = speler.size+0.45
#@play.controllers.while_button_pressed(0, 1)
#def krimp(button):
#    if speler.size > 8:
#        speler.size = speler.size-0.45

#Spawn heks
#Update HPbar 
#Game Over

play.start_program()