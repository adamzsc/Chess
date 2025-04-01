import pygame
import math

import board as b

class Square():
    def __init__(self,pos,row,column):
        self.pos = pos
        self.row = row
        self.column = column
        self.hitbox = pygame.Rect(self.column * 50, self.row * 50, 50, 50)

    def getColour(self):
        if self.pos % 2 == 0:
            return 'w'
        return 'b'

squares = []
for i in range(64):
    squares.append(Square(i,math.floor(i / 8),i % 8))

class Piece():
    def __init__(self):
        self.image = pygame.image.load(self.col.type + self.type + ".png").convert_alpha()
        self.moves = []
        self.legalMoves = []        

    def confirmMove(self,pos):
        x = b.Board.getPiece(pos)
        if x != None:
            if x.col != self.col:
                self.moves.append(b.Move(self.square.pos,pos))
            return False
        else:
            self.moves.append(b.Move(self.square.pos,pos))
            return True

    def findLegalMoves(self):          
        for x in self.moves:
            x.doMove(lookingAhead = 2)
            if not self.col.inCheck():
                self.legalMoves.append(x)
            x.undoMove()

    def getSquares(self):
        squares = []
        for x in self.moves:
            squares.append(x.newPos)
        return squares

    def getLegalSquares(self):
        squares = []
        for x in self.legalMoves:
            squares.append(x.newPos)
        return squares

class King(Piece):   
    def __init__(self,col,square):
        self.col = col
        self.square = square
        self.type = 'king'
        super().__init__()       

    def findMoves(self):
        relativePositions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for x in relativePositions:
            row = self.square.row + x[0]
            column = self.square.column + x[1]
            if 0 <= row <= 7 and 0 <= column <= 7:
                pos = b.Board.getPos(row,column)
                self.confirmMove(pos)               
        enemySquares = self.col.otherCol.getAllSquares()
        dir = self.col.castleDir
        if self.col.shortCastle:
            count = 0
            for i in range(4):
                pos = self.square.pos + (i * dir)
                piece = b.Board.getPiece(pos)
                if i < 3:
                    if i > 0:
                        if piece == None:
                            count += 1
                    if pos not in enemySquares:
                        count += 1
                else:
                    if piece != None:
                        if piece.type == 'rook':
                            count += 1
            if count == 6:
                self.moves.append(b.Move(self.square.pos,self.square.pos + (2 * dir)))

        if self.col.longCastle:
            count = 0
            for i in range(5):
                pos = self.square.pos - (i * dir)
                piece = b.Board.getPiece(pos)
                if i < 4:
                    if i > 0:
                        if piece == None:
                            count += 1
                    if i < 3:
                        if pos not in enemySquares:
                            count += 1
                else:
                    if piece != None:
                        if piece.type == 'rook':
                            count += 1
            if count == 7:
                self.moves.append(b.Move(self.square.pos,self.square.pos - (2 * dir)))

class Queen(Piece):
    def __init__(self,col,square):
        self.type = 'queen'
        self.col = col
        self.square = square
        super().__init__() 

    def findMoves(self):        
        row = self.square.row
        column = self.square.column          
        for i in range(1,8):
            if 0 <= (row + i) <= 7:
                pos = b.Board.getPos(row + i,column)
                if not self.confirmMove(pos):
                    break      
        for i in range(1,8):
            if 0 <= (row - i) <= 7:
                pos = b.Board.getPos(row - i,column)
                if not self.confirmMove(pos):
                    break
        for i in range(1,8):
            if 0 <= (column + i) <= 7:
                pos = b.Board.getPos(row,column + i)
                if not self.confirmMove(pos):
                    break          
        for i in range(1,8):                
            if 0 <= (column - i) <= 7:
                pos = b.Board.getPos(row,column - i)
                if not self.confirmMove(pos):
                    break  
        for i in range(1,8):
            if 0 <= (row + i) <= 7 and 0 <= (column + i) <= 7:
                pos = b.Board.getPos(row + i,column + i)
                if not self.confirmMove(pos):
                    break   
        for i in range(1,8):                
            if 0 <= (row + i) <= 7 and 0 <= (column - i) <= 7:
                pos = b.Board.getPos(row + i,column - i)
                if not self.confirmMove(pos):
                    break
        for i in range(1,8):
            if 0 <= (row - i) <= 7 and 0 <= (column + i) <= 7:
                pos = b.Board.getPos(row - i,column + i)
                if not self.confirmMove(pos):
                    break  
        for i in range(1,8):                
            if 0 <= (row - i) <= 7 and 0 <= (column - i) <= 7:
                pos = b.Board.getPos(row - i,column - i)
                if not self.confirmMove(pos):
                    break 

