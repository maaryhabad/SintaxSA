# main_jogo_final_corrigido.py
import pygame
import sys
import random


# --- CLASSES (com ícones e tamanhos corrigidos) ---
class Desenvolvedor:
    def __init__(self, nome, pos_x, pos_y):
        self.nome = nome
        self.image_original = pygame.image.load('assets/dev_icon.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_original, (60, 60))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.color = (120, 120, 120)
        self.hovered = False

    def draw(self, screen):
        if self.hovered:
            glow_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (200, 200, 255, 60), (40, 40), 40)
            screen.blit(glow_surface, (self.rect.centerx - 40, self.rect.centery - 40))
        pygame.draw.circle(screen, self.color, self.rect.center, 35)
        screen.blit(self.image, self.rect)


class DevIoT(Desenvolvedor):
    def __init__(self, nome, pos_x, pos_y):
        super().__init__(nome, pos_x, pos_y)
        self.color = (50, 180, 180)


class RoboAspirador:
    def __init__(self, pos_x, pos_y):
        self.rect = pygame.Rect(pos_x - 40, pos_y - 40, 80, 80)
        self.bateria = 100
        self.ligado = False
        self.icon_original = pygame.image.load('assets/robot_vacuum_icon.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon_original, (70, 70))
        self.icon_rect = self.icon.get_rect(center=self.rect.center)

    def ligar(self): self.ligado = True

    def desligar(self): self.ligado = False

    def aspirar(self):
        if self.ligado and self.bateria > 0: self.bateria = max(0, self.bateria - 10)

    def draw(self, screen, font):
        screen.blit(self.icon, self.icon_rect)
        light_color = (70, 220, 120) if self.ligado else (220, 70, 70)
        pygame.draw.circle(screen, light_color, (self.icon_rect.right - 10, self.icon_rect.top + 10), 7)
        battery_rect_bg = pygame.Rect(self.rect.left, self.rect.bottom + 5, self.rect.width, 10)
        battery_rect_fg = pygame.Rect(self.rect.left, self.rect.bottom + 5, self.rect.width * (self.bateria / 100), 10)
        pygame.draw.rect(screen, (40, 40, 40), battery_rect_bg, border_radius=4)
        pygame.draw.rect(screen, (0, 180, 0), battery_rect_fg, border_radius=4)


class SmartLamp:
    def __init__(self, pos_x, pos_y):
        self.rect = pygame.Rect(pos_x - 40, pos_y - 40, 80, 80)
        self.ligado = False
        self.icon_original = pygame.image.load('assets/smart_lamp_icon.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon_original, (70, 70))
        self.icon_rect = self.icon.get_rect(center=self.rect.center)

    def ligar(self): self.ligado = True

    def desligar(self): self.ligado = False

    def draw(self, screen, font):
        screen.blit(self.icon, self.icon_rect)
        if self.ligado:
            glow_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 255, 180, 80), (50, 50), 50)
            screen.blit(glow_surface, (self.icon_rect.centerx - 50, self.icon_rect.centery - 50))


