# main_fase_laboratorio.py
import pygame
import sys
import random


# --- CLASSES DOS OBJETOS QUE O JOGADOR PODE CONSTRUIR ---
# (Nenhuma alteração nesta seção, continua a mesma)
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
        cor_status = (0, 255, 0) if self.ligado else (200, 0, 0)
        pygame.draw.rect(tela, self.cor, self.rect, border_radius=25)
        pygame.draw.circle(tela, cor_status, (self.rect.centerx, self.rect.centery - 15), 5)
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
        cor_desenho = self.cor if self.ligado else (50, 50, 0)
        pygame.draw.circle(tela, cor_desenho, self.rect.center, 25)


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
        pygame.draw.rect(tela, self.cor, self.rect, border_radius=10)
        if self.tocando_musica:
            y_offset = random.randint(-5, 5)
            pygame.draw.line(tela, (255, 255, 255), (self.rect.centerx - 10, self.rect.centery + y_offset),
                             (self.rect.centerx + 10, self.rect.centery - y_offset), 2)


# --- INICIALIZAÇÃO DO PYGAME ---
pygame.init()
LARGURA, ALTURA = 1200, 750
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fase 2: O Laboratório de POO (Corrigido)")

# Fontes e Cores
fonte_titulo = pygame.font.SysFont('Arial', 32)
fonte_texto = pygame.font.SysFont('Arial', 22)
fonte_feedback = pygame.font.SysFont('Arial', 18)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
VERDE = (0, 200, 100)
AZUL_ATIVO = (0, 150, 255)  # <--- ALTERAÇÃO: Nova cor para feedback visual

# --- CONTROLE DE ESTADO DO JOGO ---
desafio_atual = 1
feedback_msg = "Bem-vindo ao Laboratório!"

# Estado do Class Builder
classe_em_construcao = {'nome': '', 'atributos': set(), 'metodos': set()}
classes_definidas = {}
input_box_active = False  # <--- ALTERAÇÃO: Nova variável de estado
nome_classe_input = ""

# Estado da Área de Testes (Sandbox)
objetos_instanciados = []

# --- DEFINIÇÃO DOS DESAFIOS ---
# (Nenhuma alteração nesta seção)
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

