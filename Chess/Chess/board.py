import pygame
import random

import main as m
import pieces as p
import engine as e

selected = pygame.image.load("select.png").convert_alpha()
legalMove = pygame.image.load("legalMove.png").convert_alpha()
BoardImage = pygame.image.load("board.jpg").convert() 

class Colour:
    def __init__(self,type,castleDir):
        self.type = type
        self.castleDir = castleDir
        self.shortCastle = True
        self.longCastle = True
        self.pieces = [] 

    def findAllMoves(self):
        for x in self.pieces:
            x.moves = []
            x.findMoves()

    def getAllMoves(self):
        moves = []
        for x in self.pieces:
            moves += x.moves
        return moves

    def getAllSquares(self):
        squares = []
        for x in self.pieces:
            squares += x.getSquares()
        return squares

    def findAllLegalMoves(self):
        for x in self.pieces:
            x.legalMoves = []
            x.findLegalMoves()

    def getLegalMoves(self):
        moves = []
        for x in self.pieces:
            moves += x.legalMoves
        return moves

    def getAllLegalSquares(self):
        squares = []
        for x in self.pieces:
            squares += x.getLegalSquares()
        return squares

    def inCheck(self):
        for x in self.pieces:
            if x.type == 'king':
                if x.square.pos in self.otherCol.getAllSquares():
                    return True
                return False

White = Colour('w',1)
Black = Colour('b',-1)

class Move:
    def __init__(self,oldPos,newPos,promotionPawn = None,promotionPiece = None):
        self.oldPos = oldPos
        self.newPos = newPos
        self.promotionPawn = promotionPawn
        self.promotionPiece = promotionPiece
        self.disableShortCastle = False
        self.disableLongCastle = False       
        self.target = None

    def doMove(self,oldPos = None,newPos = None,castle = False,lookingAhead = 0):
        if oldPos == None:
            oldPos = self.oldPos
            newPos = self.newPos
        dif = oldPos - newPos   
        piece = Board.getPiece(oldPos)
        self.target = Board.getPiece(newPos)
        col = piece.col
        piece.square = p.squares[newPos]
        shortBool = col.shortCastle
        longBool = col.longCastle

        if piece.type == 'pawn':
            if self.target == None:
                if abs(dif) == 9 or abs(dif) == 7:
                    M = col.multiplier
                    pos = Board.getPos(piece.square.row - M,piece.square.column)
                    self.target = Board.getPiece(pos)
                elif abs(dif) == 16:
                    piece.enPassent = True

            if self.promotionPiece != None:
                Board.promotePiece(self.promotionPawn,self.promotionPiece)               

        elif piece.type == 'king':
            dir = col.castleDir
            if shortBool:
               col.shortCastle = False
               self.disableShortCastle = True
            if longBool:
                col.longCastle = False
                self.disableLongCastle = True             
            if dif == (2 * dir): #long castle
                self.doMove(piece.square.pos - (2 * dir),piece.square.pos + dir,True,lookingAhead)
            elif dif == (-2 * dir): #short castle
                self.doMove(piece.square.pos + dir,piece.square.pos - dir,True,lookingAhead)
            

        elif piece.type == 'rook':
            if piece.col.type == 'w':
                shortPositions = (7,63)
                longPositions = (0,56)               
            else:
                longPositions = (7,63)
                shortPositions = (0,56)
            if oldPos in shortPositions:                
                if shortBool:
                    col.shortCastle = False
                    self.disableShortCastle = True
            elif oldPos in longPositions:
                if longBool:
                    col.longCastle = False
                    self.disableLongCastle = True
            
        if self.target != None:
            col.otherCol.pieces.remove(self.target)
        if not castle:
            if lookingAhead == 0:
                Board.oldSquare = p.squares[oldPos]
                Board.newSquare = p.squares[newPos]
            Board.moves.append(self)
            Board.endMove(lookingAhead)

    def undoMove(self):           
        if self.promotionPiece != None:
            Board.promotePiece(self.promotionPiece,self.promotionPawn)
        dif = self.newPos - self.oldPos   
        piece = Board.getPiece(self.newPos)
        col = piece.col               
        piece.square = p.squares[self.oldPos]
        
        if self.target != None:
            col.otherCol.pieces.append(self.target)               

        if piece.type == 'king':
            dir = col.castleDir
            if dif == (2 * dir):
                otherPiece = Board.getPiece(piece.square.pos + dir)
                otherPiece.square = p.squares[piece.square.pos + (3 * dir)]
            elif dif == (-2 * dir):
                otherPiece = Board.getPiece(piece.square.pos - dir)
                otherPiece.square = p.squares[piece.square.pos - (4 * dir)]

        if self.disableShortCastle:
            piece.col.shortCastle = True
        if self.disableLongCastle:
            piece.col.longCastle = True     
        Board.turn = Board.turn.otherCol    
        del Board.moves[-1]

