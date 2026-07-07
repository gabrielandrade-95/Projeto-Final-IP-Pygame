# O Cangaço: A Saga de Lampião

Uma aventura em 2D de ação e sobrevivência inspirada no cangaço nordestino, desenvolvida como projeto final da disciplina de **Introdução à Programação** do curso de **Ciência da Computação na UFPE** (2026.1).

---

##  Sobre o Projeto

O jogo acompanha a jornada de Lampião enfrentando hordas de inimigos em três fases. O projeto foi construído do zero utilizando **Python** e **Pygame**, aplicando conceitos sólidos de **Programação Orientada a Objetos (POO)** como herança, polimorfismo, classes abstratas, gerenciamento de estados (cenas) e persistência de dados (inventário dinâmico).

### Tecnologias e Arquitetura Utilizadas
* **Linguagem Principal:** Python 3.12
* **Biblioteca Gráfica & Áudio:** Pygame 2.x
* **Ambiente de Desenvolvimento (IDE):** Visual Studio Code (VS Code)
---

## 🎮 Funcionalidades Principais

* **Sistema de Cenas Dinâmico:** Fluxo completo entre Menu Principal, Telas de Transição Temporizadas, Pause, Game Over com reset automático e Tela de Vitória.
* **Arquitetura de Áudio Adaptativa:** Trilha sonora contextual por fase e gerenciamento inteligente de canais de áudio (`Sound.play()`) para evitar atrasos (delays) ou cortes abruptos durante combates.
* **Gerenciador de Inventário:** Dicionário dinâmico que mapeia armas desbloqueadas (Peixeira, Revólver e Espingarda) com sincronização em tempo real com o HUD gráfico e inputs do teclado.
* **Mecanismo de Colisões Preciso:** Detecção geométrica integrada por meio de máscaras e retângulos (`Rect`) gerenciando danos, inteligência de projéteis e coleta de itens (como o item Pitú para regenerar vida).

---

## 💻 Como Executar o Jogo

Certifique-se de possuir o **Python 3.10 ou superior**.

### 1. Clonar o repositório

```bash
git clone https://github.com/gabrielandrade-95/Projeto-Final-IP-Pygame.git
cd Projeto-Final-IP-Pygame
```

### 2. Criar e ativar o ambiente virtual

#### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências e executar

```bash
pip install pygame
python main.py
```
---

## Desenvolvedores

| <a href="https://github.com/davidgabrielg10"><img src="https://github.com/davidgabrielg10.png" width="120px;" alt="David Gabriel"/></a> | <a href="https://github.com/DavidDuarte13"><img src="https://github.com/DavidDuarte13.png" width="120px;" alt="David Duarte"/></a> | <a href="https://github.com/gabrielandrade-95"><img src="https://github.com/gabrielandrade-95.png" width="120px;" alt="Gabriel Andrade"/></a> | <a href="https://github.com/guihisham-dev"><img src="https://github.com/guihisham-dev.png" width="120px;" alt="Guilherme Hisham"/></a> | <a href="https://github.com/juantarciso1"><img src="https://github.com/juantarciso1.png" width="120px;" alt="Juan Tarcísio"/></a> | <a href="https://github.com/NyckolasJGF"><img src="https://github.com/NyckolasJGF.png" width="120px;" alt="Nyckolas José"/></a> |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **David Gabriel** | **David Duarte** | **Gabriel Andrade** | **Guilherme Hisham** | **Juan Tarcísio** | **Nyckolas José** |






