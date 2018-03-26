#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Modulos
import pygame,sys
from pygame.locals import *
from random import randint

#Constantes
#Ancho de la pantalla en pixeles
WIDTH = 480
#Alto de la pantalla en pixeles
HEIGHT = 360

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
        self.imageLife = pygame.image.load('imagenes/life1.png')
        self.imageList = [self.imagePikachuN,self.imagePikachuLD,self.imagePikachuLU,self.imagePikachuRU,self.imagePikachuRD]
        
        self.imagePikachu = self.imageList[0] 

        #Retorna un rectangulo de la imagen
        self.rectLife = self.imageLife.get_rect()
        self.rect = self.imagePikachu.get_rect()
        
        #Posicionarlo en el centro
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT - 60
        
        #Numero de vidas
        self.life = 3

        #Velocidad
        self.speed = 20

        #Inicio movimiento
        self.movementTime = 0

        #Direccion
        self.direction = "None"

        #Tiempo de la animacion de movimiento en milisegunos
        self.animationTime = 100
    
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


    
    
    #Movimiento
    def __movement(self):
        if self.life > 0:
            if self.rect.left < 0:
                self.rect.left = WIDTH - self.rect.width
            elif self.rect.right > WIDTH:
                self.rect.right = 0 + self.rect.width

    def draw(self,screnn,time):
        #Posicionar las imagenes de la vida
        if self.life > 0:
            for pos in range(0,self.life):
                self.rectLife.left = (WIDTH - self.rectLife.width*(pos+1))
                self.rectLife.top = 0
                screnn.blit(self.imageLife,self.rectLife)

        if self.direction == "None":
            self.imagePikachu = self.imageList[0]
        elif self.direction == "Left" and time < self.movementTime + self.animationTime:
            self.imagePikachu = self.imageList[1]
        elif self.direction == "Left" and time > self.movementTime + self.animationTime and time < self.movementTime + self.animationTime*2:
            self.imagePikachu = self.imageList[2]
        elif self.direction == "Right" and time < self.movementTime + self.animationTime:
            self.imagePikachu = self.imageList[3]
        elif self.direction == "Right" and time > self.movementTime + self.animationTime and time < self.movementTime + self.animationTime*2:
            self.imagePikachu = self.imageList[4]
        else:
            self.direction == "None"
            self.imagePikachu = self.imageList[0]
        screnn.blit(self.imagePikachu,self.rect)

#Clase para los items
class Item(pygame.sprite.Sprite):
    def __init__(self,posx):
        pygame.sprite.Sprite.__init__(self)
        
        #Lista de items
        self.itemsNames = ['bomb','cake1','cookie','cupcake','pokeball']
        
        #Item aletorio
        self.itemRandom = randint(0,100) % 4

        #Imagen
        self.imagenItem = pygame.image.load('imagenes/Items/'+self.itemsNames[self.itemRandom]+'.png')

        #Rectangulo
        self.rect = self.imagenItem.get_rect()
        
        #Velocidad
        self.speed = 1

        self.rect.top = 0

        if posx == WIDTH:
            posx -= self.rect.width
        self.rect.left = posx

    #Moviemiento del item
    def trajectory (self):
        self.rect.top += self.speed

    def draw(self,screen):
        screen.blit(self.imagenItem,self.rect)
    

def main():
    #Creacion de una ventana
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    #Creacion de mensaje de la ventan
    pygame.display.set_caption("Juego ICC")

    #Cargar imagen de fondo
    startBackgroundImage = pygame.image.load('imagenes/background/intro_2.png')
    instructionsBackgroundImage = pygame.image.load('imagenes/background/instructions_1.png')
    backgroundImage = pygame.image.load('imagenes/background/game_1.png')
    
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
                    timeInstructions = pygame.time.get_ticks()

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

    #Rango de aparicion de items en milisegundos
    rangeItems = 500
    timeItems = 0
    #Dentro de un loop infinito
    while True:
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
                    if evento.key == K_LEFT:
                        player.leftMovement(time)
                    elif evento.key == K_RIGHT:
                        player.rightMovement(time)

        #Dibujando el fondo
        screen.blit(backgroundImage,(0,0))

        #Dibujar pikachu
        player.draw(screen,time)

        if len(itemList) > 0 :
            for it in itemList:
                it.draw(screen)
                it.trajectory()
                if it.rect.top > HEIGHT:
                    itemList.remove(it)
       
        #Actualizar la ventana
        pygame.display.update()
    
    return 0

if __name__ == '__main__':
    #Obligatorio para usarlo en cualquier modulo
    pygame.init()
    main()
