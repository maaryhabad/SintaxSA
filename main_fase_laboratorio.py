# main_fase_laboratorio.py
import pygame
import sys
import random
import os

# --- CLASSES DOS OBJETOS QUE O JOGADOR PODE CONSTRUIR ---
class RoboAspirador:
    def __init__(self, pos_x, pos_y):
        self.rect = pygame.Rect(pos_x - 25, pos_y - 25, 50, 50)
        self.bateria = 100
        self.ligado = False
        self.cor = (100, 100, 100)

    def ligar(self):
        if not self.ligado:
            self.ligado = True
            return "Robô ligado!"
        return "Robô já estava ligado."

    def desligar(self):
        if self.ligado:
            self.ligado = False
            return "Robô desligado."
        return "Robô já estava desligado."

    def aspirar(self):
        if self.ligado and self.bateria > 0:
            self.bateria -= 10
            return f"Aspirando... Bateria: {self.bateria}%"
        elif not self.ligado:
            return "Não posso aspirar desligado."
        else:
            return "Bateria esgotada."

    def desenhar(self, tela):
        tela.blit(icon_robo, (self.rect.x, self.rect.y))
        cor_status = (0, 255, 0) if self.ligado else (200, 0, 0)
        pygame.draw.circle(tela, cor_status, (self.rect.centerx, self.rect.centery - 15), 7)
        pygame.draw.rect(tela, (50, 50, 50), (self.rect.left, self.rect.bottom + 5, 50, 10))
        pygame.draw.rect(tela, (0, 255, 0), (self.rect.left, self.rect.bottom + 5, self.bateria / 2, 10))

class SmartLamp:
    def __init__(self, pos_x, pos_y):
        self.rect = pygame.Rect(pos_x - 25, pos_y - 25, 50, 50)
        self.ligado = False
        self.cor = (200, 200, 0)

    def ligar(self):
        self.ligado = True
        return "Lâmpada acesa."

    def desligar(self):
        self.ligado = False
        return "Lâmpada apagada."

    def desenhar(self, tela):
        tela.blit(icon_lamp, (self.rect.x, self.rect.y))
        if self.ligado:
            pygame.draw.circle(tela, (255, 255, 100, 80), self.rect.center, 30, width=0)

class SmartSpeaker:
    def __init__(self, pos_x, pos_y):
        self.rect = pygame.Rect(pos_x - 25, pos_y - 25, 50, 50)
        self.ligado = False
        self.tocando_musica = False
        self.cor = (0, 100, 200)

    def ligar(self):
        self.ligado = True
        return "Speaker pronto."

    def desligar(self):
        self.ligado = False
        self.tocando_musica = False
        return "Speaker desligado."

    def tocar_musica(self):
        if self.ligado:
            self.tocando_musica = True
            return "Tocando música."
        return "Speaker desligado."

    def desenhar(self, tela):
        tela.blit(icon_speaker, (self.rect.x, self.rect.y))
        if self.tocando_musica:
            pygame.draw.arc(tela, (0, 255, 255), self.rect.inflate(20, 20), 0, 3.14, 3)

# --- INICIALIZAÇÃO DO PYGAME ---
pygame.init()
LARGURA, ALTURA = 1200, 750
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
AZUL_ATIVO = (100, 100, 255)
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fase 2: O Laboratório de POO (Corrigido)")

# --- CARREGAMENTO DE ASSETS ---
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
icon_dev = pygame.image.load(os.path.join(ASSETS_PATH, "dev_icon.png"))
icon_robo = pygame.image.load(os.path.join(ASSETS_PATH, "robot_vacuum_icon.png"))
icon_lamp = pygame.image.load(os.path.join(ASSETS_PATH, "smart_lamp_icon.png"))
icon_speaker = pygame.image.load(os.path.join(ASSETS_PATH, "smart_speaker_icon.png"))
icon_dev = pygame.transform.smoothscale(icon_dev, (60, 60))
icon_robo = pygame.transform.smoothscale(icon_robo, (50, 50))
icon_lamp = pygame.transform.smoothscale(icon_lamp, (50, 50))
icon_speaker = pygame.transform.smoothscale(icon_speaker, (50, 50))

