"""
Classe da Entidade do Rato (Jogador)
"""
import pygame
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, MOUSE_SPEED, MOUSE_SIZE, IMG_MOUSE
from src.entities.particle import Particle

class Mouse:
    def __init__(self, x=None, y=None):
        self.width, self.height = MOUSE_SIZE
        self.x = x if x is not None else SCREEN_WIDTH // 2 - self.width // 2
        self.y = y if y is not None else SCREEN_HEIGHT // 2 - self.height // 2
        self.speed = MOUSE_SPEED
        
        # Orientação e Animação
        self.facing_right = True
        self.walk_time = 0.0
        self.is_moving = False
        
        # Carrega o sprite original
        self.raw_sprite = self._load_sprite()
        self.sprite_right = pygame.transform.smoothscale(self.raw_sprite, (self.width, self.height))
        self.sprite_left = pygame.transform.flip(self.sprite_right, True, False)
        
        # Bounding box para colisão mais precisa (ajustada para ignorar bordas vazias)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitbox = pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 20)

    def _load_sprite(self):
        """Carrega imagem do rato ou cria uma forma procedural caso o arquivo falhe."""
        try:
            return pygame.image.load(IMG_MOUSE).convert_alpha()
        except Exception as e:
            print(f"[Mouse] Erro ao carregar imagem: {e}. Criando sprite reserva.")
            surface = pygame.Surface(MOUSE_SIZE, pygame.SRCALPHA)
            pygame.draw.ellipse(surface, (140, 140, 150), (10, 15, 55, 45))
            pygame.draw.circle(surface, (230, 130, 150), (20, 15), 14)
            pygame.draw.circle(surface, (20, 20, 20), (55, 30), 4)
            return surface

    def handle_input(self, keys):
        """Processa entrada do teclado (teclas direcionais e WASD)."""
        dx, dy = 0.0, 0.0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1.0
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1.0
            self.facing_right = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1.0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1.0

        # Normaliza movimento diagonal
        if dx != 0 and dy != 0:
            inv_len = 1.0 / math.sqrt(dx * dx + dy * dy)
            dx *= inv_len
            dy *= inv_len

        self.is_moving = (dx != 0 or dy != 0)
        
        # Move com limites da tela (respeita margem superior da HUD de 75px)
        hud_top_limit = 75
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        self.x = max(10, min(SCREEN_WIDTH - self.width - 10, self.x))
        self.y = max(hud_top_limit + 5, min(SCREEN_HEIGHT - self.height - 10, self.y))

        # Atualiza caixas de colisão
        self.rect.topleft = (int(self.x), int(self.y))
        self.hitbox.topleft = (int(self.x + 12), int(self.y + 12))

    def update(self, particles_list):
        """Atualiza animações de passo e gera pequenas poeirinhas ao correr."""
        if self.is_moving:
            self.walk_time += 0.25
            # Solta poeirinha a cada poucos passos
            if int(self.walk_time * 2) % 3 == 0:
                spawn_x = self.x + (15 if self.facing_right else self.width - 15)
                spawn_y = self.y + self.height - 8
                particles_list.append(Particle(
                    spawn_x, spawn_y, (180, 190, 210),
                    vx=(-1 if self.facing_right else 1) * 0.8,
                    vy=-0.4, size=3, lifetime=15
                ))
        else:
            self.walk_time = 0.0

    def draw(self, surface):
        """Desenha o rato com sombra e leve salto de caminhada."""
        current_sprite = self.sprite_right if self.facing_right else self.sprite_left
        
        # Efeito de balanço de corrida
        bounce_offset = math.sin(self.walk_time) * 3 if self.is_moving else 0
        
        # Sombra sob o rato
        shadow_rect = pygame.Rect(self.x + 10, self.y + self.height - 10, self.width - 20, 12)
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 80), (0, 0, shadow_rect.width, shadow_rect.height))
        surface.blit(shadow_surf, shadow_rect.topleft)
        
        # Desenha o sprite do rato
        surface.blit(current_sprite, (int(self.x), int(self.y + bounce_offset)))

    def reset(self):
        """Reinicia a posição inicial do rato no centro."""
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT // 2 - self.height // 2
        self.facing_right = True
        self.rect.topleft = (int(self.x), int(self.y))
        self.hitbox.topleft = (int(self.x + 12), int(self.y + 12))
