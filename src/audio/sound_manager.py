"""
Gerenciador de Efeitos Sonoros e Música de Fundo
"""
import pygame
from src.config import SND_EAT, SND_LOST, SND_WIN, SND_LOSE, SND_BGM

class SoundManager:
    def __init__(self):
        self.muted = False
        self.sounds_loaded = False
        self.sounds = {}
        
        # Inicializa mixer com suporte a falhas caso o sistema de áudio não responda
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self._load_sounds()
            self.sounds_loaded = True
        except Exception as e:
            print(f"[SoundManager] Aviso: Não foi possível inicializar áudio ({e}). Jogo rodará em modo silencioso.")
            self.sounds_loaded = False

    def _load_sounds(self):
        """Carrega todos os arquivos de efeitos e música."""
        try:
            self.sounds['eat'] = pygame.mixer.Sound(SND_EAT)
            self.sounds['eat'].set_volume(0.8)
            
            self.sounds['lost'] = pygame.mixer.Sound(SND_LOST)
            self.sounds['lost'].set_volume(0.85)
            
            self.sounds['win'] = pygame.mixer.Sound(SND_WIN)
            self.sounds['win'].set_volume(0.9)
            
            self.sounds['lose'] = pygame.mixer.Sound(SND_LOSE)
            self.sounds['lose'].set_volume(0.9)
            
            self.sounds['bgm'] = pygame.mixer.Sound(SND_BGM)
            self.sounds['bgm'].set_volume(0.4)
            self.bgm_channel = None
        except Exception as e:
            print(f"[SoundManager] Erro ao carregar sons: {e}")

    def play_sound(self, sound_name):
        """Toca um efeito sonoro caso o som não esteja mutado."""
        if self.muted or not self.sounds_loaded:
            return
        snd = self.sounds.get(sound_name)
        if snd:
            try:
                snd.play()
            except Exception:
                pass

    def play_bgm(self):
        """Inicia a música de fundo em loop contínuo."""
        if self.muted or not self.sounds_loaded:
            return
        bgm = self.sounds.get('bgm')
        if bgm and (self.bgm_channel is None or not self.bgm_channel.get_busy()):
            try:
                self.bgm_channel = bgm.play(loops=-1)
            except Exception:
                pass

    def stop_bgm(self):
        """Para a música de fundo."""
        if self.bgm_channel:
            try:
                self.bgm_channel.stop()
            except Exception:
                pass

    def toggle_mute(self):
        """Alterna mudo/desmudo."""
        self.muted = not self.muted
        if self.muted:
            self.stop_bgm()
        else:
            self.play_bgm()
        return self.muted
