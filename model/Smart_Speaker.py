import os
import pygame
from model.Electronic import Electronics


class Smart_Speaker(Electronics):

    try:
        icon_path = os.path.join(Electronics.assets_path, 'smart_speaker_icon.png')
        icon = pygame.image.load(icon_path)
        icon = pygame.transform.smoothscale(icon, (50, 50))
    except pygame.error:
        print("Erro ao carregar a imagem do Smart Speaker! Verifique o caminho.")
        icon = pygame.Surface((50, 50))

    def __init__(self, power_on: bool, color: tuple, pos_x: int, pos_y: int):
        super().__init__(power_on, color, pos_x, pos_y)
        self.power_on = False
        self.playing_music = False
        self.color(0, 100, 200)

    def play_music(self):
        if self.power_on:
            self.playing_music = True
            return("Playing music...")
        else:
            return("Cannot play music. The speaker is off.")
        
    def draw(self, screen):
        screen.blit(self.icon, (self.rect.x, self.rect.y))
        if self.tocando_musica:
            pygame.draw.arc(screen, (0, 255, 255), self.rect.inflate(20, 20), 0, 3.14, 3)