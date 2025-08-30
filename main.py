# src/main.py
import pygame
from src.view import View
from src.controller import Controller

def main():
    """Função principal que inicializa e executa o jogo."""
    pygame.init()
    
    LARGURA, ALTURA = 1280, 800
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("SintaxSA: DevLife")

    # Inicializa os componentes MVC
    view = View(screen)
    controller = Controller(screen, view)

    # Inicia o loop principal do jogo
    controller.run()

if __name__ == '__main__':
    main()