class SmartSpeaker:
    def __init__(self, pos_x, pos_y):
        self.rect = pygame.Rect(pos_x - 40, pos_y - 40, 80, 80)
        self.ligado = False
        self.tocando_musica = False
        self.icon_original = pygame.image.load('assets/smart_speaker_icon.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon_original, (70, 70))
        self.icon_rect = self.icon.get_rect(center=self.rect.center)

    def ligar(self):
        self.ligado = True

    def desligar(self):
        self.ligado = False; self.tocando_musica = False

    def tocar_musica(self):
        if self.ligado: self.tocando_musica = True

    def draw(self, screen, font):
        screen.blit(self.icon, self.icon_rect)
        if self.tocando_musica:
            wave_color = (200, 200, 255)
            pygame.draw.line(screen, wave_color, (self.icon_rect.centerx - 20, self.icon_rect.centery - 20),
                             (self.icon_rect.centerx + 20, self.icon_rect.centery - 20), 2)
            pygame.draw.line(screen, wave_color, (self.icon_rect.centerx - 20, self.icon_rect.centery + 20),
                             (self.icon_rect.centerx + 20, self.icon_rect.centery + 20), 2)


# --- INICIALIZAÇÃO E CONFIGURAÇÕES GERAIS ---
pygame.init()
LARGURA, ALTURA = 1280, 800
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("DevLife: Terminal Moderno")
# --- PALETA DE CORES E FONTES ---
BG_CARBON = (20, 22, 25);
PANEL_DARK = (30, 33, 40);
TEXT_LIGHT = (210, 215, 220);
TEXT_DARK = (20, 22, 25)
BORDER_LIGHT = (50, 55, 65);
ACCENT_BLUE = (80, 150, 255);
ACCENT_BLUE_HOVER = (110, 180, 255)
ACCENT_GREEN = (70, 200, 120);
ACCENT_GREEN_HOVER = (100, 230, 150);
ACCENT_IOT = (50, 180, 180)
ACCENT_IOT_HOVER = (80, 210, 210);
INPUT_ACTIVE_AMBER = (255, 180, 0)
try:
    font_ui = pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 22)
    font_ui_bold = pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 26)
    font_code = pygame.font.Font("assets/fonts/FiraCode-Regular.ttf", 20)
    font_code_small = pygame.font.Font("assets/fonts/FiraCode-Regular.ttf", 16)
except pygame.error:
    print("AVISO: Ficheiros de fonte não encontrados. Usando fontes padrão.");
    font_ui = pygame.font.SysFont('Arial', 22)
    font_ui_bold = pygame.font.SysFont('Arial', 26, bold=True);
    font_code = pygame.font.SysFont('Courier', 20);
    font_code_small = pygame.font.SysFont('Courier', 16)

# --- CONTROLE DE ESTADO ---
fase_atual = 'HERANCA';
desafio_lab_actual = 1;
feedback_msg = "Bem-vindo ao DevLife! Novo projeto recebido."
dev_iot_desbloqueado = False;
devs_contratados = [Desenvolvedor("Dev Genérico", 250, 480)]
tarefa_smarthome = {'rect': pygame.Rect(650, 200, 550, 300), 'completa': False}
button_especializar_iot = pygame.Rect(50, 200, 400, 60);
button_contratar_iot = pygame.Rect(50, 280, 400, 60);
dragged_dev = None
class_in_construction = {'name': '', 'attributes': set(), 'methods': set()};
classes_defined = {}
instantiated_objects = [];
input_box_active = False;
class_input_name = ""
lab_challenges = {
    1: {"name": "Encapsulamento", "objective": "Construa o RoboAspirador (bateria; ligar, desligar, aspirar).",
        "req": {'class': "RoboAspirador", 'atrs': {'bateria'}, 'mets': {'ligar', 'desligar', 'aspirar'}}},
    2: {"name": "Polimorfismo", "objective": "Construa a SmartLamp e o SmartSpeaker e ative todos com um comando.",
        "req_lamp": {'mets': {'ligar', 'desligar'}}, "req_speaker": {'mets': {'ligar', 'desligar', 'tocar_musica'}}}}
input_box_name = pygame.Rect(50, 180, 350, 45)
palette_attributes = {'bateria': pygame.Rect(50, 280, 165, 40)}
palette_methods = {'ligar': pygame.Rect(235, 280, 165, 40), 'desligar': pygame.Rect(235, 330, 165, 40),
                   'aspirar': pygame.Rect(235, 380, 165, 40), 'tocar_musica': pygame.Rect(235, 430, 165, 40)}
button_validate_class = pygame.Rect(50, 550, 350, 60);
button_instantiate = pygame.Rect(880, 680, 180, 60);
button_activate_all = pygame.Rect(1080, 680, 180, 60)
# --- ALTERAÇÃO: Novo botão para transição de desafio ---
button_next_challenge = pygame.Rect(50, 630, 350, 60)
desafio1_completo = False


# --- FUNÇÕES DE DESENHO ---
def draw_panel(screen, rect, color, border_color, border_radius=15):
    pygame.draw.rect(screen, color, rect, border_radius=border_radius);
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=border_radius)


def draw_text(screen, text, font, color, center_pos):
    text_surf = font.render(text, True, color);
    text_rect = text_surf.get_rect(center=center_pos);
    screen.blit(text_surf, text_rect)


