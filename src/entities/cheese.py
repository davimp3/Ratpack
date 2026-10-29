"""
Classe da Entidade do Queijo
"""
import pygame
import random
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, CHEESE_SIZE, CHEESE_LIFETIME, IMG_CHEESE
from src.entities.particle import Particle

class Cheese:
    def __init__(self, avoid_pos=None):
        self.width, self.height = CHEESE_SIZE
        self.max_lifetime = CHEESE_LIFETIME
        self.lifetime = self.max_lifetime
        
        self.raw_sprite = self._load_sprite()
        self.sprite = pygame.transform.smoothscale(self.raw_sprite, (self.width, self.height))
        
        self.hover_angle = 0.0
        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.hitbox = pygame.Rect(0, 0, self.width - 16, self.height - 16)
        
        self.respawn(avoid_pos)

    def _load_sprite(self):
        """Carrega imagem do queijo ou cria fallback procedural."""
        try:
            return pygame.image.load(IMG_CHEESE).convert_alpha()
        except Exception as e:
            print(f"[Cheese] Erro ao carregar imagem: {e}. Criando sprite reserva.")
            surface = pygame.Surface(CHEESE_SIZE, pygame.SRCALPHA)
            pygame.draw.polygon(surface, (255, 195, 0), [(10, 50), (55, 50), (32, 12)])
            pygame.draw.circle(surface, (220, 160, 0), (25, 38), 6)
            pygame.draw.circle(surface, (220, 160, 0), (42, 35), 5)
            return surface

    def respawn(self, avoid_pos=None):
        """Move o queijo para uma posição aleatória longe do jogador e da barra superior."""
        hud_margin = 85
        margin_x = 40
        margin_y = 40
        
        max_attempts = 30
        for _ in range(max_attempts):
            rx = random.randint(margin_x, SCREEN_WIDTH - self.width - margin_x)
            ry = random.randint(hud_margin + margin_y, SCREEN_HEIGHT - self.height - margin_y)
            
            if avoid_pos:
                dist = math.hypot(rx - avoid_pos[0], ry - avoid_pos[1])
                if dist < 180:
                    continue
            self.x = rx
            self.y = ry
            break
        else:
            self.x = random.randint(margin_x, SCREEN_WIDTH - self.width - margin_x)
            self.y = random.randint(hud_margin + margin_y, SCREEN_HEIGHT - self.height - margin_y)

        self.lifetime = self.max_lifetime
        self.hover_angle = random.uniform(0, math.pi * 2)
        self._update_rects()

    def _update_rects(self, y_offset=0):
        self.rect.topleft = (int(self.x), int(self.y + y_offset))
        self.hitbox.topleft = (int(self.x + 8), int(self.y + y_offset + 8))

    def update(self, dt, particles_list):
        """Atualiza o tempo de vida restante e animação flutuante."""
        self.lifetime -= dt
        self.hover_angle += 0.08
        
        # Emite pequenas partículas brilhantes douradas esporadicamente
        if random.random() < 0.25:
            sparkle_x = self.x + random.uniform(5, self.width - 5)
            sparkle_y = self.y + random.uniform(5, self.height - 5)
            particles_list.append(Particle(
                sparkle_x, sparkle_y, (255, 235, 100),
                vx=random.uniform(-0.5, 0.5), vy=random.uniform(-1.0, -0.2),
                size=3, lifetime=22
            ))

    def draw(self, surface):
        """Desenha o queijo com aura pulsante, sombra e flutuação suave."""
        y_bob = math.sin(self.hover_angle) * 6
        self._update_rects(y_bob)

        # Sombra no chão (estática em relação ao pulo)
        shadow_width = max(10, int(self.width * 0.75 - abs(y_bob)))
        shadow_rect = pygame.Rect(
            self.x + (self.width - shadow_width) // 2,
            self.y + self.height - 4,
            shadow_width, 10
        )
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 70), (0, 0, shadow_rect.width, shadow_rect.height))
        surface.blit(shadow_surf, shadow_rect.topleft)

        # Aura de brilho dourado pulsante
        pulse = (math.sin(self.hover_angle * 1.5) + 1.0) * 0.5
        glow_size = int(self.width + 16 + pulse * 8)
        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        glow_alpha = int(45 + pulse * 40)
        pygame.draw.circle(
            glow_surf, (255, 200, 40, glow_alpha),
            (glow_size // 2, glow_size // 2), glow_size // 2
        )
        surface.blit(
            glow_surf,
            (self.x + self.width // 2 - glow_size // 2,
             self.y + y_bob + self.height // 2 - glow_size // 2)
        )

        # Sprite do queijo
        surface.blit(self.sprite, (int(self.x), int(self.y + y_bob)))

    @property
    def is_expired(self):
        return self.lifetime <= 0

    @property
    def time_ratio(self):
        """Retorna proporção de 1.0 a 0.0 do tempo de frescor do queijo."""
        return max(0.0, min(1.0, self.lifetime / self.max_lifetime))
