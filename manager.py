import pygame

pygame.mixer.init()
moveSound = pygame.mixer.Sound('pieceMoved.wav')
castleSound = pygame.mixer.Sound('Castle.wav')

class Manager:
    def __init__(self):
        self.grid = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr'],
        ]
        self.piece = {
            'wk' : pygame.image.load('pieces/white-king.png'),
            'wq' : pygame.image.load('pieces/white-queen.png'),
            'wb' : pygame.image.load('pieces/white-bishop.png'),
            'wn' : pygame.image.load('pieces/white-knight.png'),
            'wr' : pygame.image.load('pieces/white-rook.png'),
            'wp' : pygame.image.load('pieces/white-pawn.png'),
            'bk' : pygame.image.load('pieces/black-king.png'),
            'bq' : pygame.image.load('pieces/black-queen.png'),
            'bb' : pygame.image.load('pieces/black-bishop.png'),
            'bn' : pygame.image.load('pieces/black-knight.png'),
            'br' : pygame.image.load('pieces/black-rook.png'),
            'bp' : pygame.image.load('pieces/black-pawn.png'),
        }
        self.selected = None
        self.validMoves = []
        self.whiteTurn = True
        self.whiteRooksMoved = 0
        self.whiteKingMoved = False
        self.blackRooksMoved = 0
        self.blackKingMoved = False
            
    def draw(self, screen):
        #if self.whiteTurn:
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] != ' ':
                    img = pygame.transform.scale(self.piece[self.grid[row][col]], (64, 64))
                    screen.blit(img, (col*64, row*64))
        # else:
        #     for row in range(len(self.grid)):
        #         for col in range(len(self.grid[row])):
        #             if self.grid[row][col] != ' ':
        #                 img = pygame.transform.scale(self.piece[self.grid[row][col]], (64, 64))
        #                 screen.blit(img, ((7-col)*64, (7-row)*64))
    
    def returnQueenMoves(self, screen, row, col):
        if self.grid[row][col][0] == 'w':
            color = 'w'
        else:
            color = 'b'
        moves = []
        moves.extend(self.returnAxis(row+1, col+1, 1, 1, color))
        moves.extend(self.returnAxis(row+1, col-1, 1, -1, color))
        moves.extend(self.returnAxis(row-1, col-1, -1, -1, color))
        moves.extend(self.returnAxis(row-1, col+1, -1, 1, color))
        moves.extend(self.returnAxis(row+1, col, 1, 0, color))
        moves.extend(self.returnAxis(row-1, col, -1, 0, color))
        moves.extend(self.returnAxis(row, col-1, 0, -1, color))
        moves.extend(self.returnAxis(row, col+1, 0, 1, color))

        for pos in moves:
            pygame.draw.rect(screen, (0, 200, 0), [pos[1]*64, pos[0]*64, 64, 64])
        
        self.validMoves = moves
    
    def returnRookMoves(self, screen, row, col):
        if self.grid[row][col][0] == 'w':
            color = 'w'
        else:
            color = 'b'
        moves = []
        moves.extend(self.returnAxis(row+1, col, 1, 0, color))
        moves.extend(self.returnAxis(row-1, col, -1, 0, color))
        moves.extend(self.returnAxis(row, col-1, 0, -1, color))
        moves.extend(self.returnAxis(row, col+1, 0, 1, color))

        for pos in moves:
            pygame.draw.rect(screen, (0, 200, 0), [pos[1]*64, pos[0]*64, 64, 64])
        
        self.validMoves = moves
    
    def returnBishopMoves(self, screen, row, col):
        if self.grid[row][col][0] == 'w':
            color = 'w'
        else:
            color = 'b'

        moves = []
        moves.extend(self.returnAxis(row+1, col+1, 1, 1, color))
        moves.extend(self.returnAxis(row+1, col-1, 1, -1, color))
        moves.extend(self.returnAxis(row-1, col-1, -1, -1, color))
        moves.extend(self.returnAxis(row-1, col+1, -1, 1, color))

        for pos in moves:
            pygame.draw.rect(screen, (0, 200, 0), [pos[1]*64, pos[0]*64, 64, 64])
        
        self.validMoves = moves
        

    def returnPawnMoves(self, screen, row, col):
        moves = []
        if self.grid[row][col][0] == 'w':
            color = 'w'
            rowDir = -1
        else:
            color = 'b'
            rowDir = 1
        
        if self.grid[row+rowDir][col] == ' ':
            moves.append((row+rowDir, col))
        if col < len(self.grid) - 2:
            if self.grid[row+rowDir][col+1] != ' ' and self.grid[row+rowDir][col+1][0] != color:
                moves.append((row+rowDir, col+1))
        if col > 1:
            if self.grid[row+rowDir][col-1] != ' ' and self.grid[row+rowDir][col-1][0] != color:
                moves.append((row+rowDir, col-1))

        # Special rules
        if row == 1 and color == 'b':
            if self.grid[row+rowDir*2][col] == ' ':
                moves.append((row+rowDir*2, col))
        if row == 6 and color == 'w': 
            if self.grid[row+rowDir*2][col] == ' ':
                moves.append((row+rowDir*2, col))
        
        for pos in moves:
            pygame.draw.rect(screen, (0, 200, 0), [pos[1]*64, pos[0]*64, 64, 64])
        
        self.validMoves = moves

    def returnKnightMoves(self, screen, row, col):
        # Thanks chat GPT :D
        moves = []
        if self.grid[row][col][0] == 'w':
            color = 'w'
            rowDir = -1
        else:
            color = 'b'
            rowDir = 1

        # Knight Moves
        knight_moves = [(-1, -2), (-2, -1), (-2, 1), (-1, 2),
                        (1, -2), (2, -1), (2, 1), (1, 2)]

        for move in knight_moves:
            newRow = row + move[0]
            newCol = col + move[1]
            if 0 <= newRow < 8 and 0 <= newCol < 8:
                if self.grid[newRow][newCol][0] != color:
                    moves.append((newRow, newCol))
        
        for pos in moves:
            pygame.draw.rect(screen, (0, 200, 0), [pos[1]*64, pos[0]*64, 64, 64])
        
        self.validMoves = moves

    def returnKingMoves(self, screen, row, col):
        if self.grid[row][col][0] == 'w':
            color = 'w'
        else:
            color = 'b'
        moves = []

        for i in range(-1, 2):
            for o in range(-1, 2):
                if self.isValidPosition(row + o, col + i):
                    moves.append((row + o, col + i)) if (abs(i) + abs(o) != 0) and (self.grid[row+o][col+i][0] != color)else 0 

        for pos in moves:
            pygame.draw.rect(screen, (0, 200, 0), [pos[1]*64, pos[0]*64, 64, 64])
        
        self.validMoves = moves

    def isValidPosition(self, row, col):
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            return True
        return False
        
    
    def returnSelected(self, screen, row, col):
        color = 'w' if self.whiteTurn == True else 'b'
        if self.grid[row][col] == ' ':
            return
        if self.grid[row][col][0] == color:
            if self.grid[row][col][1] == 'k':
                self.returnKingMoves(screen, row, col)
            if self.grid[row][col][1] == 'q':
                self.returnQueenMoves(screen, row, col)
            if self.grid[row][col][1] == 'r':
                self.returnRookMoves(screen, row, col)
            if self.grid[row][col][1] == 'b':
                self.returnBishopMoves(screen, row, col)
            if self.grid[row][col][1] == 'p':
                self.returnPawnMoves(screen, row, col)
            if self.grid[row][col][1] == 'n':
                self.returnKnightMoves(screen, row, col)

    
    def returnAxis(self, row, col, rowDir, colDir, color):
        try:
            if self.grid[row][col] == ' ':
                available = [(row, col)]
                available.extend(self.returnAxis(row + rowDir, col + colDir, rowDir, colDir, color))
            elif self.grid[row][col][0] != color:
                available = [(row, col)]
            else:
                available = []
        except IndexError:
            available = []

        return available

    def confirmMove(self, row, col):
        if self.checkCastle(row, col) == True:
            castleSound.play()
            return True
        if (row, col) in self.validMoves:
            # special cases
            if self.grid[self.selected[0]][self.selected[1]] == 'wk':
                self.whiteKingMoved = True
            if self.grid[self.selected[0]][self.selected[1]] == 'bk':
                self.blackKingMoved = True
            if self.grid[self.selected[0]][self.selected[1]] == 'wr':
                for rook in self.whiteRooksMoved:
                    if rook == False:
                        rook = True
                        break
            if self.grid[self.selected[0]][self.selected[1]] == 'br':
                for rook in self.blackRooksMoved:
                    if rook == False:
                        rook = True
                        break

            # normal cases
            self.grid[row][col] = self.grid[self.selected[0]][self.selected[1]]
            self.grid[self.selected[0]][self.selected[1]] = ' '
            self.whiteTurn = not self.whiteTurn
            moveSound.play()
            return True
        else:
            return False
    
    def checkCastle(self, row, col):
        if self.grid[self.selected[0]][self.selected[1]][0] == 'w':
            color = 'w'
        else:
            color = 'b'

        if color == 'w':
            if self.grid[self.selected[0]][self.selected[1]] == 'wk' and self.whiteKingMoved == False:
                if self.grid[row][col] == 'wr' and self.whiteRooksMoved < 2:
                    self.grid[self.selected[0]][self.selected[1]] = 'wr'
                    self.grid[row][col] = 'wk'
                    self.whiteKingMoved = True
                    self.whiteRooksMoved += 1
                    self.whiteTurn = not self.whiteTurn
                    return True

        elif color == 'b':
            if self.grid[self.selected[0]][self.selected[1]] == 'bk' and self.blackKingMoved == False:
                if self.grid[row][col] == 'br' and self.blackRooksMoved < 2:
                    self.grid[self.selected[0]][self.selected[1]] = 'br'
                    self.grid[row][col] = 'bk'
                    self.blackKingMoved = True
                    self.blackRooksMoved += 1
                    self.whiteTurn = not self.whiteTurn
                    return True
        
        return False