def draw_button_styled(screen, rect, text, font, base_color, hover_color, text_color, is_enabled=True):
    current_color = base_color
    if rect.collidepoint(pygame.mouse.get_pos()) and is_enabled:
        current_color = hover_color;
        glow_surface = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*current_color, 80), glow_surface.get_rect(), border_radius=15);
        screen.blit(glow_surface, (rect.x - 5, rect.y - 5))
    if not is_enabled:
        current_color = (40, 45, 55);
        text_color = (100, 105, 115)
    pygame.draw.rect(screen, current_color, rect, border_radius=10);
    draw_text(screen, text, font, text_color, rect.center)


# --- LOOP PRINCIPAL ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if fase_atual == 'HERANCA':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_especializar_iot.collidepoint(mouse_pos) and not dev_iot_desbloqueado:
                    dev_iot_desbloqueado = True;
                    feedback_msg = "Herança aplicada! 'DevIoT' especialização disponível."
                elif button_contratar_iot.collidepoint(mouse_pos) and dev_iot_desbloqueado:
                    devs_contratados.append(DevIoT("Dev de IoT", 350, 480));
                    feedback_msg = "DevIoT contratado! Arraste-o para o projeto."
                for dev in devs_contratados:
                    if dev.rect.collidepoint(mouse_pos):
                        dragged_dev = dev;
                        offset_x = dev.rect.x - mouse_pos[0];
                        offset_y = dev.rect.y - mouse_pos[1];
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragged_dev:
                    if isinstance(dragged_dev, DevIoT) and tarefa_smarthome['rect'].collidepoint(mouse_pos):
                        tarefa_smarthome['completa'] = True;
                        feedback_msg = "Especialista alocado! Entrando no laboratório...";
                        pygame.time.delay(1000);
                        fase_atual = 'LABORATORIO'
                    dragged_dev = None
            elif event.type == pygame.MOUSEMOTION:
                if dragged_dev:
                    dragged_dev.rect.x = mouse_pos[0] + offset_x;
                    dragged_dev.rect.y = mouse_pos[1] + offset_y
                for dev in devs_contratados: dev.hovered = dev.rect.collidepoint(mouse_pos)

        elif fase_atual == 'LABORATORIO':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_name.collidepoint(event.pos):
                    input_box_active = True
                else:
                    input_box_active = False

                # --- ALTERAÇÃO: Lógica de transição movida para o novo botão ---
                if desafio1_completo and button_next_challenge.collidepoint(mouse_pos):
                    desafio_lab_actual = 2
                    feedback_msg = "Próximo desafio: Polimorfismo."
                    # Limpa o estado para o próximo desafio
                    class_in_construction = {'name': '', 'attributes': set(), 'methods': set()}
                    class_input_name = ""
                    input_box_active = False
                    instantiated_objects = []
                    classes_defined = {}
                    desafio1_completo = False  # Reseta o estado do botão

                for name, rect in palette_attributes.items():
                    if rect.collidepoint(mouse_pos): class_in_construction['attributes'].add(name)
                for name, rect in palette_methods.items():
                    if rect.collidepoint(mouse_pos): class_in_construction['methods'].add(name)

                if button_validate_class.collidepoint(mouse_pos):
                    # ... (lógica de validação inalterada)
                    current_challenge = lab_challenges[desafio_lab_actual]
                    if desafio_lab_actual == 1:
                        req = current_challenge['req']
                        if (class_in_construction['name'] == req['class'] and class_in_construction['attributes'] ==
                                req['atrs'] and class_in_construction['methods'] == req['mets']):
                            feedback_msg = "RoboAspirador definido! Agora instancie-o.";
                            classes_defined['RoboAspirador'] = True
                        else:
                            feedback_msg = "Requisitos do RoboAspirador não atendidos."
                    elif desafio_lab_actual == 2:
                        class_name = class_in_construction['name']
                        if class_name == 'SmartLamp' and class_in_construction['methods'] == \
                                current_challenge['req_lamp']['mets']:
                            feedback_msg = "SmartLamp definida!";
                            classes_defined['SmartLamp'] = True
                        elif class_name == 'SmartSpeaker' and class_in_construction['methods'] == \
                                current_challenge['req_speaker']['mets']:
                            feedback_msg = "SmartSpeaker definido!";
                            classes_defined['SmartSpeaker'] = True
                        else:
                            feedback_msg = "Requisitos não atendidos para este dispositivo."

                if button_instantiate.collidepoint(mouse_pos):
                    name_to_instantiate = class_in_construction['name']
                    if classes_defined.get(name_to_instantiate):
                        pos_x, pos_y = random.randint(500, LARGURA - 100), random.randint(150, ALTURA - 150)
                        if name_to_instantiate == "RoboAspirador":
                            instantiated_objects.append(RoboAspirador(pos_x, pos_y))
                            # --- ALTERAÇÃO: Lógica de transição foi removida daqui ---
                            # Apenas marcamos o desafio como completo
                            desafio1_completo = True
                            feedback_msg = "RoboAspirador instanciado com sucesso!"
                        elif name_to_instantiate == "SmartLamp":
                            instantiated_objects.append(SmartLamp(pos_x, pos_y))
                        elif name_to_instantiate == "SmartSpeaker":
                            instantiated_objects.append(SmartSpeaker(pos_x, pos_y))
                    else:
                        feedback_msg = "Defina e valide a classe corretamente primeiro."

                if desafio_lab_actual == 2 and button_activate_all.collidepoint(mouse_pos):
                    # ... (lógica do botão ATIVAR TUDO inalterada)
                    if classes_defined.get('SmartLamp') and classes_defined.get('SmartSpeaker') and any(
                            isinstance(o, SmartLamp) for o in instantiated_objects) and any(
                            isinstance(o, SmartSpeaker) for o in instantiated_objects):
                        for obj in instantiated_objects:
                            if hasattr(obj, 'ligar'): obj.ligar()
                        feedback_msg = "Comando 'ligar' enviado a todos! Polimorfismo em ação."
                    else:
                        feedback_msg = "Instancie SmartLamp e SmartSpeaker primeiro!"

                for obj in instantiated_objects:
                    if obj.rect.collidepoint(mouse_pos):
                        if isinstance(obj, RoboAspirador):
                            if obj.ligado:
                                obj.aspirar()
                            else:
                                obj.ligar()
                        elif hasattr(obj, 'ligado'):
                            if obj.ligado:
                                obj.desligar()
                            else:
                                obj.ligar()
            elif event.type == pygame.KEYDOWN:
                if input_box_active:
                    if event.key == pygame.K_BACKSPACE:
                        class_input_name = class_input_name[:-1]
                    else:
                        if event.unicode.isprintable(): class_input_name += event.unicode
                    class_in_construction['name'] = class_input_name

    # --- RENDERIZAÇÃO ---
    screen.fill(BG_CARBON)
    if fase_atual == 'HERANCA':
        # ... (renderização da fase de herança inalterada)
        draw_panel(screen, (20, 20, 450, ALTURA - 80), PANEL_DARK, BORDER_LIGHT)
        draw_text(screen, "Fase 1: Herança", font_ui_bold, TEXT_LIGHT, (245, 60))
        draw_text(screen, "O projeto SmartHome precisa de um especialista.", font_ui, TEXT_LIGHT, (245, 100))
        draw_button_styled(screen, button_especializar_iot, "Definir Subclasse: DevIoT", font_code, ACCENT_BLUE,
                           ACCENT_BLUE_HOVER, TEXT_LIGHT, is_enabled=not dev_iot_desbloqueado)
        if dev_iot_desbloqueado: draw_button_styled(screen, button_contratar_iot, "Contratar DevIoT", font_ui_bold,
                                                    ACCENT_IOT, ACCENT_IOT_HOVER, TEXT_LIGHT)
        draw_panel(screen, (50, 360, 400, ALTURA - 460), BG_CARBON, BORDER_LIGHT)
        draw_text(screen, "Equipa:", font_ui_bold, TEXT_LIGHT, (100, 390))
        for dev in devs_contratados: dev.draw(screen)
        draw_panel(screen, tarefa_smarthome['rect'], PANEL_DARK, BORDER_LIGHT)
        draw_text(screen, "Projeto: Sistema SmartHome", font_ui_bold, TEXT_LIGHT, tarefa_smarthome['rect'].center)
        draw_text(screen, "Arraste o DevIoT aqui para começar!", font_ui, TEXT_LIGHT,
                  (tarefa_smarthome['rect'].centerx, tarefa_smarthome['rect'].centery + 40))
    elif fase_atual == 'LABORATORIO':
        # ... (renderização da fase de laboratório, com uma adição)
        challenge_info = lab_challenges[desafio_lab_actual]
        draw_panel(screen, (20, 20, LARGURA - 40, 80), PANEL_DARK, BORDER_LIGHT)
        draw_text(screen, f"Fase 2: Laboratório - {challenge_info['name']}", font_ui_bold, TEXT_LIGHT,
                  ((LARGURA - 40) / 2, 45))
        draw_text(screen, challenge_info['objective'], font_ui, TEXT_LIGHT, ((LARGURA - 40) / 2, 75))
        draw_panel(screen, (20, 120, 420, ALTURA - 180), PANEL_DARK, BORDER_LIGHT)
        draw_text(screen, "Mesa de Trabalho", font_ui_bold, TEXT_LIGHT, (230, 150))
        border_color = INPUT_ACTIVE_AMBER if input_box_active else BORDER_LIGHT
        draw_panel(screen, input_box_name, BG_CARBON, border_color)
        text_surf = font_code.render(class_input_name, True, TEXT_LIGHT)
        screen.blit(text_surf, (input_box_name.x + 10, input_box_name.y + 10))
        draw_text(screen, "Nome da Classe:", font_ui, TEXT_LIGHT, (120, 240))
        draw_text(screen, "Atributos:", font_ui, TEXT_LIGHT, (130, 300))
        for name, rect in palette_attributes.items():
            is_selected = name in class_in_construction['attributes'];
            draw_button_styled(screen, rect, name, font_code_small, ACCENT_GREEN if is_selected else BG_CARBON,
                               ACCENT_GREEN_HOVER if is_selected else BORDER_LIGHT, TEXT_LIGHT)
        draw_text(screen, "Métodos:", font_ui, TEXT_LIGHT, (315, 300))
        for name, rect in palette_methods.items():
            is_selected = name in class_in_construction['methods'];
            draw_button_styled(screen, rect, f"{name}()", font_code_small, ACCENT_GREEN if is_selected else BG_CARBON,
                               ACCENT_GREEN_HOVER if is_selected else BORDER_LIGHT, TEXT_LIGHT)

        # --- ALTERAÇÃO: Botão de Próximo Desafio só aparece quando o desafio 1 está completo ---
        if desafio1_completo:
            draw_button_styled(screen, button_next_challenge, "Próximo Desafio ->", font_ui_bold, ACCENT_BLUE,
                               ACCENT_BLUE_HOVER, TEXT_LIGHT)
        else:
            draw_button_styled(screen, button_validate_class, "Validar Planta da Classe", font_ui_bold, ACCENT_GREEN,
                               ACCENT_GREEN_HOVER, TEXT_DARK)

        draw_panel(screen, (460, 120, LARGURA - 480, ALTURA - 180), BG_CARBON, BORDER_LIGHT)
        draw_text(screen, "Área de Testes (Sandbox)", font_ui_bold, TEXT_LIGHT, (460 + (LARGURA - 480) / 2, 150))
        for obj in instantiated_objects: obj.draw(screen, font_code_small)
        draw_button_styled(screen, button_instantiate, "Instanciar", font_ui_bold, ACCENT_BLUE, ACCENT_BLUE_HOVER,
                           TEXT_LIGHT, is_enabled=(class_in_construction['name'] in classes_defined))
        if desafio_lab_actual == 2:
            draw_button_styled(screen, button_activate_all, "ATIVAR TUDO", font_ui_bold, (200, 80, 80), (230, 110, 110),
                               TEXT_LIGHT,
                               is_enabled=(classes_defined.get('SmartLamp') and classes_defined.get('SmartSpeaker')))

    draw_text(screen, feedback_msg, font_ui, TEXT_LIGHT, (LARGURA / 2, ALTURA - 30))
    pygame.display.flip()

pygame.quit()