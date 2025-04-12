import tkinter as tk

import pygame
from pygame.sprite import Sprite
from pygame import gfxdraw

class Ball(Sprite):
    def __init__(self, radius=50, ball_id=0, color="red", x=0, y=0):
        Sprite.__init__(self)


        self.radius = radius
        self.x = x
        self.y = y
        self.direction = 1
        self.vi = 0
        self.gravity = 0.5
        self.acc_time = 0
        self.x_speed = 4
        self.y_speed = 0

        surface = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(surface,color="red",center = (radius,radius),radius=radius)

        #Set the image of the sprite as the circle
        self.image=surface
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.current_speed = 0

    def update(self, *args, **kwargs):
        self.calc_position(*args)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

        self.rect.center = (self.x, self.y)

    def get_coord(self):

        return self.x, self.y

    def calc_position(self, screen : pygame.Surface, time):


        self.y_speed += self.gravity
        self.y += self.y_speed
        self.x += self.x_speed

        if self.y < 0 or self.y >= screen.get_height():
            self.y = screen.get_height()
            self.y_speed *= - 1

        if self.x < 0 or self.x >= screen.get_width():
            self.x_speed *= -1


        self.y_speed = self.y_speed + self.gravity * time


        self.set_pos(self.x,self.y)



        print(f"X pos: {self.x}, Y pos: {self.y}, Y speed: {self.y_speed}")


