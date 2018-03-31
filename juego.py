#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Modulos
import pygame,sys
from pygame.locals import *
from random import randint

#Constantes
#Ancho de la pantalla en pixeles
WIDTH = 960#480
#Alto de la pantalla en pixeles
HEIGHT = 720#360

#Clase para el personaje Pikachu
class Pikachu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #Imagenes
        self.imagePikachuN = pygame.image.load('imagenes/Pikachu/pika_N.png')
        self.imagePikachuLU = pygame.image.load('imagenes/Pikachu/pika_LU.png')
        self.imagePikachuLD = pygame.image.load('imagenes/Pikachu/pika_LD.png')
        self.imagePikachuRU = pygame.image.load('imagenes/Pikachu/pika_RU.png')
        self.imagePikachuRD = pygame.image.load('imagenes/Pikachu/pika_RD.png')
        self.imagePikachuJL = pygame.image.load('imagenes/Pikachu/pika_JL.png')
        self.imagePikachuJR = pygame.image.load('imagenes/Pikachu/pika_JR.png')
        self.imagePikachuSad = pygame.image.load('imagenes/Pikachu/pika_sad.png')
        self.imageLife = pygame.image.load('imagenes/life1.png')
        self.imageScore = pygame.image.load('imagenes/score.png')
        self.imageList = [self.imagePikachuN,self.imagePikachuLD,self.imagePikachuLU,self.imagePikachuRU,self.imagePikachuRD,self.imagePikachuJL,
        self.imagePikachuJR,self.imagePikachuSad]
        
        self.imagePikachu = self.imageList[0] 

        #Retorna un rectangulo de la imagen
        self.rectLife = self.imageLife.get_rect()
        self.rect = self.imagePikachu.get_rect()
        self.rectScore = self.imageScore.get_rect()
        
        #Velocidad
        self.speed = 50#20

        #Posicionarlo en el centro
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT - 60
        self.base = self.rect.top
        self.maxHeight = self.base  - self.speed * 7
        
        #Numero de vidas
        self.life = 3
        
        #Puntaje
        self.score = 0
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

        #Inicio movimiento
        self.movementTime = 0

        #Direccion
        self.direction = "None"

        #Tiempo de la animacion de movimiento en milisegunos
        self.animationTime = 200#100
    
    def gameOver(self):
        self.direction = "None"
        self.rect.centerx = WIDTH/2 + 100
        self.rect.centery = HEIGHT - 60
        self.rectScore.centerx = self.rect.centerx + 75
        self.rectScore.centery = self.rect.centery - 75


    def leftMovement(self,time):
        self.rect.left -= self.speed
        self.movementTime = time
        self.direction = "Left"
        self.__movement()

    
    def rightMovement(self,time):
        self.rect.right += self.speed
        self.movementTime = time
        self.direction = "Right"
        self.__movement()


    def verticalJump(self,time):
        self.direction = "Jump"
        self.movementTime = time
    
    def leftJump(self,time):
        self.direction = "leftJump"
        print("hey")
        self.movementTime = time
    
    def rightJump(self,time):
        self.direction = "rightJump"
        self.movementTime = time

    def jumpBehavior(self,orintation):
        if orintation == "up" and self.rect.top > self.maxHeight:
            self.rect.top -= self.speed
        elif orintation == "down" and self.rect.top < self.base:
            self.rect.top += self.speed
        if self.rect.top == self.base:
            self.direction = "None"
        print("JUMP",orintation,self.rect.top)

    def leftJumpBehavior(self,orintation):
        if orintation == "up" and self.rect.top > self.maxHeight:
            self.rect.top -= self.speed
            self.rect.left -= self.speed/2
        elif orintation == "down" and self.rect.top < self.base:
            self.rect.top += self.speed
            self.rect.left -= self.speed/2
        if self.rect.top == self.base:
            self.direction = "None"
        self.__movement()
        print("JUMPL",orintation,self.rect.top,self.rect.left)

    def rightJumpBehavior(self,orintation):
        if orintation == "up" and self.rect.top > self.maxHeight:
            self.rect.top -= self.speed
            self.rect.left += self.speed/2
        elif orintation == "down" and self.rect.top < self.base:
            self.rect.top += self.speed
            self.rect.left += self.speed/2
        if self.rect.top == self.base:
            self.direction = "None"
        self.__movement()
        print("JUMPR",orintation,self.rect.top,self.rect.left)

    #Movimiento
    def __movement(self):
        if self.life > 0:
            if self.rect.left < 0:
                self.rect.left = WIDTH - self.rect.width
            elif self.rect.right > WIDTH:
                self.rect.right = 0 + self.rect.width
            elif self.rect.centery != HEIGHT - 60 and not(self.direction != "jump"  or self.direction != "rightJump" or self.direction != "leftJump"):
                self.rect.centery = HEIGHT - 60

    def draw(self,screnn,time,showScore = False):
        #Posicionar las imagenes de la vida
        if self.life > 0:
            for pos in range(0,self.life):
                self.rectLife.left = (WIDTH - self.rectLife.width*(pos+1))
                self.rectLife.top = 0
                screnn.blit(self.imageLife,self.rectLife)

        if self.direction == "None" and self.life > 0:
            self.imagePikachu = self.imageList[0]
        elif self.direction == "None" and self.life < 1:
            self.imagePikachu = self.imageList[7]
        elif self.direction == "Left" and time < self.movementTime + self.animationTime:
            self.imagePikachu = self.imageList[1]
        elif self.direction == "Left" and time > self.movementTime + self.animationTime and time < self.movementTime + self.animationTime*2:
            self.imagePikachu = self.imageList[2]
        elif self.direction == "Right" and time < self.movementTime + self.animationTime:
            self.imagePikachu = self.imageList[3]
        elif self.direction == "Right" and time > self.movementTime + self.animationTime and time < self.movementTime + self.animationTime*2:
            self.imagePikachu = self.imageList[4]
        elif self.direction == "Jump" and time < self.movementTime + self.animationTime:
            self.jumpBehavior("up")
        elif self.direction == "Jump" and time > self.movementTime + self.animationTime and time < self.movementTime + self.animationTime*3:
            self.jumpBehavior("down")
        elif self.direction == "leftJump" and time < self.movementTime + self.animationTime:
            self.leftJumpBehavior("up")
            self.imagePikachu = self.imageList[5]
        elif self.direction == "leftJump" and time > self.movementTime + self.animationTime and time < self.movementTime + self.animationTime*3:
            self.leftJumpBehavior("down")
            self.imagePikachu = self.imageList[5]
        elif self.direction == "rightJump" and time < self.movementTime + self.animationTime:
            self.rightJumpBehavior("up")
            self.imagePikachu = self.imageList[6]
        elif self.direction == "rightJump" and time > self.movementTime + self.animationTime and time < self.movementTime + self.animationTime*3:
            self.rightJumpBehavior("down")
            self.imagePikachu = self.imageList[6]
        else:
            self.direction == "None"
            self.imagePikachu = self.imageList[0]
        if showScore == True:
            self.rectScore.centerx = self.rect.centerx + 75
            self.rectScore.centery = self.rect.centery - 75
            finalScore = str(self.score)
            textsurface = self.myfont.render(finalScore, False, (0, 0, 0))
            x = self.rectScore.centerx + 2
            y = self.rectScore.centery - 17
            screnn.blit(self.imageScore,self.rectScore)
            screnn.blit(textsurface,(x,y))
        screnn.blit(self.imagePikachu,self.rect)

