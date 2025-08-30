import os


class Project:

    def __init__(self, name, description, icon):
        self.name = name
        self.description = description
        self.icon = icon

    @staticmethod
    def load_projects():
        # Carrega os projetos disponíveis (pode ser de um arquivo ou banco de dados)
        assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "projects")
        return [
            Project("Eletrodomésticos Inteligentes", "Construa classes para Robot_Vacuum, Smart_Lamp e Smart_Speaker usando POO.", os.path.join(assets_path, "smart_electronics.png")),
            Project("Sistema de Controle de Portas", "Implemente classes para portas automáticas, com métodos abrir, fechar e trancar.", os.path.join(assets_path, "door_system.png"))
        ]