# --- LOOP PRINCIPAL ---
while True:
    mouse_pos = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # --- LÓGICA DE INPUT CORRIGIDA ---
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # <--- ALTERAÇÃO: Ativa ou desativa a caixa de texto com o clique
            if input_box_nome.collidepoint(evento.pos):
                input_box_active = True
            else:
                input_box_active = False
            # (O restante do código de MOUSEBUTTONDOWN continua abaixo)

        if evento.type == pygame.KEYDOWN:
            # <--- ALTERAÇÃO: Só processa a digitação se a caixa estiver ativa
            if input_box_active:
                if evento.key == pygame.K_BACKSPACE:
                    nome_classe_input = nome_classe_input[:-1]
                else:
                    # Impede que caracteres de controle sejam adicionados
                    if evento.unicode.isprintable():
                        nome_classe_input += evento.unicode
                classe_em_construcao['nome'] = nome_classe_input

        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Lógica dos botões (continua a mesma)
            if not input_box_nome.collidepoint(mouse_pos):  # Para não clicar nos botões "por baixo" da caixa
                for nome, rect in paleta_atributos.items():
                    if rect.collidepoint(mouse_pos):
                        classe_em_construcao['atributos'].add(nome)
                for nome, rect in paleta_metodos.items():
                    if rect.collidepoint(mouse_pos):
                        classe_em_construcao['metodos'].add(nome)

                if botao_validar_classe.collidepoint(mouse_pos):
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

                if botao_instanciar.collidepoint(mouse_pos):
                    nome_para_instanciar = classe_em_construcao['nome']
                    if classes_definidas.get(nome_para_instanciar):
                        pos_x = random.randint(820, 1150)
                        pos_y = random.randint(100, 500)
                        if nome_para_instanciar == "RoboAspirador":
                            objetos_instanciados.append(RoboAspirador(pos_x, pos_y))
                            feedback_msg = "RoboAspirador instanciado!"
                        elif nome_para_instanciar == "SmartLamp":
                            objetos_instanciados.append(SmartLamp(pos_x, pos_y))
                            feedback_msg = "SmartLamp instanciada!"
                        elif nome_para_instanciar == "SmartSpeaker":
                            objetos_instanciados.append(SmartSpeaker(pos_x, pos_y))
                            feedback_msg = "SmartSpeaker instanciado!"
                    else:
                        feedback_msg = "Defina e valide a classe corretamente primeiro."

                if desafio_atual == 2 and botao_ativar_todos.collidepoint(mouse_pos):
                    count = 0
                    for obj in objetos_instanciados:
                        if hasattr(obj, 'ligar'):
                            obj.ligar()
                            count += 1
                    feedback_msg = f"Comando 'ligar' enviado para {count} objetos!"

                for obj in objetos_instanciados:
                    if obj.rect.collidepoint(mouse_pos):
                        if hasattr(obj, 'ligado'):
                            if obj.ligado:
                                obj.desligar()
                            else:
                                obj.ligar()

                if desafio_atual == 1 and classes_definidas.get("RoboAspirador") and any(
                        isinstance(o, RoboAspirador) for o in objetos_instanciados):
                    desafio_atual = 2
                    feedback_msg = "Desafio 1 completo! Vamos para o próximo."
                    classe_em_construcao = {'nome': '', 'atributos': set(), 'metodos': set()}
                    nome_classe_input = ""
                    input_box_active = False  # Desativa a caixa ao mudar de fase

    # --- RENDERIZAÇÃO ---
    tela.fill((245, 245, 245))

    # Desenhar Painel do Desafio (sem alterações)
    pygame.draw.rect(tela, CINZA, (20, 20, 750, 80))
    desafio_info = desafios[desafio_atual]
    titulo_desafio = fonte_texto.render(desafio_info['nome'], True, PRETO)
    objetivo_desafio = fonte_feedback.render(desafio_info['objetivo'], True, (50, 50, 50))
    tela.blit(titulo_desafio, (30, 30))
    tela.blit(objetivo_desafio, (30, 60))

    # Desenhar Mesa de Trabalho (Class Builder)
    pygame.draw.line(tela, PRETO, (400, 120), (400, 720), 2)
    titulo_builder = fonte_titulo.render("Mesa de Trabalho", True, PRETO)
    tela.blit(titulo_builder, (50, 110))

    # <--- ALTERAÇÃO: A cor da borda muda se a caixa estiver ativa
    cor_da_borda = AZUL_ATIVO if input_box_active else PRETO
    pygame.draw.rect(tela, BRANCO, input_box_nome)
    pygame.draw.rect(tela, cor_da_borda, input_box_nome, 2)
    texto_input = fonte_texto.render(nome_classe_input, True, PRETO)
    tela.blit(texto_input, (input_box_nome.x + 10, input_box_nome.y + 5))

    # O resto da renderização continua igual...
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

    # Desenhar Área de Testes
    pygame.draw.line(tela, PRETO, (800, 20), (800, 720), 2)
    titulo_sandbox = fonte_titulo.render("Área de Testes", True, PRETO)
    tela.blit(titulo_sandbox, (900, 40))
    for obj in objetos_instanciados:
        obj.desenhar(tela)

    pygame.draw.rect(tela, (0, 100, 150), botao_instanciar)
    tela.blit(fonte_texto.render("Instanciar", True, BRANCO), (botao_instanciar.x + 30, botao_instanciar.y + 10))
    if desafio_atual == 2:
        pygame.draw.rect(tela, (150, 0, 150), botao_ativar_todos)
        tela.blit(fonte_texto.render("ATIVAR TUDO", True, BRANCO),
                  (botao_ativar_todos.x + 15, botao_ativar_todos.y + 10))

    # Painel de Feedback
    pygame.draw.rect(tela, PRETO, (0, 720, LARGURA, 30))
    feedback_render = fonte_feedback.render(feedback_msg, True, BRANCO)
    tela.blit(feedback_render, (10, 725))

    pygame.display.flip()