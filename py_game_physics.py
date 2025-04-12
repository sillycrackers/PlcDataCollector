import pygame


from physics_sim import *
from file_management import *


class MyPyGame:
    def __init__(self):
        ...
        self.ball1 = Ball(25,1,"red",100,100)
        # noinspection PyTypeChecker
        self.balls = pygame.sprite.Group(self.ball1)



    def run(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load(resource_path("gui\\imgs\\data_icon_big.png")))
        pygame.display.set_caption("Plc Data Collector - Physics Simulator")
        screen = pygame.display.set_mode((600, 750))
        clock = pygame.time.Clock()

        #change in time
        dt = 0
        #elapsed time
        vt = 0


        #Insantaneous velocity : V = Vi + a*t

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            if self.ball1.direction < 0:
                vt = 0

            screen.fill("black")

            self.ball1.calc_position(screen, dt)
            self.balls.draw(screen)

            pygame.display.flip()

            #Time in seconds
            dt = clock.tick(60) / 1000
            #Acumulated time in seconds
            vt += dt


        pygame.quit()