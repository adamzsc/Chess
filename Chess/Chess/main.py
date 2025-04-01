import pygame
import random
import math

import board as b
import state as s

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Calibri Body', 50)

WHITE = (255,255,255)

class Game:
    def __init__(self):
        self.bg = pygame.image.load("bg.jpg").convert()
        self.menuScreen = pygame.image.load("menu.png").convert_alpha()
        self.endGameScreen = pygame.image.load("endGame.png").convert_alpha()
        self.chooseColScreen = pygame.image.load("chooseCol.png").convert_alpha()
        self.promotionScreen = pygame.image.load("promotion.png").convert_alpha()
        self.but1 = pygame.Rect(100,150,200,75)
        self.but2 = pygame.Rect(100,275,200,75)

    def changeState(self,state,args = None):
        s.state = state
        s.args = args

    def stateManager(self):
        if s.state == 'menu':
            self.menu()
        elif s.state == 'chooseCol':
            self.chooseCol()
        elif s.state == 'userGo':
            self.userGo()
        elif s.state == 'botGo':
            self.botGo()
        elif s.state == 'endGame':
            self.endGame(s.args)
        else:
            self.promotion(s.args[0],s.args[1])

    def menu(self):
        buttonDown = self.getEvents()
        screen.blit(self.bg,[0,0])
        screen.blit(self.menuScreen,[0,0])
        if buttonDown:
            mousePos = pygame.mouse.get_pos()
            if self.but1.collidepoint(mousePos):
                s.state = 'chooseCol'
            elif self.but2.collidepoint(mousePos):
                pygame.quit()

    def chooseCol(self):
        buttonDown = self.getEvents()       
        screen.blit(self.bg,[0,0])
        screen.blit(self.chooseColScreen,[0,0])
        if buttonDown:
            mousePos = pygame.mouse.get_pos()
            if self.but1.collidepoint(mousePos):
                b.Board.generateBoard(b.White,b.Black)
                s.state = 'userGo'
            elif self.but2.collidepoint(mousePos):
                b.Board.generateBoard(b.Black,b.White)
                s.state = 'botGo'

    def promotion(self,piece,pos):
        b.Board.draw()
        screen.blit(self.promotionScreen,[0,0])
        pieces = ('knight','bishop','rook','queen')
        buttonDown = self.getEvents()
        if buttonDown:
            mousePos = pygame.mouse.get_pos()
            for i in range(4):
                hitbox = pygame.Rect(100,25 + (100 * i),200,50)
                if hitbox.collidepoint(mousePos):
                    for x in piece.legalMoves:
                        if x.newPos == pos and x.promotionPiece.type == pieces[i]:
                            self.changeState('botGo')
                            x.doMove()
                            break
                    break   

    def userGo(self):
        buttonDown = self.getEvents()
        if buttonDown:
            b.Board.checkSelect()
        b.Board.draw()

    def botGo(self):
        b.Board.draw()
        b.Board.findBotMove()

    def endGame(self,text):
        buttonDown = self.getEvents()        
        screen.blit(self.bg,[0,0])
        screen.blit(self.endGameScreen,[0,0])
        self.displayText(text,200,120)
        if buttonDown:
            mousePos = pygame.mouse.get_pos()
            if self.but1.collidepoint(mousePos):
                s.state = 'chooseCol'
            elif self.but2.collidepoint(mousePos):
                s.state = 'menu'

    def text_objects(self,text,font):
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()

    def displayText(self,text,x,y):
        largeText = pygame.font.Font('freesansbold.ttf',30)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = (x,y)
        screen.blit(TextSurf, TextRect)

    def getEvents(self):
        for event in pygame.event.get():     
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return True           
        return False

Game = Game()

if __name__ == '__main__':
    while True:           
        Game.stateManager()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
