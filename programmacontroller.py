import pygame

pygame.init()
pygame.joystick.init()

scherm = pygame.display.set_mode((500, 200))
pygame.display.set_caption("Controllerknoppen testen")

klok = pygame.time.Clock()
controllers = []

for i in range(pygame.joystick.get_count()):
    controller = pygame.joystick.Joystick(i)
    controller.init()
    controllers.append(controller)

    print(f"\nController {i}: {controller.get_name()}")
    print(f"Instance ID: {controller.get_instance_id()}")
    print(f"Aantal knoppen: {controller.get_numbuttons()}")

print("\nDruk op A, B, X, Y, L, R, Select en Start.")
print("Sluit het venster om te stoppen.")

actief = True

while actief:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            actief = False

        elif event.type == pygame.JOYBUTTONDOWN:
            print(
                f"INGEDRUKT: controller {event.instance_id}, "
                f"knop {event.button}"
            )

        elif event.type == pygame.JOYBUTTONUP:
            print(
                f"LOSGELATEN: controller {event.instance_id}, "
                f"knop {event.button}"
            )

        elif event.type == pygame.JOYDEVICEADDED:
            print("Controller toegevoegd.")

        elif event.type == pygame.JOYDEVICEREMOVED:
            print("Controller verwijderd.")

    klok.tick(60)

pygame.quit()