# personagens.py
import pygame


# CLASSE-MÃE (ou Superclasse)
# A base para todos os nossos desenvolvedores.
class Desenvolvedor:
    def __init__(self, nome, pos_x, pos_y):
        self.nome = nome
        self.imagem_base = pygame.image.load('assets/dev_icon.png')
        self.imagem = pygame.transform.scale(self.imagem_base, (40, 40))
        self.rect = self.imagem.get_rect(center=(pos_x, pos_y))
        self.status = f"Olá, sou {self.nome}!"
        self.especialidade = "Generalista"
        self.cor = (50, 50, 50)  # Cor para o dev genérico

    def trabalhar(self):
        self.status = "Analisando requisitos..."
        print(self.status)

    def desenhar(self, tela):
        # Desenha um círculo colorido para identificar o tipo de dev
        pygame.draw.circle(tela, self.cor, self.rect.center, 25)
        tela.blit(self.imagem, self.rect)


# --- AQUI ACONTECE A HERANÇA ---

# CLASSE-FILHA (ou Subclasse)
# Herda tudo de 'Desenvolvedor' e adiciona suas próprias características.
class DevFrontEnd(Desenvolvedor):
    def __init__(self, nome, pos_x, pos_y):
        # super().__init__() chama o construtor da classe-mãe.
        # Isso garante que o DevFrontEnd tenha nome, imagem, rect, etc.
        super().__init__(nome, pos_x, pos_y)

        # Atributos específicos desta subclasse
        self.especialidade = "Front-End"
        self.cor = (0, 150, 255)  # Azul para Front-End
        self.status = f"Pronto para criar interfaces incríveis!"

    # Método exclusivo (e sobrescrito) da subclasse
    def trabalhar(self):
        self.status = "Codificando em React e CSS!"
        print(self.status)


# CLASSE-FILHA (ou Subclasse)
# Também herda de 'Desenvolvedor'.
class DevBackEnd(Desenvolvedor):
    def __init__(self, nome, pos_x, pos_y):
        # Reutilizando o construtor da classe-mãe
        super().__init__(nome, pos_x, pos_y)

        # Atributos específicos
        self.especialidade = "Back-End"
        self.cor = (255, 100, 0)  # Laranja para Back-End
        self.status = f"Estruturando o servidor e o banco de dados."

    # Método exclusivo
    def trabalhar(self):
        self.status = "Otimizando queries no banco de dados!"
        print(self.status)