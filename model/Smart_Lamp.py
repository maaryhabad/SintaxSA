import os
import pygame
from model.Electronic import Electronics


class Smart_Lamp(Electronics):
    try:
        icon_path = os.path.join(Electronics.assets_path, 'smart_lamp_icon.png')
        icon = pygame.image.load(icon_path)
        icon = pygame.transform.smoothscale(icon, (50, 50))
    except pygame.error:
        print("Erro ao carregar a imagem da Smart Lamp! Verifique o caminho.")
        icon = pygame.Surface((50, 50))

    def __init__(self, pos_x: int, pos_y: int):
        super().__init__(power_on=False, color=(255, 255, 0), pos_x=pos_x, pos_y=pos_y, icon_name=icon_name)
        

    def draw(self, screen):
        screen.blit(Smart_Lamp.icon_image, (self.rect.x, self.rect.y))
        if self.power_on:
            pygame.draw.circle(screen, (255, 255, 100, 80), self.rect.center, 30, width=0)