# --- PROJETOS/FASES ---
projetos = [
    {
        "nome": "Eletrodomésticos Inteligentes",
        "descricao": "Construa classes para RoboAspirador, SmartLamp e SmartSpeaker usando POO.",
        "icone": icon_robo
    },
    {
        "nome": "Sistema de Controle de Portas",
        "descricao": "Implemente classes para portas automáticas, com métodos abrir, fechar e trancar.",
        "icone": icon_lamp
    }
]
projeto_selecionado = None
atribuindo_dev = True

# --- CONTROLE DE ESTADO DO JOGO ---
desafio_atual = 1
feedback_msg = "Bem-vindo ao Laboratório!"
classe_em_construcao = {'nome': '', 'atributos': set(), 'metodos': set()}
classes_definidas = {}
input_box_active = False
nome_classe_input = ""
objetos_instanciados = []
intro = True

# --- DESAFIOS ---
desafios = {
    1: {
        "nome": "Desafio 1: Encapsulamento",
        "objetivo": "Crie a classe RoboAspirador com atributo 'bateria' e métodos 'ligar', 'desligar', 'aspirar'.",
        "classe_alvo": "RoboAspirador",
        "atributos_req": {'bateria'},
        "metodos_req": {'ligar', 'desligar', 'aspirar'}
    },
    2: {
        "nome": "Desafio 2: Polimorfismo",
        "objetivo": "Crie SmartLamp (ligar, desligar) e SmartSpeaker (ligar, desligar, tocar_musica).",
        "classes_alvo": ["SmartLamp", "SmartSpeaker"],
    }
}
requisitos_desafio2 = {
    "SmartLamp": {"metodos_req": {'ligar', 'desligar'}},
    "SmartSpeaker": {"metodos_req": {'ligar', 'desligar', 'tocar_musica'}}
}
desafios_portas = {
    1: {
        "nome": "Desafio 1: Porta Automática",
        "objetivo": "Crie a classe Porta com métodos abrir, fechar e trancar.",
        "classe_alvo": "Porta",
        "atributos_req": set(),
        "metodos_req": {'abrir', 'fechar', 'trancar'}
    }
}

# --- INTERFACE (UI) ---
input_box_nome = pygame.Rect(50, 150, 280, 40)
paleta_atributos = {'bateria': pygame.Rect(50, 250, 120, 35)}
paleta_metodos = {
    'ligar': pygame.Rect(200, 250, 120, 35),
    'desligar': pygame.Rect(200, 300, 120, 35),
    'aspirar': pygame.Rect(200, 350, 120, 35),
    'tocar_musica': pygame.Rect(200, 400, 120, 35)
}
botao_validar_classe = pygame.Rect(50, 500, 280, 50)
botao_instanciar = pygame.Rect(850, 650, 150, 50)
botao_ativar_todos = pygame.Rect(1020, 650, 150, 50)

# --- EXPLICAÇÃO SOBRE HERANÇA ---
explicacao_eletro = [
    "Antes de criarmos o RoboAspirador, vamos entender o conceito de herança.",
    "Imagine uma classe mãe chamada 'Eletrodomestico'.",
    "Ela pode ligar, desligar e conectar na energia.",
    "RoboAspirador, SmartLamp e SmartSpeaker são eletrodomésticos,",
    "ou seja, herdam comportamentos básicos dessa classe mãe.",
    "",
    "Pressione qualquer tecla para continuar."
]

# --- SELEÇÃO DE DESENVOLVEDORES ---
devs_disponiveis = [
    {"nome": "Ana", "cor": (255, 100, 100), "nivel": "Júnior", "descricao": "Recebe dicas visuais e feedback detalhado."},
    {"nome": "Bruno", "cor": (100, 255, 100), "nivel": "Pleno", "descricao": "Recebe algumas dicas e feedback moderado."},
    {"nome": "Carla", "cor": (100, 100, 255), "nivel": "Sênior", "descricao": "Sem dicas, apenas o escopo do desafio."},
    {"nome": "Diego", "cor": (255, 200, 50), "nivel": "Sênior", "descricao": "Sem dicas, desafios extras aparecem."}
]
dev_selecionado = None
selecionando_dev = False
nivel_dev = None

