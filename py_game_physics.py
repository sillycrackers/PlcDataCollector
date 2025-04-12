import pygame


from physics_sim import *
from file_management import *


class MyPyGame:
    def __init__(self):

        pygame.init()
        pygame.display.set_icon(pygame.image.load(resource_path("gui\\imgs\\data_icon_big.png")))
        pygame.display.set_caption("Plc Data Collector - Physics Simulator")
        self.screen = pygame.display.set_mode((600, 750))
        self.clock = pygame.time.Clock()

        #labels
        self.text_font = pygame.font.SysFont("calibri", 24)

        #balls
        self.ball1 = Ball(25,1,"red",10,100)
        self.ball2 = Ball(40, 1, "green", 100, 60)
        self.ball3 = Ball(5, 1, "pink", 200, 200)
        self.ball4 = Ball(70, 1, "blue", 90, 10)
        self.ball5 = Ball(10, 1, "purple", 300, 150)

        self.balls = pygame.sprite.Group()
        # noinspection PyTypeChecker
        self.balls.add(self.ball1)
        # noinspection PyTypeChecker
        self.balls.add(self.ball2)
        # noinspection PyTypeChecker
        self.balls.add(self.ball3)
        # noinspection PyTypeChecker
        self.balls.add(self.ball4)
        # noinspection PyTypeChecker
        self.balls.add(self.ball5)



    def run(self):



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

            self.screen.fill("black")

            label1 = self.text_font.render(f"Y Speed:  {self.ball1.y_speed:.2f}", True, "white")
            self.screen.blit(label1, (100,100))
            self.ball1.calc_position(self.screen, dt)
            self.ball2.calc_position(self.screen, dt)
            self.ball3.calc_position(self.screen, dt)
            self.ball4.calc_position(self.screen, dt)
            self.ball5.calc_position(self.screen, dt)
            self.balls.draw(self.screen)

            pygame.display.flip()

            #Time in seconds
            dt = self.clock.tick(60) / 1000
            #Acumulated time in seconds
            vt += dt


        pygame.quit()