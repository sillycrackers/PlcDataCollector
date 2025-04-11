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

        surface = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(surface,color="red",center = (radius,radius),radius=radius)

        #Set the image of the sprite as the circle
        self.image=surface
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.current_speed = 0

    def update(self, *args, **kwargs):

        if "set_pos" in kwargs.keys():
            self.set_pos(kwargs["set_pos"][0],kwargs["set_pos"][1])


    def set_pos(self, x, y):
        self.x = x
        self.y = y

        self.rect.center = (self.x, self.y)

    def get_coord(self):

        return self.x, self.y