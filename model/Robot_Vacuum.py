from model.Electronic import Electronics
import pygame
import os


class Robot_Vacuum(Electronics):
    try:
        icon_path = os.path.join(Electronics.assets_path, 'robot_vacuum_icon.png')
        icon = pygame.image.load(icon_path)
        icon = pygame.transform.smoothscale(icon, (50, 50))
    except pygame.error:
        print("Erro ao carregar a imagem do Smart Speaker! Verifique o caminho.")
        icon = pygame.Surface((50, 50))

    def __init__(self, power_on: bool, color: tuple, pos_x: int, pos_y: int, battery_life: int):
        super().__init__(power_on, color, pos_x, pos_y)
        self.battery_life = battery_life  # em porcentagem
        self.moving = False
        self.move_direction = (1, 0)  # (dx, dy) - por padrão, move para a direita


    def draw(self, screen):
        screen.blit(self.icon, (self.rect.x, self.rect.y))
        color_status = (0, 255, 0) if self.power_on else (200, 0, 0)
        pygame.draw.circle(screen, color_status, (self.rect.centerx, self.rect.centery - 15), 7)
        pygame.draw.rect(screen, (50, 50, 50), (self.rect.left, self.rect.bottom + 5, 50, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.left, self.rect.bottom + 5, self.battery_life / 2, 10))
        # print("Drawing the robot vacuum on the screen.")

    def start_cleaning(self):
        if self.power_on and self.battery_life > 0:
            print("The robot vacuum has started cleaning.")
            self.moving = True
        elif not self.power_on:
            print("Please power on the robot vacuum first.")
        else:
            print("Battery is dead. Please recharge.")

    def stop_cleaning(self):
        self.moving = False

    def update(self):
        """Atualiza a posição do robô se estiver em movimento."""
        if self.moving and self.battery_life > 0:
            dx, dy = self.move_direction
            self.rect.x += dx
            self.rect.y += dy
            self.battery_life -= 0.05  # Consome um pouco de bateria ao andar
            if self.battery_life <= 0:
                self.battery_life = 0
                self.moving = False
                print("Battery is dead. Please recharge.")