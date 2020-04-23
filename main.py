import pygame
from pygame.locals import *
import time
import random
from playsound import playsound

LARGURA_JANELA = 1024
ALTURA_JANELA = 768
FRAMES = 60
run = True
fm = 0
db = ""
pause = False
timeBall = 0
lstBola = []
class Jogador:
    tamanho = [30,200]
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
        self.posY = random.randint(0,ALTURA_JANELA)
        self.moveLeft = bool(random.getrandbits(1))
        self.moveUp = bool(random.getrandbits(1))
        self.velocidade=2
    def move(self):

        if self.moveUp == True:
            self.posY -= self.velocidade
        elif self.moveUp == False:
            self.posY += self.velocidade
        else:
            self.posY += 0
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
           # sound2.play()
        elif (self.posX+self.tamanho[0]) > LARGURA_JANELA:
            self.posInicial()
            self.moveLeft = not self.moveLeft
            jg1.pontos +=1
            #sound2.play()
        elif self.posY < 0:
            self.moveUp = not self.moveUp
            #sound1.play()
        elif (self.posY+self.tamanho[1]) > ALTURA_JANELA:
            self.moveUp = not self.moveUp
            #sound1.play()
        self.move()
            
pygame.mixer.pre_init(44100,-16,1, 1024 * 5)
pygame.mixer.init()
pygame.mixer.set_num_channels(10) 
sound1 = pygame.mixer.Sound('sound1.wav')
sound2 = pygame.mixer.Sound('sound2.wav')

jg1 = Jogador()
jg1.cor = (255,0,0)
jg1.posX = 10
jg1.posY = (ALTURA_JANELA/2)-(jg1.tamanho[1]/2)


jg2 = Jogador()
jg2.cor = (255,0,255)
jg2.posX = (LARGURA_JANELA-jg2.tamanho[0]) -10
jg2.posY = (ALTURA_JANELA/2)-(jg2.tamanho[1]/2)
for i in range(300) :
    bola = Bola()
    bola.cor = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
    bola.posInicial()
    lstBola.append(bola)



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
    for b in lstBola:
        b.colisionWall()

    inputs()
    for b in lstBola:
        b.desenhar()
        if b.posY+b.tamanho[1] > jg1.posY and b.posY < jg1.posY+jg1.tamanho[1]:
            if b.posX < jg1.posX+jg1.tamanho[0] and b.posX+b.tamanho[0] > jg1.posX:
                b.moveLeft = not b.moveLeft                
                b.posX+=7
                b.speedUp()
                db = clock,b.posX,b.posY,jg1.posY,jg1.posY
                jg1.pontos-=2
                if b.posY+b.tamanho[1] < jg1.posY+(jg1.tamanho[1]*0.20):
                    b.moveUp = True
                elif b.posY > jg1.posY+(jg1.tamanho[1]*0.80) :
                    b.moveUp = False
                else:
                    b.moveUp = None

                
                #sound1.play()
        if b.posY+b.tamanho[1] > jg2.posY and b.posY < jg2.posY+jg1.tamanho[1]:
            if b.posX+b.tamanho[0] > jg2.posX and b.posX < jg2.posX+jg2.tamanho[0]:
                b.moveLeft = not b.moveLeft
                b.posX-=7
                b.speedUp()
                db = clock,b.posX,b.posY,jg2.posY,jg2.posY
                jg2.pontos-=2
                if b.posY+b.tamanho[1] < jg2.posY+(jg2.tamanho[1]*0.20):
                    b.moveUp = True
                elif b.posY > jg2.posY+(jg2.tamanho[1]*0.80) :
                    b.moveUp = False
                else:
                    b.moveUp = None
                #sound1.play()

    jg1.velocidade = bola.velocidade*2
    jg2.velocidade = bola.velocidade*2
    for b in lstBola:
        b.move()
    debug("{}".format(db))


def inputs(): 
    global jg1,jg2,run,pause,timeBall      
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

    if keys[K_n]:
        print(len(lstBola),timeBall)
        timeBall += 1
        if clock.get_fps() > 57:
            bola = Bola()
            bola.cor = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
            bola.posInicial()
            if timeBall > 20:
                lstBola.append(bola)
                timeBall = 0
        else:
            del lstBola[0]

def desenhar():
    jg1.desenhar()
    jg2.desenhar()
    for b in lstBola:
        b.desenhar()
    painel()
    if clock.get_fps() < 57 and  len(lstBola) > 200:
        del lstBola[0]

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

    
