"""
Gerenciador de Telas de Memes, Popups e Telas Finais (Vitória e Derrota)
"""
import pygame
import random
import os
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_CARD_BG, COLOR_PRIMARY,
    COLOR_SUCCESS, COLOR_DANGER, COLOR_TEXT_LIGHT, COLOR_TEXT_MUTED,
    IMG_DEFEAT_WHEEZY, IMG_VICTORY_KING, IMG_MEME_LOST_1, IMG_MEME_LOST_2,
    LOST_CHEESE_QUOTES, TARGET_SCORE
)

class MemeOverlay:
    def __init__(self):
        self.font_title = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_subtitle = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_quote = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_body = pygame.font.SysFont("Arial", 16)
        self.font_btn = pygame.font.SysFont("Arial", 18, bold=True)

        # Popup de Queijo Perdido
        self.lost_popup_active = False
        self.lost_popup_timer = 0.0
        self.lost_popup_quote = ""
        self.lost_popup_img = None

        # Carrega imagens
        self.img_wheezy = self._load_scaled_image(IMG_DEFEAT_WHEEZY, max_w=280, max_h=300)
        self.img_victory = self._load_scaled_image(IMG_VICTORY_KING, max_w=280, max_h=300)
        
        self.lost_meme_images = []
        for path in [IMG_MEME_LOST_1, IMG_MEME_LOST_2]:
            img = self._load_scaled_image(path, max_w=120, max_h=120)
            if img:
                self.lost_meme_images.append(img)

    def _load_scaled_image(self, path, max_w, max_h):
        if not os.path.exists(path):
            return None
        try:
            raw = pygame.image.load(path).convert_alpha()
            w, h = raw.get_size()
            scale = min(max_w / w, max_h / h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            return pygame.transform.smoothscale(raw, (new_w, new_h))
        except Exception as e:
            print(f"[MemeOverlay] Erro ao carregar {path}: {e}")
            return None

    def trigger_lost_cheese(self):
        """Dispara o popup cômico de queijo perdido."""
        self.lost_popup_active = True
        self.lost_popup_timer = 2.2  # Duração em segundos
        self.lost_popup_quote = random.choice(LOST_CHEESE_QUOTES)
        if self.lost_meme_images:
            self.lost_popup_img = random.choice(self.lost_meme_images)
        else:
            self.lost_popup_img = None

    def update(self, dt):
        """Atualiza cronômetro do popup temporário."""
        if self.lost_popup_active:
            self.lost_popup_timer -= dt
            if self.lost_popup_timer <= 0:
                self.lost_popup_active = False

    def draw_lost_popup(self, surface):
        """Desenha uma notificação estilo meme moderno na parte inferior da tela."""
        if not self.lost_popup_active:
            return

        box_w = 540
        box_h = 100
        box_x = (SCREEN_WIDTH - box_w) // 2
        box_y = SCREEN_HEIGHT - box_h - 25

        # Card de fundo com borda arredondada e sombra
        s = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        pygame.draw.rect(s, (20, 24, 38, 245), (0, 0, box_w, box_h), border_radius=16)
        pygame.draw.rect(s, (255, 75, 90), (0, 0, box_w, box_h), 2, border_radius=16)
        surface.blit(s, (box_x, box_y))

        # Imagem do meme na esquerda
        text_x_offset = box_x + 20
        if self.lost_popup_img:
            img_y = box_y + (box_h - self.lost_popup_img.get_height()) // 2
            surface.blit(self.lost_popup_img, (box_x + 12, img_y))
            text_x_offset = box_x + self.lost_popup_img.get_width() + 24

        # Texto do aviso
        title_alert = self.font_subtitle.render("[!] QUEIJO PERDIDO!", True, (255, 80, 100))
        quote_text = self.font_quote.render(f'"{self.lost_popup_quote}"', True, COLOR_TEXT_LIGHT)
        
        surface.blit(title_alert, (text_x_offset, box_y + 20))
        surface.blit(quote_text, (text_x_offset, box_y + 50))

    def draw_defeat_screen(self, surface, score):
        """Desenha a tela de derrota com o meme do Wheezy do Toy Story anexado pelo usuário."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 12, 20, 220))
        surface.blit(overlay, (0, 0))

        card_w = 640
        card_h = 540
        card_x = (SCREEN_WIDTH - card_w) // 2
        card_y = (SCREEN_HEIGHT - card_h) // 2

        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, COLOR_CARD_BG, (0, 0, card_w, card_h), border_radius=24)
        pygame.draw.rect(card_surf, COLOR_DANGER, (0, 0, card_w, card_h), 3, border_radius=24)
        surface.blit(card_surf, (card_x, card_y))

        # Título
        title = self.font_title.render("DERROTA!", True, COLOR_DANGER)
        surface.blit(title, (card_x + (card_w - title.get_width()) // 2, card_y + 18))

        # Imagem Meme do Wheezy
        if self.img_wheezy:
            img_x = card_x + (card_w - self.img_wheezy.get_width()) // 2
            img_y = card_y + 68
            pygame.draw.rect(
                surface, (10, 10, 15),
                (img_x - 4, img_y - 4, self.img_wheezy.get_width() + 8, self.img_wheezy.get_height() + 8),
                border_radius=12
            )
            surface.blit(self.img_wheezy, (img_x, img_y))
            content_y = img_y + self.img_wheezy.get_height() + 16
        else:
            content_y = card_y + 180

        # Subtítulo cômico
        sub = self.font_subtitle.render('"Ficou só o pó do Wheezy..."', True, COLOR_PRIMARY)
        surface.blit(sub, (card_x + (card_w - sub.get_width()) // 2, content_y))

        score_info = self.font_body.render(
            f"Você coletou {score} de {TARGET_SCORE} queijos antes de ficar sem vidas.",
            True, COLOR_TEXT_MUTED
        )
        surface.blit(score_info, (card_x + (card_w - score_info.get_width()) // 2, content_y + 30))

        # Botão estilizado
        btn_box = pygame.Rect(card_x + 50, card_y + card_h - 60, card_w - 100, 42)
        pygame.draw.rect(surface, (230, 50, 75), btn_box, border_radius=10)
        prompt_btn = self.font_btn.render("[R] TENTAR NOVAMENTE   |   [ESC] SAIR", True, COLOR_TEXT_LIGHT)
        surface.blit(
            prompt_btn,
            (btn_box.x + (btn_box.width - prompt_btn.get_width()) // 2,
             btn_box.y + (btn_box.height - prompt_btn.get_height()) // 2)
        )

    def draw_victory_screen(self, surface, score):
        """Desenha a tela triunfante de vitória."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 20, 15, 215))
        surface.blit(overlay, (0, 0))

        card_w = 640
        card_h = 540
        card_x = (SCREEN_WIDTH - card_w) // 2
        card_y = (SCREEN_HEIGHT - card_h) // 2

        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, COLOR_CARD_BG, (0, 0, card_w, card_h), border_radius=24)
        pygame.draw.rect(card_surf, COLOR_SUCCESS, (0, 0, card_w, card_h), 3, border_radius=24)
        surface.blit(card_surf, (card_x, card_y))

        # Título
        title = self.font_title.render("VITORIA! O REI DO QUEIJO!", True, COLOR_PRIMARY)
        surface.blit(title, (card_x + (card_w - title.get_width()) // 2, card_y + 18))

        # Imagem do Rato Campeão
        if self.img_victory:
            img_x = card_x + (card_w - self.img_victory.get_width()) // 2
            img_y = card_y + 68
            pygame.draw.rect(
                surface, (15, 30, 20),
                (img_x - 4, img_y - 4, self.img_victory.get_width() + 8, self.img_victory.get_height() + 8),
                border_radius=12
            )
            surface.blit(self.img_victory, (img_x, img_y))
            content_y = img_y + self.img_victory.get_height() + 16
        else:
            content_y = card_y + 180

        sub = self.font_subtitle.render("Banquete Conquistado com Sucesso!", True, COLOR_SUCCESS)
        surface.blit(sub, (card_x + (card_w - sub.get_width()) // 2, content_y))

        score_info = self.font_body.render(
            f"Voce coletou todos os {TARGET_SCORE} queijos a tempo!",
            True, COLOR_TEXT_MUTED
        )
        surface.blit(score_info, (card_x + (card_w - score_info.get_width()) // 2, content_y + 30))

        # Botão
        btn_box = pygame.Rect(card_x + 50, card_y + card_h - 60, card_w - 100, 42)
        pygame.draw.rect(surface, (38, 185, 100), btn_box, border_radius=10)
        prompt_btn = self.font_btn.render("[R] JOGAR NOVAMENTE   |   [ESC] SAIR", True, COLOR_TEXT_LIGHT)
        surface.blit(
            prompt_btn,
            (btn_box.x + (btn_box.width - prompt_btn.get_width()) // 2,
             btn_box.y + (btn_box.height - prompt_btn.get_height()) // 2)
        )

    def draw_start_screen(self, surface):
        """Tela inicial com instruções e controles."""
        card_w = 680
        card_h = 500
        card_x = (SCREEN_WIDTH - card_w) // 2
        card_y = (SCREEN_HEIGHT - card_h) // 2

        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, COLOR_CARD_BG, (0, 0, card_w, card_h), border_radius=24)
        pygame.draw.rect(card_surf, COLOR_PRIMARY, (0, 0, card_w, card_h), 2, border_radius=24)
        surface.blit(card_surf, (card_x, card_y))

        # Título
        title = self.font_title.render("RATO EM BUSCA DO QUEIJO", True, COLOR_PRIMARY)
        surface.blit(title, (card_x + (card_w - title.get_width()) // 2, card_y + 35))

        sub = self.font_subtitle.render("Edicao Especial com Sons & Memes", True, COLOR_TEXT_MUTED)
        surface.blit(sub, (card_x + (card_w - sub.get_width()) // 2, card_y + 80))

        # Instruções
        instructions = [
            ("[*] OBJETIVO:", True),
            (f"    - Colete {TARGET_SCORE} queijos para vencer a partida!", False),
            ("    - Cada queijo colidido teleporta para outro lugar da tela.", False),
            ("    - Atencao ao tempo! Se o queijo expirar, voce perde vida e toma meme!", False),
            ("", False),
            ("[*] CONTROLES:", True),
            ("    - Teclas Direcionais [Setas] ou [W, A, S, D]: Movimentam o Rato", False),
            ("    - Tecla [P]: Pausar o jogo", False),
            ("    - Tecla [M]: Ligar / Desligar sons e musica", False)
        ]

        curr_y = card_y + 130
        for line, is_header in instructions:
            if is_header:
                color = COLOR_PRIMARY
                font = self.font_subtitle
            else:
                color = COLOR_TEXT_LIGHT
                font = self.font_body
            txt = font.render(line, True, color)
            surface.blit(txt, (card_x + 50, curr_y))
            curr_y += 28

        # Botão Iniciar
        btn_box = pygame.Rect(card_x + 60, card_y + card_h - 75, card_w - 120, 50)
        pygame.draw.rect(surface, (255, 175, 25), btn_box, border_radius=12)
        btn_txt = self.font_title.render("PRESSIONE [ESPACO] PARA JOGAR", True, (20, 20, 30))
        btn_txt_scaled = pygame.transform.smoothscale(btn_txt, (int(btn_txt.get_width() * 0.72), int(btn_txt.get_height() * 0.72)))
        surface.blit(
            btn_txt_scaled,
            (btn_box.x + (btn_box.width - btn_txt_scaled.get_width()) // 2,
             btn_box.y + (btn_box.height - btn_txt_scaled.get_height()) // 2)
        )

    def draw_pause_screen(self, surface):
        """Tela de pausa sutil."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        title = self.font_title.render("JOGO PAUSADO", True, COLOR_PRIMARY)
        sub = self.font_subtitle.render("Pressione [P] para continuar ou [ESC] para sair", True, COLOR_TEXT_LIGHT)
        
        surface.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, SCREEN_HEIGHT // 2 - 40))
        surface.blit(sub, ((SCREEN_WIDTH - sub.get_width()) // 2, SCREEN_HEIGHT // 2 + 15))
