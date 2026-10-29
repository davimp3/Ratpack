"""
Motor Principal do Jogo (Game Loop e Gerenciador de Estados)
"""
import pygame
import sys
import random
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, COLOR_BG_TOP, COLOR_BG_BOTTOM,
    COLOR_TILE_1, COLOR_TILE_2, TARGET_SCORE, MAX_LIVES
)
from src.entities.mouse import Mouse
from src.entities.cheese import Cheese
from src.entities.particle import Particle, FloatingText, ConfettiParticle
from src.ui.hud import HUD
from src.ui.meme_overlay import MemeOverlay
from src.audio.sound_manager import SoundManager

# Estados do Jogo
STATE_START = "START"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAME_OVER = "GAME_OVER"
STATE_VICTORY = "VICTORY"

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = STATE_START

        # Sistemas
        self.sound_manager = SoundManager()
        self.hud = HUD()
        self.meme_overlay = MemeOverlay()

        # Entidades do Jogo
        self.mouse = Mouse()
        self.cheese = Cheese(avoid_pos=(self.mouse.x, self.mouse.y))
        
        # Coleções de Efeitos Visuais
        self.particles = []
        self.floating_texts = []
        self.confetti = []

        # Estado da Partida
        self.score = 0
        self.lives = MAX_LIVES

        # Prepara Superfície de Fundo Estilizada
        self.background_surface = self._create_background_surface()

    def _create_background_surface(self):
        """Gera uma superfície de fundo pré-renderizada com padrão de piso de cozinha moderno."""
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Gradiente suave
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(COLOR_BG_TOP[0] * (1 - ratio) + COLOR_BG_BOTTOM[0] * ratio)
            g = int(COLOR_BG_TOP[1] * (1 - ratio) + COLOR_BG_BOTTOM[1] * ratio)
            b = int(COLOR_BG_TOP[2] * (1 - ratio) + COLOR_BG_BOTTOM[2] * ratio)
            pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Grade sutil de azulejos elegantes
        tile_size = 60
        hud_limit = 70
        for x in range(0, SCREEN_WIDTH, tile_size):
            for y in range(hud_limit, SCREEN_HEIGHT, tile_size):
                color = COLOR_TILE_1 if (x // tile_size + y // tile_size) % 2 == 0 else COLOR_TILE_2
                pygame.draw.rect(surf, color, (x, y, tile_size - 1, tile_size - 1))

        # Vinheta escura nas bordas para profundidade cinematográfica
        vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(vignette, (0, 0, 0, 80), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), width=18)
        surf.blit(vignette, (0, 0))

        return surf

    def reset_game(self):
        """Reinicia os valores da partida para um novo jogo."""
        self.score = 0
        self.lives = MAX_LIVES
        self.particles.clear()
        self.floating_texts.clear()
        self.confetti.clear()
        self.mouse.reset()
        self.cheese.respawn(avoid_pos=(self.mouse.x, self.mouse.y))
        self.state = STATE_PLAYING
        self.sound_manager.play_bgm()

    def handle_events(self):
        """Captura e distribui os eventos do teclado e janela."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                # Atalho Global: Mudo
                if event.key == pygame.K_m:
                    self.sound_manager.toggle_mute()

                # Telas de Vitória ou Derrota
                if self.state in (STATE_GAME_OVER, STATE_VICTORY):
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_START
                        self.sound_manager.stop_bgm()

                # Tela Inicial
                elif self.state == STATE_START:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

                # Durante o Jogo
                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_p:
                        self.state = STATE_PAUSED
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_PAUSED

                # Durante a Pausa
                elif self.state == STATE_PAUSED:
                    if event.key in (pygame.K_p, pygame.K_SPACE):
                        self.state = STATE_PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_START
                        self.sound_manager.stop_bgm()

    def update(self, dt):
        """Atualiza a lógica interna do jogo."""
        # Atualiza sistema de memes sempre
        self.meme_overlay.update(dt)

        if self.state == STATE_PLAYING:
            # 1. Movimento do Jogador (Rato)
            keys = pygame.key.get_pressed()
            self.mouse.handle_input(keys)
            self.mouse.update(self.particles)

            # 2. Atualiza Queijo
            self.cheese.update(dt, self.particles)

            # 3. Verifica Colisão: Rato colidiu com o Queijo?
            if self.mouse.hitbox.colliderect(self.cheese.hitbox):
                # Efeito Sonoro de Coleta
                self.sound_manager.play_sound('eat')
                
                # Partículas de Migalhas Douradas
                for _ in range(18):
                    self.particles.append(Particle(
                        self.cheese.x + self.cheese.width // 2,
                        self.cheese.y + self.cheese.height // 2,
                        random.choice([(255, 215, 0), (255, 180, 20), (255, 240, 120)]),
                        lifetime=35
                    ))
                
                # Texto Flutuante
                self.floating_texts.append(FloatingText(
                    self.cheese.x + self.cheese.width // 2,
                    self.cheese.y - 10,
                    "+1 Queijo!",
                    color=(255, 220, 40)
                ))

                # Incrementa Placar
                self.score += 1

                # O queijo aparece em outro lugar aleatório da tela
                self.cheese.respawn(avoid_pos=(self.mouse.x, self.mouse.y))

                # Condição de Vitória: Atingiu o placar alvo
                if self.score >= TARGET_SCORE:
                    self.state = STATE_VICTORY
                    self.sound_manager.stop_bgm()
                    self.sound_manager.play_sound('win')
                    # Cria chuva de confetes inicial
                    for _ in range(60):
                        self.confetti.append(ConfettiParticle(SCREEN_WIDTH, SCREEN_HEIGHT))

            # 4. Verifica se o queijo expirou (Queijo Perdido!)
            elif self.cheese.is_expired:
                # Efeito Sonoro de Queijo Perdido
                self.sound_manager.play_sound('lost')

                # Dispara popup meme
                self.meme_overlay.trigger_lost_cheese()

                # Perde vida
                self.lives -= 1

                # Texto Flutuante de Perda
                self.floating_texts.append(FloatingText(
                    self.cheese.x + self.cheese.width // 2,
                    self.cheese.y - 10,
                    "-1 Vida!",
                    color=(255, 75, 90)
                ))

                # O queijo respawna em outro local
                self.cheese.respawn(avoid_pos=(self.mouse.x, self.mouse.y))

                # Condição de Derrota: Ficou sem vidas
                if self.lives <= 0:
                    self.state = STATE_GAME_OVER
                    self.sound_manager.stop_bgm()
                    self.sound_manager.play_sound('lose')

        # Atualiza partículas e textos flutuantes
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.is_alive]

        for ft in self.floating_texts:
            ft.update()
        self.floating_texts = [ft for ft in self.floating_texts if ft.is_alive]

        # Atualiza confetes de vitória
        if self.state == STATE_VICTORY:
            if random.random() < 0.4:
                self.confetti.append(ConfettiParticle(SCREEN_WIDTH, SCREEN_HEIGHT))
            for c in self.confetti:
                c.update()
            self.confetti = [c for c in self.confetti if c.is_alive]

    def draw(self):
        """Renderiza todas as camadas visuais do jogo."""
        # 1. Fundo
        self.screen.blit(self.background_surface, (0, 0))

        # 2. Entidades do Jogo (se em jogo ou pausado)
        if self.state in (STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER, STATE_VICTORY):
            self.cheese.draw(self.screen)
            self.mouse.draw(self.screen)

            # Partículas e Textos
            for p in self.particles:
                p.draw(self.screen)
            for ft in self.floating_texts:
                ft.draw(self.screen)

            # Confetes (se vitória)
            if self.state == STATE_VICTORY:
                for c in self.confetti:
                    c.draw(self.screen)

            # HUD Superior
            self.hud.draw(
                self.screen,
                self.score,
                self.lives,
                self.cheese.time_ratio,
                self.sound_manager.muted
            )

            # Notificação / Popup de Queijo Perdido (somente durante a partida ativa)
            if self.state == STATE_PLAYING:
                self.meme_overlay.draw_lost_popup(self.screen)

        # 3. Sobreposições de Telas conforme Estado
        if self.state == STATE_START:
            self.meme_overlay.draw_start_screen(self.screen)
        elif self.state == STATE_PAUSED:
            self.meme_overlay.draw_pause_screen(self.screen)
        elif self.state == STATE_GAME_OVER:
            self.meme_overlay.draw_defeat_screen(self.screen, self.score)
        elif self.state == STATE_VICTORY:
            self.meme_overlay.draw_victory_screen(self.screen, self.score)

        pygame.display.flip()

    def run(self):
        """Loop Principal."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time em segundos
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()
