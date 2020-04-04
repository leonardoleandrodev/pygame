import pygame
from pygame.locals import *
import time
import random
LARGURA_JANELA = 1024
ALTURA_JANELA = 768
FRAMES = 59
run = True
fm = 0
db = ""
pause = False
class Jogador:
    tamanho = [30,90]
    posX = 0#posicao largura
    posY = 0#posicao altura
    pontos = 0
    
    cor = (255,0,0)
    velocidade=20
    def moveUp(self):
        if self.posY > 0:
            self.posY -= self.velocidade
        
    def moveDown(self):
        if self.posY < (ALTURA_JANELA-self.tamanho[1]) :
            self.posY += self.velocidade

    def desenhar(self):
        global screen
        pygame.draw.rect(screen, self.cor, [self.posX, self.posY, self.tamanho[0], self.tamanho[1]])

class Bola:
    posX = 0#posicao largura
    posY = 0#posicao altura    
    tamanho = [20,20]
    cor = (255,255,0)
    moveLeft = True
    moveUp = True
    velocidade=2
    
    def posInicial(self):
        self.posX = (LARGURA_JANELA/2)
        self.posY = (ALTURA_JANELA/2)
        self.moveLeft = bool(random.getrandbits(1))
        self.moveUp = bool(random.getrandbits(1))
        self.velocidade=2
    def move(self):

        if self.moveUp:
            self.posY -= self.velocidade
        else:
            self.posY += self.velocidade
        if self.moveLeft:
            self.posX += self.velocidade
        else:
            self.posX -= self.velocidade
    def speedUp(self):
        if self.velocidade < 60:
            self.velocidade+=0.2
    def desenhar(self):
        global screen
        pygame.draw.rect(screen, self.cor, [self.posX, self.posY, self.tamanho[0], self.tamanho[1]])

    def colisionWall(self):
        global jg1,jg2
        if self.posX < 0:
            self.posInicial()
            self.moveLeft = not self.moveLeft
            jg2.pontos +=1
        elif (self.posX+self.tamanho[0]) > LARGURA_JANELA:
            self.posInicial()
            self.moveLeft = not self.moveLeft
            jg1.pontos +=1
        elif self.posY < 0:
            self.moveUp = not self.moveUp
        elif (self.posY+self.tamanho[1]) > ALTURA_JANELA:
            self.moveUp = not self.moveUp
        self.move()
            


jg1 = Jogador()
jg1.cor = (255,0,0)
jg1.posX = 10
jg1.posY = (ALTURA_JANELA/2)-(jg1.tamanho[1]/2)


jg2 = Jogador()
jg2.cor = (255,0,255)
jg2.posX = (LARGURA_JANELA-jg2.tamanho[0]) -10
jg2.posY = (ALTURA_JANELA/2)-(jg2.tamanho[1]/2)


bola = Bola()
bola.cor = (255,100,0)
bola.posInicial()
def debug(msg):
    global fontDebug
    text = fontDebug.render(msg, True, [10,10,255])
    screen.blit(text, [10,  ALTURA_JANELA-30])

def painel():
    global fontPainel
    txt = "PLAYER 1: {}   VS   PLAYER 2: {}".format(jg1.pontos,jg2.pontos)
    text = fontPainel.render(txt , True, [10,200,10])
    screen.blit(text, [5,10])
def atualizar():
    global screen,run,jg1,jg2,bola,db,pause
    bola.colisionWall()
    inputs()
    if bola.posY+bola.tamanho[1] > jg1.posY and bola.posY < jg1.posY+jg1.tamanho[1]:
        if bola.posX < jg1.posX+jg1.tamanho[0] and bola.posX+bola.tamanho[0] > jg1.posX:
            bola.moveLeft = not bola.moveLeft
            bola.posX+=7
            bola.speedUp()
            db = clock,bola.posX,bola.posY,jg1.posY,jg1.posY
    if bola.posY+bola.tamanho[1] > jg2.posY and bola.posY < jg2.posY+jg1.tamanho[1]:
        if bola.posX+bola.tamanho[0] > jg2.posX and bola.posX < jg2.posX+jg2.tamanho[0]:
            bola.moveLeft = not bola.moveLeft
            bola.posX-=7
            bola.speedUp()
            db = clock,bola.posX,bola.posY,jg2.posY,jg2.posY

    jg1.velocidade = bola.velocidade*2
    jg2.velocidade = bola.velocidade*2
    bola.move()
    debug("{}".format(db))


def inputs(): 
    global jg1,jg2,run,pause       
    keys = pygame.key.get_pressed()
    if keys[K_p]:
        pause = not pause
    if keys[K_w]:
        jg1.moveUp()
    if keys[K_s]:
        jg1.moveDown()

    if keys[K_UP]:
        jg2.moveUp()

    if keys[K_DOWN]:
        jg2.moveDown()
        
    if keys[K_ESCAPE] or keys[K_q]:
        run = False



def desenhar():
    jg1.desenhar()
    jg2.desenhar()
    bola.desenhar()
    painel()
    
    

pygame.init()
fontPainel = pygame.font.SysFont("tahoma", 18)
fontDebug = pygame.font.SysFont("tahoma", 15)
clock = pygame.time.Clock()
#font = pygame.font.SysFont("comicsansms", 72)
screen = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))


while run : 
    fm = clock
    screen.fill([0,0,0])
    atualizar()
    desenhar()
    clock.tick(FRAMES)    
    pygame.display.flip()
    pygame.event.pump()

    