class Rook(Piece):
    def __init__(self,col,square):
        self.type = 'rook'
        self.col = col
        self.square = square
        super().__init__() 

    def findMoves(self):        
        row = self.square.row
        column = self.square.column          
        for i in range(1,8):
            if 0 <= (row + i) <= 7:
                pos = b.Board.getPos(row + i,column)
                if not self.confirmMove(pos):
                    break   
        for i in range(1,8):                
            if 0 <= (row - i) <= 7:
                pos = b.Board.getPos(row - i,column)
                if not self.confirmMove(pos):
                    break
        for i in range(1,8):
            if 0 <= (column + i) <= 7:
                pos = b.Board.getPos(row,column + i)
                if not self.confirmMove(pos):
                    break      
        for i in range(1,8):                
            if 0 <= (column - i) <= 7:
                pos = b.Board.getPos(row,column - i)
                if not self.confirmMove(pos):
                    break    

class Bishop(Piece):   
    def __init__(self,col,square):
        self.type = 'bishop'
        self.col = col
        self.square = square
        super().__init__() 

    def findMoves(self): 
        row = self.square.row
        column = self.square.column 
        for i in range(1,8):
            if 0 <= (row + i) <= 7 and 0 <= (column + i) <= 7:
                pos = b.Board.getPos(row + i,column + i)
                if not self.confirmMove(pos):
                    break   
        for i in range(1,8):                
            if 0 <= (row + i) <= 7 and 0 <= (column - i) <= 7:
                pos = b.Board.getPos(row + i,column - i)
                if not self.confirmMove(pos):
                    break
        for i in range(1,8):
            if 0 <= (row - i) <= 7 and 0 <= (column + i) <= 7:
                pos = b.Board.getPos(row - i,column + i)
                if not self.confirmMove(pos):
                    break    
        for i in range(1,8):                
            if 0 <= (row - i) <= 7 and 0 <= (column - i) <= 7:
                pos = b.Board.getPos(row - i,column - i)
                if not self.confirmMove(pos):
                    break             

class Knight(Piece):
    def __init__(self,col,square):
        self.type = 'knight'
        self.col = col
        self.square = square
        super().__init__() 

    def findMoves(self):
        relativePositions = [(-1,-2),(-1,2),(1,-2),(1,2),(-2,-1),(-2,1),(2,-1),(2,1)]
        for x in relativePositions:
            row = self.square.row + x[0]
            column = self.square.column + x[1]
            if 0 <= row <= 7 and 0 <= column <= 7:
                pos = b.Board.getPos(row,column)
                self.confirmMove(pos)

class Pawn(Piece):
    def __init__(self,col,square):
        self.enPassent = False
        self.type = 'pawn'
        self.col = col
        self.square = square  
        super().__init__() 

    def addPromotionMoves(self,oldPos,newPos):
        self.moves.append(b.Move(oldPos,newPos,self,Knight(self.col,squares[newPos])))
        self.moves.append(b.Move(oldPos,newPos,self,Bishop(self.col,squares[newPos])))
        self.moves.append(b.Move(oldPos,newPos,self,Rook(self.col,squares[newPos])))
        self.moves.append(b.Move(oldPos,newPos,self,Queen(self.col,squares[newPos])))

    def findMoves(self):
        M = self.col.multiplier    
        if self.square.row == self.col.promotionRow - M:
            promotion = True
        else:
            promotion = False
        if b.Board.getPiece(self.square.pos + (8 * M)) == None:
            if promotion:
                self.addPromotionMoves(self.square.pos,self.square.pos + (8 * M))
            else:
                self.moves.append(b.Move(self.square.pos,self.square.pos + (8 * M)))
            if self.square.row == self.col.pawnRow:
                if b.Board.getPiece(self.square.pos + (16 * M)) == None:  
                    self.moves.append(b.Move(self.square.pos,self.square.pos + (16 * M)))

        for i in range(1,-2,-2): #1,-1
            column = self.square.column + i
            targetPos = b.Board.getPos(self.square.row + M,column)
            for t in range(1,-1,-1): #1,0
                row = self.square.row + (t * M)
                if 0 <= row <= 7 and 0 <= column <= 7:
                    pos = b.Board.getPos(row,column)
                    piece = b.Board.getPiece(pos)
                    if piece != None: 
                        if piece.col != self.col:
                            if t == 1:
                                if promotion:
                                    self.addPromotionMoves(self.square.pos,targetPos)
                                else:
                                    self.moves.append(b.Move(self.square.pos,targetPos))
                                break
                            else:
                                if piece.type == 'pawn':
                                    if piece.enPassent:
                                        if promotion:
                                            self.addPromotionMoves(self.square.pos,targetPos)
                                        else:
                                            self.moves.append(b.Move(self.square.pos,targetPos))                    
