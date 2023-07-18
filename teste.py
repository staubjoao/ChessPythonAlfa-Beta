import pygame
import sys
from pygame.locals import *

# inicializa a biblioteca
pygame.init()
# obtém a superfície do jogo e define o tamanho da tela
DISPLAYSURF = pygame.display.set_mode((600, 450))

# vamos definir o título da janela do jogo
pygame.display.set_caption("Meu Jogo de Cartas")

# vamos definir a cor de fundo para a tela do jogo do Pyagem
BRANCO = (255, 255, 255)
DISPLAYSURF.fill(BRANCO)  # e definimos a cor para a superfície da janela

# e aqui nós entramos no loop do game
while True:
    # monitoramos os eventos
    for evento in pygame.event.get():
        # se o evento foi um pedido para sair
        if evento.type == QUIT:
            # fechamos a tela do jogo
            pygame.quit()
            # e saimos do programa
            sys.exit()

        # vamos verificar se o evento pygame.KEYDOWN foi disparado
        if evento.type == pygame.KEYDOWN:
            print("Uma tecla foi pressionada na janela de desenho")

# redesenha a tela continuamente
pygame.display.update()