# --- FONTES ---
FONTS_PATH = os.path.join(os.path.dirname(__file__), "assets", "fonts")
press_start_path = os.path.join(FONTS_PATH, "PressStart2P-Regular.ttf")

fonte_titulo = pygame.font.Font(press_start_path, 24)
fonte_texto = pygame.font.Font(press_start_path, 14)
fonte_feedback = pygame.font.Font(press_start_path, 10)

# --- FUNÇÕES DE TELA ---
def wrap_text(text, font, max_width):
    """Quebra o texto em múltiplas linhas para caber no retângulo."""
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines

def tela_selecao_dev():
    tela.fill((230, 230, 255))
    titulo = fonte_titulo.render("Selecione um(a) dev para o laboratório!", True, (30, 30, 30))
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 80))
    x = 120
    y = 250
    botoes = []
    for dev in devs_disponiveis:
        rect = pygame.Rect(x, y, 220, 140)
        pygame.draw.rect(tela, dev["cor"], rect, border_radius=15)
        pygame.draw.rect(tela, PRETO, rect, 2, border_radius=15)
        tela.blit(icon_dev, (rect.x + 10, rect.y + 20))
        nome = fonte_titulo.render(dev["nome"], True, PRETO)
        nivel = fonte_texto.render(f"Nível: {dev['nivel']}", True, PRETO)
        desc = fonte_feedback.render(dev["descricao"], True, PRETO)
        tela.blit(nome, (rect.x + 80, rect.y + 15))
        tela.blit(nivel, (rect.x + 80, rect.y + 50))
        tela.blit(desc, (rect.x + 10, rect.y + 90))
        botoes.append((rect, dev))
        x += 260
    pygame.display.flip()
    return botoes

def tela_atribuicao_projeto():
    tela.fill((227, 240, 255))  # Azul claro
    titulo = fonte_titulo.render("Atribua um(a) dev a um projeto!", True, (30, 30, 30))
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 60))

    card_w, card_h = 320, 170
    card_y = 250
    espacamento = 60
    total_w = len(projetos) * card_w + (len(projetos) - 1) * espacamento
    start_x = (LARGURA - total_w) // 2

    botoes = []
    for i, projeto in enumerate(projetos):
        card_x = start_x + i * (card_w + espacamento)
        rect = pygame.Rect(card_x, card_y, card_w, card_h)

        # Sombra
        sombra_rect = rect.move(6, 8)
        pygame.draw.rect(tela, (180, 200, 220), sombra_rect, border_radius=18)

        # Card
        pygame.draw.rect(tela, (240, 240, 255), rect, border_radius=18)
        pygame.draw.rect(tela, (80, 80, 120), rect, 3, border_radius=18)

        # Ícone centralizado no topo do card
        icon = projeto["icone"]
        icon_rect = icon.get_rect(center=(rect.centerx, rect.y + 45))
        tela.blit(icon, icon_rect)

        # Nome do projeto
        nome = fonte_titulo.render(projeto["nome"], True, (40, 40, 60))
        nome_rect = nome.get_rect(center=(rect.centerx, rect.y + 100))
        tela.blit(nome, nome_rect)

        # Descrição com quebra de linha real
        desc = projeto["descricao"]
        desc_lines = wrap_text(desc, fonte_feedback, card_w - 40)
        for j, line in enumerate(desc_lines):
            desc_render = fonte_feedback.render(line, True, (60, 60, 80))
            tela.blit(desc_render, (rect.x + 20, rect.y + 120 + j * 16))

        botoes.append((rect, projeto))
    pygame.display.flip()
    return botoes

