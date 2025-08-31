class Developer():
    def __init__(self, name, color, level, description):
        self.name = name
        self.color = color
        self.level = level
        self.description = description

    @staticmethod
    def load_developers():
        return [
            Developer('Ana', (255, 100, 100), 'Júnior', 'Recebe dicas visuais e feedback detalhado.'),
            Developer('Bruno', (100, 255, 100), 'Pleno', 'Desafios intermediários e dicas ocasionais.'),
            Developer('Carla', (100, 100, 255), 'Sênior', 'Desafios avançados e pouca ajuda.'),
            Developer('Diego', (255, 200, 50), 'Sênior', 'Desafios complexos e sem dicas.'),
        ]