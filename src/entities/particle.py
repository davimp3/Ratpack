"""
Sistema de Partículas e Textos Flutuantes
"""
import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color, vx=None, vy=None, size=None, lifetime=40):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 5.0)
        self.vx = vx if vx is not None else math.cos(angle) * speed
        self.vy = vy if vy is not None else math.sin(angle) * speed
        self.size = size if size is not None else random.uniform(3, 7)
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = 0.12

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime <= 0:
            return
        alpha_ratio = max(0.0, self.lifetime / self.max_lifetime)
        current_size = max(1, int(self.size * alpha_ratio))
        
        # Desenha partícula com alfa
        s = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
        color_with_alpha = (*self.color[:3], int(255 * alpha_ratio))
        pygame.draw.circle(s, color_with_alpha, (current_size, current_size), current_size)
        surface.blit(s, (int(self.x - current_size), int(self.y - current_size)))

    @property
    def is_alive(self):
        return self.lifetime > 0


class FloatingText:
    def __init__(self, x, y, text, color=(255, 215, 0), font_size=26, lifetime=45):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.vy = -1.8

    def update(self):
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime <= 0:
            return
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        rendered = self.font.render(self.text, True, self.color)
        alpha_surface = pygame.Surface(rendered.get_size(), pygame.SRCALPHA)
        alpha_surface.blit(rendered, (0, 0))
        alpha_surface.set_alpha(alpha)
        
        # Sombra sutil
        shadow = self.font.render(self.text, True, (0, 0, 0))
        shadow_surf = pygame.Surface(shadow.get_size(), pygame.SRCALPHA)
        shadow_surf.blit(shadow, (0, 0))
        shadow_surf.set_alpha(int(alpha * 0.6))
        
        surface.blit(shadow_surf, (self.x - rendered.get_width() // 2 + 2, self.y + 2))
        surface.blit(alpha_surface, (self.x - rendered.get_width() // 2, self.y))

    @property
    def is_alive(self):
        return self.lifetime > 0


class ConfettiParticle:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-50, -10)
        self.screen_height = screen_height
        self.colors = [
            (255, 71, 87), (46, 213, 115), (255, 186, 0),
            (30, 144, 255), (165, 94, 234), (255, 107, 129)
        ]
        self.color = random.choice(self.colors)
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(2.5, 6.0)
        self.w = random.randint(6, 12)
        self.h = random.randint(6, 12)
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-5, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rot_speed

    def draw(self, surface):
        s = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(s, self.color, (0, 0, self.w, self.h), border_radius=2)
        rot_s = pygame.transform.rotate(s, self.rotation)
        surface.blit(rot_s, (int(self.x), int(self.y)))

    @property
    def is_alive(self):
        return self.y < self.screen_height + 20