#Clase para los items
class Item(pygame.sprite.Sprite):
    def __init__(self,posx):
        pygame.sprite.Sprite.__init__(self)
        
        #Lista de items
        self.itemsNames = ['bomb','cake1','cookie','cupcake','pokeball']
        
        #Item aletorio
        self.itemRandom = randint(0,100) % 5

        #Tipo item
        if self.itemsNames[self.itemRandom] in ['cake1','cookie','cupcake']:
            self.itemType = 1
        else:
            self.itemType = -1

        #Imagen
        self.imagenItem = pygame.image.load('imagenes/Items/'+self.itemsNames[self.itemRandom]+'.png')

        #Rectangulo
        self.rect = self.imagenItem.get_rect()
        
        #Velocidad
        self.speed = 2

        self.rect.top = 0

        if posx == WIDTH:
            posx -= self.rect.width
        self.rect.left = posx

    #Moviemiento del item
    def trajectory (self):
        self.rect.top += self.speed
    
    #Retornar el tipo
    def getType(self):
        return self.itemType

    def isCollition(self,rect1):
        return self.rect.colliderect(rect1)

    def draw(self,screen):
        screen.blit(self.imagenItem,self.rect)
    

def main():
    #Creacion de una ventana
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    #Creacion de mensaje de la ventan
    pygame.display.set_caption("Juego ICC")

    #Cargar imagen de fondo
    startBackgroundImage = pygame.image.load('imagenes/background/intro_2.png')
    instructionsBackgroundImage = pygame.image.load('imagenes/background/instructions_1_grande.png')
    backgroundImage = pygame.image.load('imagenes/background/game_1_grande.png')
    
    #Cargar sonidos y audios
    soundInit = pygame.mixer.Sound('audios/piKAchu_cute.wav')
    soundCoin = pygame.mixer.Sound('audios/coin.wav')
    soundBomb = pygame.mixer.Sound('audios/pika_dead.wav')
    pygame.mixer.music.load('audios/cycling_cut.mp3')
    
    

    stillStart = True
    instructions = False
    timeInstructions = None
    while stillStart:
        #Dibujando el fondo
        if instructions ==  False:
            screen.blit(startBackgroundImage,(0,0))
        else:
            screen.blit(instructionsBackgroundImage,(0,0))
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == K_SPACE:
                    instructions = True
                    soundInit.play()
                    timeInstructions = pygame.time.get_ticks()
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()

        if timeInstructions != None:
            if pygame.time.get_ticks() > timeInstructions + 3000:
                stillStart = False
        #Actualizar la ventana
        pygame.display.update()



    player = Pikachu()

    itemList = []

    #Para saber si ya gano o perdio
    inGame = True

    #Reloj para... 
    clock = pygame.time.Clock()

    #Iniciando musica
    pygame.mixer.music.play(-1)

    #Rango de aparicion de items en milisegundos
    rangeItems = 500
    timeItems = 0
    #Dentro de un loop infinito
    while player.life > 0:
        #Numero de frames por segundo
        clock.tick(60)
        #Obtener el tiempo
        time = pygame.time.get_ticks()
        
        if time > timeItems + rangeItems:
            itemTemp = Item(randint(0,WIDTH))
            itemList.append(itemTemp)
            timeItems = time

        #Comprobar eventos
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if inGame == True:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == K_UP and player.direction == "Left":
                        player.leftJump(time)
                    elif evento.key == K_UP and player.direction == "Right":
                        player.rightJump(time)
                    elif evento.key == K_UP and player.direction != "Jump":
                        player.verticalJump(time)
                    elif evento.key == K_LEFT and player.direction != "Jump":
                        player.leftMovement(time)
                    elif evento.key == K_RIGHT and player.direction != "Jump":
                        player.rightMovement(time)
        #Dibujando el fondo
        screen.blit(backgroundImage,(0,0))
        
        
        showScore = True
        if len(itemList) > 0 :
            for it in itemList:
                it.draw(screen)
                it.trajectory()
                if it.rect.top > HEIGHT:
                    itemList.remove(it)
                else:
                    if it.isCollition(player.rect) == True:
                        if it.getType() == 1:
                            player.score += 1
                            soundCoin.play()
                            #showScore = True
                            print("score:",player.score)
                            print("item",it.itemsNames[it.itemRandom])
                        else:
                            player.life -= 1
                            showScore = False
                            soundBomb.play()
                            print("life:",player.life)
                            print("item",it.itemsNames[it.itemRandom])
                        itemList.remove(it)        
       
        #Dibujar pikachu
        player.draw(screen,time,showScore)
        #Actualizar la ventana
        pygame.display.update()
    
    del(itemList)
    player.gameOver()
    gameOverBI = pygame.image.load('imagenes/background/finalscore_grande.png')
    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
        #Dibujando el fondo
        screen.blit(gameOverBI,(0,0))

        #Dibujar pikachu
        player.draw(screen,time,True)

        #Actualizar la ventana
        pygame.display.update()



    
    return 0

if __name__ == '__main__':
    #Obligatorio para usarlo en cualquier modulo
    pygame.init()
    main()