# --- LOOP PRINCIPAL ---
while True:
    # Tela de atribuição de dev ao projeto
    if atribuindo_dev:
        botoes = tela_atribuicao_projeto()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for rect, projeto in botoes:
                    if rect.collidepoint(evento.pos):
                        projeto_selecionado = projeto
                        atribuindo_dev = False
                        selecionando_dev = True
        continue

    # Tela de seleção de dev
    if selecionando_dev:
        botoes = tela_selecao_dev()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for rect, dev in botoes:
                    if rect.collidepoint(evento.pos):
                        dev_selecionado = dev
                        nivel_dev = dev["nivel"]
                        selecionando_dev = False
                        intro = True
                        # Resetar estado do desafio
                        desafio_atual = 1
                        feedback_msg = "Bem-vindo ao Laboratório!"
                        classe_em_construcao = {'nome': '', 'atributos': set(), 'metodos': set()}
                        classes_definidas = {}
                        input_box_active = False
                        nome_classe_input = ""
                        objetos_instanciados = []
        continue

    # Tela de introdução
    if intro:
        tela.fill((245, 245, 245))
        y = 150
        titulo = fonte_titulo.render("Herança e Classe Mãe: Eletrodomestico", True, (0, 0, 0))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 80))
        for linha in explicacao_eletro:
            texto = fonte_texto.render(linha, True, (0, 0, 0))
            tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, y))
            y += 40
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                intro = False
        continue

    mouse_pos = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if input_box_nome.collidepoint(evento.pos):
                input_box_active = True
            else:
                input_box_active = False

        if evento.type == pygame.KEYDOWN:
            if input_box_active:
                if evento.key == pygame.K_BACKSPACE:
                    nome_classe_input = nome_classe_input[:-1]
                else:
                    if evento.unicode.isprintable():
                        nome_classe_input += evento.unicode
                classe_em_construcao['nome'] = nome_classe_input

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if not input_box_nome.collidepoint(mouse_pos):
                for nome, rect in paleta_atributos.items():
                    if rect.collidepoint(mouse_pos):
                        classe_em_construcao['atributos'].add(nome)
                for nome, rect in paleta_metodos.items():
                    if rect.collidepoint(mouse_pos):
                        classe_em_construcao['metodos'].add(nome)

                if botao_validar_classe.collidepoint(mouse_pos):
                    if projeto_selecionado["nome"] == "Eletrodomésticos Inteligentes":
                        if desafio_atual == 1:
                            req = desafios[1]
                            if (classe_em_construcao['nome'] == req['classe_alvo'] and
                                    classe_em_construcao['atributos'] == req['atributos_req'] and
                                    classe_em_construcao['metodos'] == req['metodos_req']):
                                feedback_msg = "RoboAspirador definido com sucesso! Agora instancie."
                                classes_definidas['RoboAspirador'] = True
                            else:
                                feedback_msg = "Requisitos não atendidos. Verifique a planta."
                        elif desafio_atual == 2:
                            nome_classe = classe_em_construcao['nome']
                            if nome_classe in requisitos_desafio2:
                                req = requisitos_desafio2[nome_classe]
                                if classe_em_construcao['metodos'] == req['metodos_req']:
                                    feedback_msg = f"{nome_classe} definido com sucesso!"
                                    classes_definidas[nome_classe] = True
                                else:
                                    feedback_msg = f"Métodos incorretos para {nome_classe}."
                            else:
                                feedback_msg = "Nome da classe não corresponde ao desafio."
                    elif projeto_selecionado["nome"] == "Sistema de Controle de Portas":
                        req = desafios_portas[1]
                        if (classe_em_construcao['nome'] == req['classe_alvo'] and
                                classe_em_construcao['metodos'] == req['metodos_req']):
                            feedback_msg = "Porta definida com sucesso! Agora instancie."
                            classes_definidas['Porta'] = True
                        else:
                            feedback_msg = "Requisitos não atendidos. Verifique a planta."

                if botao_instanciar.collidepoint(mouse_pos):
                    nome_para_instanciar = classe_em_construcao['nome']
                    if classes_definidas.get(nome_para_instanciar):
                        pos_x = random.randint(820, 1150)
                        pos_y = random.randint(100, 500)
                        if nome_para_instanciar == "RoboAspirador":
                            objetos_instanciados.append(RoboAspirador(pos_x, pos_y))
                            feedback_msg = "RoboAspirador instanciado!"
                        elif nome_para_instanciado == "SmartLamp":
                            objetos_instanciados.append(SmartLamp(pos_x, pos_y))
                            feedback_msg = "SmartLamp instanciada!"
                        elif nome_para_instanciado == "SmartSpeaker":
                            objetos_instanciados.append(SmartSpeaker(pos_x, pos_y))
                            feedback_msg = "SmartSpeaker instanciado!"
                        elif nome_para_instanciado == "Porta":
                            # Implemente a classe Porta se desejar
                            feedback_msg = "Porta instanciada!"
                    else:
                        feedback_msg = "Defina e valide a classe corretamente primeiro."

                if projeto_selecionado["nome"] == "Eletrodomésticos Inteligentes" and desafio_atual == 2 and botao_ativar_todos.collidepoint(mouse_pos):
                    count = 0
                    for obj in objetos_instanciados:
                        if hasattr(obj, 'ligar'):
                            obj.ligar()
                            count += 1
                    feedback_msg = f"Comando 'ligar' enviado para {count} objetos!"
                    # Verifica se todos os objetos estão ligados para finalizar a fase
                    if all(getattr(obj, 'ligado', False) for obj in objetos_instanciados):
                        feedback_msg = "Parabéns! Projeto concluído. Escolha um novo desafio."
                        projeto_selecionado = None
                        atribuindo_dev = True
                        selecionando_dev = False
                        intro = False
                        objetos_instanciados = []
                        pygame.time.wait(1500)
                        break

                for obj in objetos_instanciados:
                    if obj.rect.collidepoint(mouse_pos):
                        if hasattr(obj, 'ligado'):
                            if obj.ligado:
                                obj.desligar()
                            else:
                                obj.ligar()

                # Avança para próximo desafio/fase
                if projeto_selecionado["nome"] == "Eletrodomésticos Inteligentes" and desafio_atual == 1 and classes_definidas.get("RoboAspirador") and any(
                        isinstance(o, RoboAspirador) for o in objetos_instanciados):
                    desafio_atual = 2
                    feedback_msg = "Desafio 1 completo! Vamos para o próximo."
                    classe_em_construcao = {'nome': '', 'atributos': set(), 'metodos': set()}
                    nome_classe_input = ""
                    input_box_active = False

        if evento.type == pygame.KEYDOWN and intro:
            intro = False

    # --- RENDERIZAÇÃO ---
    tela.fill((245, 245, 245))

    # Painel do Desafio
    pygame.draw.rect(tela, CINZA, (20, 20, 750, 80))
    if projeto_selecionado:
        if projeto_selecionado["nome"] == "Eletrodomésticos Inteligentes":
            desafio_info = desafios[desafio_atual]
        else:
            desafio_info = desafios_portas[1]
        titulo_desafio = fonte_texto.render(desafio_info['nome'], True, PRETO)
        objetivo_desafio = fonte_feedback.render(desafio_info['objetivo'], True, (50, 50, 50))
        tela.blit(titulo_desafio, (30, 30))
        tela.blit(objetivo_desafio, (30, 60))

    # Dicas baseadas no nível do desenvolvedor
    if nivel_dev == "Júnior":
        dica = "Dica: Use os botões para adicionar atributos e métodos corretamente!"
        tela.blit(fonte_feedback.render(dica, True, (0, 120, 0)), (30, 85))
    elif nivel_dev == "Pleno":
        dica = "Dica: Atenção aos nomes dos métodos!"
        tela.blit(fonte_feedback.render(dica, True, (0, 120, 0)), (30, 85))

    # Mesa de Trabalho (Class Builder)
    pygame.draw.line(tela, PRETO, (400, 120), (400, 720), 2)
    titulo_builder = fonte_titulo.render("Mesa de Trabalho", True, PRETO)
    tela.blit(titulo_builder, (50, 110))
    cor_da_borda = AZUL_ATIVO if input_box_active else PRETO
    pygame.draw.rect(tela, BRANCO, input_box_nome)
    pygame.draw.rect(tela, cor_da_borda, input_box_nome, 2)
    texto_input = fonte_texto.render(nome_classe_input, True, PRETO)
    tela.blit(texto_input, (input_box_nome.x + 10, input_box_nome.y + 5))

    tela.blit(fonte_texto.render("Atributos:", True, PRETO), (50, 210))
    for nome, rect in paleta_atributos.items():
        selecionado = nome in classe_em_construcao['atributos']
        cor = VERDE if selecionado else BRANCO
        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, PRETO, rect, 1)
        tela.blit(fonte_feedback.render(nome, True, PRETO), (rect.x + 10, rect.y + 8))

    tela.blit(fonte_texto.render("Métodos:", True, PRETO), (200, 210))
    for nome, rect in paleta_metodos.items():
        selecionado = nome in classe_em_construcao['metodos']
        cor = VERDE if selecionado else BRANCO
        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, PRETO, rect, 1)
        tela.blit(fonte_feedback.render(f"{nome}()", True, PRETO), (rect.x + 10, rect.y + 8))

    pygame.draw.rect(tela, (0, 150, 0), botao_validar_classe)
    tela.blit(fonte_texto.render("Validar Classe", True, BRANCO),
              (botao_validar_classe.x + 70, botao_validar_classe.y + 10))

    # Área de Testes
    pygame.draw.line(tela, PRETO, (800, 20), (800, 720), 2)
    titulo_sandbox = fonte_titulo.render("Área de Testes", True, PRETO)
    tela.blit(titulo_sandbox, (900, 40))
    for obj in objetos_instanciados:
        obj.desenhar(tela)

    pygame.draw.rect(tela, (0, 100, 150), botao_instanciar)
    tela.blit(fonte_texto.render("Instanciar", True, BRANCO), (botao_instanciar.x + 30, botao_instanciar.y + 10))
    if projeto_selecionado and projeto_selecionado["nome"] == "Eletrodomésticos Inteligentes" and desafio_atual == 2:
        pygame.draw.rect(tela, (150, 0, 150), botao_ativar_todos)
        tela.blit(fonte_texto.render("ATIVAR TUDO", True, BRANCO),
                  (botao_ativar_todos.x + 15, botao_ativar_todos.y + 10))

    # Painel de Feedback
    pygame.draw.rect(tela, PRETO, (0, 720, LARGURA, 30))
    feedback_render = fonte_feedback.render(feedback_msg, True, BRANCO)
    tela.blit(feedback_render, (10, 725))

    # Renderização da explicação
    if intro:
        y_offset = 0
        for linha in explicacao_eletro:
            texto_explicacao = fonte_texto.render(linha, True, PRETO)
            tela.blit(texto_explicacao, (50, 100 + y_offset))
            y_offset += 30

    if dev_selecionado:
        tela.blit(icon_dev, (750, 5))
        dev_nome = fonte_feedback.render(f"Dev: {dev_selecionado['nome']} ({dev_selecionado['nivel']})", True, dev_selecionado["cor"])
        tela.blit(dev_nome, (820, 10))
        dev_desc = fonte_feedback.render(dev_selecionado["descricao"], True, dev_selecionado["cor"])
        tela.blit(dev_desc, (820, 30))
    if projeto_selecionado:
        tela.blit(projeto_selecionado["icone"], (700, 5))
        nome_proj = fonte_feedback.render(f"Projeto: {projeto_selecionado['nome']}", True, PRETO)
        tela.blit(nome_proj, (770, 10))

    pygame.display.flip()

    # Dificuldade extra para dev Sênior
    if nivel_dev == "Sênior":
        paleta_atributos['corpo'] = pygame.Rect(50, 300, 120, 35)
        paleta_metodos['dançar'] = pygame.Rect(200, 450, 120, 35)