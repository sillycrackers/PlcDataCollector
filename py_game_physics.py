import pygame
from PIL import Image, ImageTk
from PIL.Image import Resampling


from file_management import *


class MyPyGame:
    def __init__(self):
        ...

    def run(self):
        pygame.init()

        pygame.display.set_icon(pygame.image.load(resource_path("gui\\imgs\\data_icon_big.png")))
        pygame.display.set_caption("Plc Data Collector - Physics Simulator")

        screen = pygame.display.set_mode((600, 750))
        clock = pygame.time.Clock()
        a = 9.81
        dt = 0
        vt = 0
        v = 0
        circle_pos = pygame.Vector2(screen.get_width() / 2, 40)

        #Insantaneous velocity : V = Vi + a*t

        # = 49 m/s = 176 km/hr

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            #grey

            if not (circle_pos.y + 40) > screen.get_height():
                screen.fill(color=(161, 161, 161))
                pygame.draw.circle(screen, "red", circle_pos, 40)

            circle_pos.y += v

            pygame.display.flip()

            #Time in seconds
            dt = clock.tick(60) / 1000

            #Acumulated time in seconds
            vt += dt
            v = a * vt



        pygame.quit()