class Board:
    def __init__(self):     
        self.oldSquare = None
        self.newSquare = None
        self.selectedPiece = None
        self.moves = []

    def draw(self):
        m.screen.blit(BoardImage,[0,0])
        if self.oldSquare != None:
            pygame.draw.rect(m.screen,(115, 147, 179),self.oldSquare.hitbox)
        if self.newSquare != None:
            pygame.draw.rect(m.screen,(115, 147, 179),self.newSquare.hitbox)
        for x in Board.getAllPieces():      
            m.screen.blit(x.image,[x.square.column * 50,x.square.row * 50])
        if self.selectedPiece != None:
            m.screen.blit(selected,[self.selectedPiece.square.column * 50,self.selectedPiece.square.row * 50])
            for x in self.selectedPiece.legalMoves:
                square = p.squares[x.newPos]
                m.screen.blit(legalMove,[square.column * 50,square.row * 50])

    def checkSelect(self):       
        pos = pygame.mouse.get_pos()
        if self.turn == self.userCol:
            for x in p.squares:
                if x.hitbox.collidepoint(pos):
                    square = x
                    break
            piece = self.getPiece(square.pos)
            if self.selectedPiece == None:
                if piece != None and piece.col == self.userCol:
                    self.selectedPiece = piece
            else:
                for x in self.selectedPiece.legalMoves:
                    if x.newPos == square.pos:
                        if x.promotionPiece != None:
                            m.Game.changeState('promotion',(self.selectedPiece,square.pos))
                        else:
                            m.Game.changeState('botGo')                            
                            x.doMove() 
                        self.selectedPiece = None
                        break
                if piece != None:
                    if piece == self.selectedPiece:
                        self.selectedPiece = None
                    elif piece.col == self.userCol:
                        self.selectedPiece = piece   
                else:
                    self.selectedPiece = None   
                    
    def promotePiece(self,oldPiece,newPiece):
        col = oldPiece.col
        col.pieces.remove(oldPiece)
        col.pieces.append(newPiece)

    def endMove(self,lookingAhead):    
        if lookingAhead <= 1:
            self.turn.findAllMoves()
        self.turn = self.turn.otherCol
        self.turn.findAllMoves()
        if lookingAhead <= 1:
            self.turn.otherCol.findAllMoves()
            self.turn.findAllLegalMoves()
            for x in self.turn.pieces:
                if x.type == 'pawn':
                    x.enPassent = False
            if lookingAhead == 0:
                x = len(self.turn.getLegalMoves())
                if x == 0:               
                    if self.turn.inCheck():
                        if self.turn == self.userCol:
                            text = 'YOU LOST'
                        else:
                            text = 'YOU WIN'
                    else:
                        text = 'DRAW'
                    m.Game.changeState('endGame',text)
            
    def findBotMove(self):
        move = e.Engine.getBestMove()
        m.Game.changeState('userGo')
        move.doMove()  
    
    def getPos(self,row,column):
        return (row * 8) + column

    def getAllPieces(self):
        return (White.pieces + Black.pieces)   

    def getPiece(self,pos):
        for x in self.getAllPieces():
            if x.square.pos == pos:
                return x
        return None          
        
    def generateBoard(self,uCol,bCol):
        self.turn = White 
        self.userCol = uCol
        self.botCol = bCol
        self.userCol.pawnRow = 6
        self.userCol.promotionRow = 0
        self.userCol.multiplier = -1
        self.userCol.otherCol = self.botCol
        self.botCol.pawnRow = 1
        self.botCol.promotionRow = 7
        self.botCol.multiplier = 1
        self.botCol.otherCol = self.userCol
        setup =    [p.Rook,p.Knight,p.Bishop,p.Queen,p.King,p.Bishop,p.Knight,p.Rook,
                    p.Pawn,p.Pawn  ,p.Pawn  ,p.Pawn ,p.Pawn,p.Pawn  ,p.Pawn  ,p.Pawn,
                    None  ,None    ,None    ,None   ,None  ,None    ,None    ,None  ,
                    None  ,None    ,None    ,None   ,None  ,None    ,None    ,None  ,
                    None  ,None    ,None    ,None   ,None  ,None    ,None    ,None  ,
                    None  ,None    ,None    ,None   ,None  ,None    ,None    ,None  ,
                    p.Pawn,p.Pawn  ,p.Pawn  ,p.Pawn ,p.Pawn,p.Pawn  ,p.Pawn  ,p.Pawn,
                    p.Rook,p.Knight,p.Bishop,p.Queen,p.King,p.Bishop,p.Knight,p.Rook,]
        if uCol.type == 'b':
            setup.reverse()
        self.userCol.pieces,self.botCol.pieces = [],[]
        self.userCol.shortCastle,self.botCol.shortCastle = True,True
        self.userCol.longCastle,self.botCol.longCastle = True,True
        self.oldSquare,self.newSquare = None,None
        for i in range(64):            
            if setup[i] != None:
                if i <= 15:
                    piece = setup[i](self.botCol,p.squares[i])
                else:
                    piece = setup[i](self.userCol,p.squares[i])
                piece.col.pieces.append(piece)
        self.turn.findAllMoves()
        self.turn.findAllLegalMoves()
Board = Board()
