import pygame

from physics_sim import *
from file_management import *


class MyPyGame:
    def __init__(self):

        self.ball1 = Ball(40, 1)

    def run(self):
        pygame.init()

        pygame.display.set_icon(pygame.image.load(resource_path("gui\\imgs\\data_icon_big.png")))
        pygame.display.set_caption("Plc Data Collector - Physics Simulator")
        screen = pygame.display.set_mode((600, 750))
        clock = pygame.time.Clock()

        #acceleration
        a = 9.81
        #change in time
        dt = 0
        #elapsed time
        vt = 0
        #current speed
        v = 0

        self.ball1.set_pos(screen.get_width()/2, self.ball1.radius)

        #Insantaneous velocity : V = Vi + a*t

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            #grey

            if not (self.ball1.y + self.ball1.radius) > screen.get_height():
                screen.fill(color=(161, 161, 161))
                pygame.draw.circle(screen, "red", self.ball1.get_coord(), 40)

            self.ball1.y += v

            pygame.display.flip()

            #Time in seconds
            dt = clock.tick(60) / 1000
            #Acumulated time in seconds
            vt += dt
            #calculate velocity
            v = a * vt

        pygame.quit()