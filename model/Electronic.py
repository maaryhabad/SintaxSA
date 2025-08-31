from abc import ABC, abstractmethod
import os
import pygame

class Electronic(ABC):
    assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "electronics")
    icon = None

    def __init__(self, power_on: bool, color: tuple, pos_x: int, pos_y: int, ):
        self.rect = pygame.Rect(pos_x - 25, pos_y - 25, 50, 50)
        self.power_on = power_on
        self.color = color
        

    def power_on(self):
        if not self.power_on:
            self.power_on = True
            print("The device is powered on.")

    def power_off(self):
        if self.power_on:
            self.power_on = False
            print("The device is powered off.")

    @abstractmethod
    def draw(self):
        pass