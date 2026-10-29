"""
Módulo de Configuração e Constantes Globais do Jogo
"""
import os

# Dimensões da Janela
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 680
FPS = 60
TITLE = "🐭 Rato em Busca do Queijo - Edição Memes"

# Diretórios de Assets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# Caminhos das Imagens
IMG_MOUSE = os.path.join(IMAGES_DIR, "mouse.png")
IMG_CHEESE = os.path.join(IMAGES_DIR, "cheese.png")
IMG_DEFEAT_WHEEZY = os.path.join(IMAGES_DIR, "derrota_wheezy.png")
IMG_VICTORY_KING = os.path.join(IMAGES_DIR, "vitoria_king.png")
IMG_MEME_LOST_1 = os.path.join(IMAGES_DIR, "meme_lost_1.png")
IMG_MEME_LOST_2 = os.path.join(IMAGES_DIR, "meme_lost_2.png")

# Caminhos dos Sons
SND_EAT = os.path.join(SOUNDS_DIR, "eat.wav")
SND_LOST = os.path.join(SOUNDS_DIR, "lost.wav")
SND_WIN = os.path.join(SOUNDS_DIR, "win.wav")
SND_LOSE = os.path.join(SOUNDS_DIR, "lose.wav")
SND_BGM = os.path.join(SOUNDS_DIR, "bgm.wav")

# Regras do Jogo
MOUSE_SPEED = 7.0
MOUSE_SIZE = (76, 76)
CHEESE_SIZE = (64, 64)
CHEESE_LIFETIME = 5.5  # Segundos que um queijo dura na tela antes de expirar
TARGET_SCORE = 10     # Queijos necessários para vitória
MAX_LIVES = 3         # Vidas do jogador

# Paleta de Cores Moderna e Agradável (RGB)
COLOR_BG_TOP = (36, 41, 62)         # Azul Ardósia Escuro
COLOR_BG_BOTTOM = (20, 24, 38)      # Fundo Profundo
COLOR_TILE_1 = (44, 50, 75)         # Grid sutil piso 1
COLOR_TILE_2 = (38, 44, 68)         # Grid sutil piso 2

COLOR_PRIMARY = (255, 180, 0)       # Dourado Queijo
COLOR_PRIMARY_GLOW = (255, 215, 64)
COLOR_ACCENT = (255, 75, 110)       # Rosa vibrante
COLOR_SUCCESS = (46, 213, 115)      # Verde vitória
COLOR_DANGER = (255, 71, 87)        # Vermelho derrota
COLOR_TEXT_LIGHT = (245, 247, 250)
COLOR_TEXT_MUTED = (164, 176, 190)
COLOR_HUD_BG = (25, 30, 48, 220)    # Barra superior com transparência
COLOR_CARD_BG = (28, 33, 53, 240)

# Frases cômicas para quando um queijo for perdido
LOST_CHEESE_QUOTES = [
    "O queijo foi de arrasta pra cima!",
    "Mais lerdo que Wi-Fi de padaria!",
    "O queijo cansou de esperar e evaporou!",
    "Visão turva: cadê o bendito queijo?!",
    "O gato comeu antes de você chegar!",
    "Queijo vencido! O PROCON foi acionado!"
]
