
import os

# ASSETS PATH
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
ELECTRONICS_ASSETS_PATH = os.path.join(ASSETS_PATH, "electronics")

# CONFIGURAÇÕES DA TELA
WIDTH = 1280
HEIGHT = 800

# CORES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (200, 200, 200)
ACTIVE_BLUE = (0, 120, 215)

# EXPLICAÇÕES
EXPLICACAO_ELETRO = "Antes de criarmos o robot_vacuum, vamos entender o conceito de herança.",
    "Imagine uma classe mãe chamada 'Eletrodomestico'.",
    "Ela pode ligar, desligar e conectar na energia.",
    "robot_vacuum, SmartLamp e Smart_Speaker são eletrodomésticos,",
    "ou seja, herdam comportamentos básicos dessa classe mãe.",
    "",
    "Pressione qualquer tecla para continuar."