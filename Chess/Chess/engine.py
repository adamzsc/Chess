import random

import board as b

class Engine:
    def __init__(self):       
        self.materialCounter = {
            'pawn'   : 1,
            'knight' : 3,
            'bishop' : 3,
            'rook'   : 5,
            'queen'  : 9,
            'king'   : 200
            }
        self.maxDepth = 1
        self.materialWeight = 1

    def getBestMove(self):     
        self.finalNodes = []
        self.finalMoves = []
        startNode = Node(0,None,None)
        startNode.getChildren()
        for x in self.finalNodes:
            if x.value == startNode.value:
                self.finalMoves.append(x.move)
        return random.choice(self.finalMoves)

    def evaluatePosition(self):
        count = 0
        count += self.evalMaterial() * self.materialWeight
        return count
        
    def evalMaterial(self):
        count = 0
        for x in b.Board.getAllPieces():
            count += self.materialCounter[x.type] * x.col.castleDir #castleDir same value as material multiplier
        return count

Engine = Engine()

class Node:
    def __init__(self,depth,parent,move):
        self.depth = depth
        self.parent = parent
        self.move = move
        self.children = []
        self.value = None

    def getChildren(self):
        if self.depth > 0:
            if self.depth == Engine.maxDepth:
                self.move.doMove(lookingAhead = 2)
            else:
                self.move.doMove(lookingAhead = 1)
        if self.depth < Engine.maxDepth:            
            for x in b.Board.turn.getLegalMoves():
                self.children.append(Node(self.depth + 1,self,x))          
            self.goToChild()

        else:
            self.value = Engine.evaluatePosition()
            self.goToParent()
            
    def updateValue(self,value):
        if value != None:
            if self.value == None:
                self.value = value
            else:
                if b.Board.turn.type == 'w':
                    if value > self.value:
                        self.value = value
                else:
                    if value < self.value:
                        self.value = value

    def goToChild(self):
        if len(self.children) > 0:
            self.children[0].getChildren()
        else:
            self.goToParent()
                       
    def goToParent(self):
        if self.depth > 0:
            self.move.undoMove()            
            self.parent.updateValue(self.value)
            if self.depth == 1:
                Engine.finalNodes.append(self)
            self.parent.children.remove(self)
            self.parent.goToChild()
    