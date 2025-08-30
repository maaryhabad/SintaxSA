# main_fase_laboratorio.py
import pygame
import sys
import random
import os
from const import ALTURA, AZUL_ATIVO, BRANCO, CINZA, LARGURA, PRETO, VERDE, ASSETS_PATH
from model.Project import Project
from model.Smart_Lamp import Smart_Lamp
from model.Smart_Speaker import Smart_Speaker
from model.Robot_Vacuum import Robot_Vacuum

# --- INICIALIZAÇÃO DO PYGAME ---
pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SintaxSA")

# --- CARREGAMENTO DE ASSETS ---
icon_dev = pygame.image.load(os.path.join(ASSETS_PATH, "dev_icon.png"))
icon_speaker = Smart_Speaker.icon
icon_lamp = Smart_Lamp.icon
icon_robo = Robot_Vacuum.icon
icon_dev = pygame.transform.smoothscale(icon_dev, (60, 60))
icon_robo = pygame.transform.smoothscale(icon_robo, (50, 50))
icon_lamp = pygame.transform.smoothscale(icon_lamp, (50, 50))
icon_speaker = pygame.transform.smoothscale(icon_speaker, (50, 50))

# --- PROJETOS/FASES ---
projetos = Project.load_projects()
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
        "objetivo": "Crie a classe robot_vacuum com atributo 'bateria' e métodos 'ligar', 'desligar', 'aspirar'.",
        "classe_alvo": "Robot_Vacuum",
        "atributos_req": {'bateria'},
        "metodos_req": {'ligar', 'desligar', 'aspirar'}
    },
    2: {
        "nome": "Desafio 2: Polimorfismo",
        "objetivo": "Crie SmartLamp (ligar, desligar) e Smart_Speaker (ligar, desligar, tocar_musica).",
        "classes_alvo": ["Smart_Lamp", "Smart_Speaker"],
    }
}
requisitos_desafio2 = {
    "SmartLamp": {"metodos_req": {'ligar', 'desligar'}},
    "Smart_Speaker": {"metodos_req": {'ligar', 'desligar', 'tocar_musica'}}
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
    "Antes de criarmos o robot_vacuum, vamos entender o conceito de herança.",
    "Imagine uma classe mãe chamada 'Eletrodomestico'.",
    "Ela pode ligar, desligar e conectar na energia.",
    "robot_vacuum, SmartLamp e Smart_Speaker são eletrodomésticos,",
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
        icon = projeto.icon
        icon_rect = icon.get_rect(center=(rect.centerx, rect.y + 45))
        tela.blit(icon, icon_rect)

        # Nome do projeto
        nome = fonte_titulo.render(projeto.nome, True, (40, 40, 60))
        nome_rect = nome.get_rect(center=(rect.centerx, rect.y + 100))
        tela.blit(nome, nome_rect)

        # Descrição com quebra de linha real
        desc = projeto.description
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
                                feedback_msg = "robot_vacuum definido com sucesso! Agora instancie."
                                classes_definidas['robot_vacuum'] = True
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
                        if nome_para_instanciar == "robot_vacuum":
                            objetos_instanciados.append(Robot_Vacuum(False, (100, 100, 100), pos_x, pos_y, 100))
                            feedback_msg = "robot_vacuum instanciado!"
                        elif nome_para_instanciar == "smart_lamp":
                            objetos_instanciados.append(Smart_Lamp(pos_x, pos_y))
                            feedback_msg = "SmartLamp instanciada!"
                        elif nome_para_instanciar == "Smart_Speaker":
                            objetos_instanciados.append(Smart_Speaker(pos_x, pos_y))
                            feedback_msg = "Smart_Speaker instanciado!"
                        elif nome_para_instanciar == "Porta":
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
                if projeto_selecionado["nome"] == "Eletrodomésticos Inteligentes" and desafio_atual == 1 and classes_definidas.get("robot_vacuum") and any(
                        isinstance(o, robot_vacuum) for o in objetos_instanciados):
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
        obj.draw(tela)

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