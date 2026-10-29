# 🐭 Rato em Busca do Queijo - Edição Memes 🧀

Um jogo 2D interativo e bem-humorado desenvolvido em **Python** com **Pygame-CE**, com visual moderno, efeitos de partículas, trilha sonora, efeitos de áudio e memes divertidos (incluindo o meme do **Wheezy** de Toy Story na derrota).

---

## 📸 Demonstração e Visual
- **Visual Moderno e Colorido**: Sprites em alta definição com transparência real, animação de passos/balanço do rato e queijo flutuante com brilho dourado pulsante.
- **HUD Glassmórfico**: Placar com ícone do queijo, barra de frescor/tempo em degradê (verde/amarelo/vermelho) e vidas com corações vetoriais.
- **Sistema de Partículas**: Migalhas de queijo explosivas ao coletar, rastro de poeira ao correr e chuva de confetes festivos na vitória.
- **Sons Personalizados**:
  - Som de coleta ("nom nom / chime" alegre)
  - Som de queijo perdido (efeito cômico de escorregão)
  - Som de vitória (fanfarra triunfante)
  - Som de derrota (sad trombone: "wah-wah-wah-waaah")
  - Música de fundo chiptune animada e relaxante
- **Memes Integrados**:
  - Popups aleatórios com memes e frases cômicas quando o queijo expira e você perde vidas ("It is Fine", Hamster desesperado, etc.).
  - **Tela de Derrota com o Wheezy**: exibe o meme clássico do pinguim empoeirado ("Ficou só o pó do Wheezy...").
  - **Tela de Vitória**: exibe o Rato Campeão coroado como "Rei do Queijo".

---

## 🎮 Controles

| Tecla | Ação |
| :--- | :--- |
| **⬆️ ⬇️ ⬅️ ➡️** ou **W, A, S, D** | Movimenta o Rato pelo cenário |
| **P** ou **ESC** | Pausa / Retoma o jogo |
| **M** | Liga / Desliga o Áudio (Mudo) |
| **R** | Reinicia a partida (nas telas de vitória/derrota) |
| **ESPAÇO / ENTER** | Inicia o jogo a partir do menu |

---

## 📁 Estrutura Organizada de Pastas

```text
Pratica04/
├── main.py                     # Ponto de entrada do jogo
├── requirements.txt            # Dependências (pygame-ce, Pillow)
├── README.md                   # Documentação detalhada
├── assets/                     # Recursos visuais e auditivos
│   ├── images/
│   │   ├── mouse.png           # Sprite moderno do rato (transparente)
│   │   ├── cheese.png          # Sprite moderno do queijo (transparente)
│   │   ├── derrota_wheezy.png  # Meme do Wheezy (anexado pelo usuário)
│   │   ├── vitoria_king.png    # Imagem de comemoração da vitória
│   │   ├── meme_lost_1.png     # Meme cômico 1 de queijo perdido
│   │   └── meme_lost_2.png     # Meme cômico 2 de queijo perdido
│   └── sounds/
│       ├── eat.wav             # Som de coleta do queijo
│       ├── lost.wav            # Som de queijo perdido
│       ├── win.wav             # Fanfarra de vitória
│       ├── lose.wav            # Sad trombone de derrota
│       └── bgm.wav             # Trilha musical de fundo
└── src/                        # Código-fonte modular
    ├── __init__.py
    ├── config.py               # Configurações, cores e constantes
    ├── game.py                 # Loop principal e máquina de estados
    ├── audio/
    │   ├── __init__.py
    │   └── sound_manager.py    # Gerenciamento de áudio e música
    ├── entities/
    │   ├── __init__.py
    │   ├── mouse.py            # Entidade do jogador (Rato)
    │   ├── cheese.py           # Entidade do Queijo com tempo e respawn
    │   └── particle.py         # Partículas, textos flutuantes e confetes
    └── ui/
        ├── __init__.py
        ├── hud.py              # Interface superior (placar, timer, corações)
        └── meme_overlay.py     # Modais de vitória, derrota e popups
```

---

## 🚀 Como Executar

### 1. Pré-requisitos
Certifique-se de ter o Python 3.10+ instalado no seu sistema.

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Iniciar o jogo
```bash
python3 main.py
```

Divirta-se buscando os queijos e cuidado para não deixar o queijo estragar! 🧀🐭
