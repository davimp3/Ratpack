"""
Interface do Usuário (HUD - Heads-Up Display)
"""
import pygame
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_HUD_BG, COLOR_PRIMARY, COLOR_PRIMARY_GLOW,
    COLOR_SUCCESS, COLOR_DANGER, COLOR_TEXT_LIGHT, COLOR_TEXT_MUTED,
    TARGET_SCORE, MAX_LIVES, IMG_CHEESE
)

def draw_heart(surface, cx, cy, size, color):
    """Desenha um coração estilizado e suave."""
    r = size // 3
    pygame.draw.circle(surface, color, (cx - r // 2, cy - r // 4), r)
    pygame.draw.circle(surface, color, (cx + r // 2, cy - r // 4), r)
    pts = [
        (cx - size // 2, cy - 2),
        (cx + size // 2, cy - 2),
        (cx, cy + size // 2 + 2)
    ]
    pygame.draw.polygon(surface, color, pts)

class HUD:
    def __init__(self):
        self.font_main = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 14, bold=True)
        
        # Mini ícone do queijo para o placar
        try:
            raw_cheese = pygame.image.load(IMG_CHEESE).convert_alpha()
            self.cheese_icon = pygame.transform.smoothscale(raw_cheese, (28, 28))
        except Exception:
            self.cheese_icon = None

    def draw(self, surface, score, lives, cheese_time_ratio, is_muted):
        hud_height = 68
        hud_surf = pygame.Surface((SCREEN_WIDTH, hud_height), pygame.SRCALPHA)
        hud_surf.fill(COLOR_HUD_BG)
        
        # Borda inferior fina e luminosa
        pygame.draw.line(hud_surf, (80, 95, 140, 180), (0, hud_height - 1), (SCREEN_WIDTH, hud_height - 1), 2)
        surface.blit(hud_surf, (0, 0))

        # 1. QUEIJOS COLETADOS (Placar com ícone gráfico)
        icon_x = 22
        if self.cheese_icon:
            surface.blit(self.cheese_icon, (icon_x, 19))
            score_x = icon_x + 36
        else:
            score_x = icon_x

        score_text = f"Queijos: {score} / {TARGET_SCORE}"
        score_rendered = self.font_main.render(score_text, True, COLOR_PRIMARY)
        surface.blit(score_rendered, (score_x, 21))

        # 2. BARRA DE FRESCOR / TEMPO DO QUEIJO (Centro)
        bar_width = 240
        bar_height = 14
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = 34

        label_time = self.font_small.render("TEMPO DE FRESCOR DO QUEIJO", True, COLOR_TEXT_MUTED)
        surface.blit(label_time, (bar_x + (bar_width - label_time.get_width()) // 2, 14))

        # Fundo da barra
        pygame.draw.rect(surface, (45, 52, 75), (bar_x, bar_y, bar_width, bar_height), border_radius=7)

        # Cor dinâmica: Verde -> Amarelo -> Vermelho
        if cheese_time_ratio > 0.5:
            bar_color = COLOR_SUCCESS
        elif cheese_time_ratio > 0.25:
            bar_color = (255, 185, 30)
        else:
            bar_color = COLOR_DANGER

        current_fill_w = max(0, int(bar_width * cheese_time_ratio))
        if current_fill_w > 0:
            pygame.draw.rect(surface, bar_color, (bar_x, bar_y, current_fill_w, bar_height), border_radius=7)
        # Borda sutil
        pygame.draw.rect(surface, (100, 115, 150), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=7)

        # 3. VIDAS (Direita, desenhadas com corações vetoriais)
        lives_x = SCREEN_WIDTH - 200
        lives_label = self.font_main.render("Vidas:", True, COLOR_TEXT_LIGHT)
        surface.blit(lives_label, (lives_x, 21))

        heart_spacing = 28
        for i in range(MAX_LIVES):
            hx = lives_x + 85 + (i * heart_spacing)
            hy = 34
            if i < lives:
                draw_heart(surface, hx, hy, 20, (255, 71, 87))
            else:
                draw_heart(surface, hx, hy, 20, (80, 90, 110))

        # 4. ATALHOS / STATUS NO CANTO INFERIOR
        audio_text = "[M] Áudio: Mudo" if is_muted else "[M] Áudio: Ligado"
        audio_surf = self.font_small.render(f"{audio_text}  |  [P] Pausar", True, (130, 140, 170))
        surface.blit(audio_surf, (SCREEN_WIDTH - audio_surf.get_width() - 15, SCREEN_HEIGHT - 22))
