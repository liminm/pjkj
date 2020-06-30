import numpy as np
import re
"""
import random

ZOBRIST_INDICES = {"q": np.uint64(0), # queen
            "k": np.uint64(1), # king
            "p": np.uint64(2), # pawn
            "b": np.uint64(3), # bishop
            "n": np.uint64(4), # knight
            "r": np.uint64(5), # rook
            "Q": np.uint64(6), # queen
            "K": np.uint64(7), # king
            "P": np.uint64(8), # pawn
            "B": np.uint64(9), # bishop
            "N": np.uint64(10), # knight
            "R": np.uint64(11), # rook
            }

if not "ZOBRIST_MATRIX" is globals():
    init_Zobrist()

def init_Zobrist():
    global ZOBRIST_MATRIX
    ZOBRIST_MATRIX = np.zeros((64,12), type=np.uint64)
    
    for i in range(64):
        for j in range(12):
            ZOBRIST_MATRIX[i][j] = np.uint64(randint(0, 2**64))
"""
"""
Notation:
a trun will alway be FEN i.e: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1    
we start at the top row number 8
small letters for the black figuees and capital letters for white 
r - rook (Turm), n - knight(Springer), b - bishop(laeufer), q - queen (Koenigin), k - king (koenig)
--> racing king is not played with pawns
an 8 is tells us the amount of empty fields, if we have a king on the third tile from the left : 2k5
the first letter after the board description is the current player
the KQkq we can ignore and will be replaced with - (chess only rules)
the - wont be changed (again chess rules that do not apply to racing kings)
the 0 is the amount of halfturns since the last figure was killed TODO languge 
1 the round number that is currently played
"""
class Board:
    
    def __init__(self, string=None):
        self.string = string
        self.board = {
            "q": np.uint64(0), # queen
            "k": np.uint64(0), # king
            "p": np.uint64(0), # pawn
            "b": np.uint64(0), # bishop
            "n": np.uint64(0), # knight
            "r": np.uint64(0), # rook
            "wh": np.uint64(0), # white
            "bl": np.uint64(0) # black
        }
        self.player = "w"
        self.rochade = "-"
        self.enPassant = "-"
        self.halfRounds = 0
        self.roundCount = 1
        
        self.log = []
        
        self.pattern = re.compile("(([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})) ([wb]) (\-|KQ?k?q?|K?Qk?q?|K?Q?kq?|K?Q?k?q) (\-|[a-f][1-8]) (\d+) (\d+)")
        
        if not string is None:
            self.parse(string)
        
    """
    return [0: Figurenstellungen mit / separated
           1-8:    Figurenstellung aus der FEN Notation,
            9:      Spieler am Zug,
            10:      Rochade,
            11:     En passant,
            12:     Halbzuege
            13:     Zugnummer]
    """
    def scan(self, string):
        m = self.pattern.match(string)
        
        if m is None:
            raise SyntaxError("The FEN string is not valid! string:" + string)
            
        return [m.group(i) for i in range(1, int(self.pattern.groups+1) )]
        
    def parse(self, fen):
        turn_parts = self.scan(fen)

        self.fields = turn_parts[0];
        self.player = turn_parts[9]
        self.rochade = turn_parts[10]
        self.enPassant = turn_parts[11]
        self.halfRounds = int(turn_parts[12])
        self.roundCount = int(turn_parts[13])
        pos = 0
        for elem in self.fields:
            mask = np.uint64(9223372036854775808>>pos) # 9223372036854775808 == s^63
            if elem == 'K':
                self.board[elem.lower()] |= mask
                self.board["wh"] |= mask
                pos += 1
            elif elem == 'B':
                self.board[elem.lower()] |= mask
                self.board["wh"] |= mask
                pos += 1
            elif elem == 'N':
                self.board[elem.lower()] |= mask
                self.board["wh"] |= mask
                pos += 1
            elif elem == 'R':
                self.board[elem.lower()] |= mask
                self.board["wh"] |= mask
                pos += 1
            elif elem == 'Q':
                self.board[elem.lower()] |= mask
                self.board["wh"] |= mask
                pos += 1
            elif elem == 'P':
                self.board[elem.lower()] |= mask
                self.board["wh"] |= mask
                pos += 1
            elif elem == 'k':
                self.board[elem.lower()] |= mask
                self.board["bl"] |= mask
                pos += 1
            elif elem == 'b':
                self.board[elem.lower()] |= mask
                self.board["bl"] |= mask
                pos += 1
            elif elem == 'n':
                self.board[elem.lower()] |= mask
                self.board["bl"] |= mask
                pos += 1
            elif elem == 'r':
                self.board[elem.lower()] |= mask
                self.board["bl"] |= mask
                pos += 1
            elif elem == 'q':
                self.board[elem.lower()] |= mask
                self.board["bl"] |= mask
                pos += 1
            elif elem == 'p':
                self.board[elem.lower()] |= mask
                self.board["bl"] |= mask
                pos += 1
            elif elem != '/':
                pos += int(elem)
            elif elem == '/' and pos % 8 != 0:
                raise RuntimeError("ParseError: Each line on the board has to contain exactly 8 fields.")
    
    def movePlayer(self, start, end=None, logging=False):
        """
        this is for debugging
        """
        if end is None:
            m = re.compile("([a-h][1-8])[- ]?([a-h][1-8])").match(start.lower())
            if m is None:
                raise SyntaxError("Syntax Error in UCI String!")
            
            start = m.group(1)
            end = m.group(2)
        
        if logging:
            move = [repr(self), start, end, "True"]
        
        # halbzüge
        newRound = self.halfRounds
        if self.getField(start) in ["pP"]:
            newRound = 0
        elif not self.getField(end) is None:
            newRound = 0
        else:
            newRound+=1
        
        self.moveUCI(start, end)
        
        if self.player == "b":
            self.roundCount+=1
        if self.player == "w":
            self.player = "b"
        else:
            self.player = "w"
            
        if logging:
            self.log.append(move)
        self.halfRounds = newRound
    
    def moveUCI(self,start,end=None):
        if end is None:
            m = re.compile("([a-h][1-8])[- ]?([a-h][1-8])").match(start.lower())
            if m is None:
                raise SyntaxError("Syntax Error in UCI String! string:" + start)
            
            start = m.group(1)
            end = m.group(2)
        
        character = self.getField(start)
        self.getField(end)
        if character is None:
            raise ValueError("No Character on the field! field:" + start + ","+end + "\nboard:\n"+str(self))
        
            
        self.setField(end, character)
        self.removeField(start)
    
    def getOwner(self, position):
        field = self.getField(position)
        if field is None:
            return None
            
        if field.lower() == field:
            return "b"
        else:
            return "w"
    
    def setField(self, position, character):
        """
    
        this functions sets a field on the bitboard. You have to give a location, for example 'f2' and a character in fen style, like 'Q' or 'q', for white and black queens.
        
        """
        
        position = position[0].lower() + position[1]
        m = re.compile("[a-h][1-8] [qQkKrRpPnNbB]").match(position + " " + character)
        
        if m is None:
            raise SyntaxError("The Syntax of the position or character is wrong!")
        
        x = 7-int(ord(position[0])-ord("a"))
        y = int(position[1])-1
        pos = y*8+x
        mask = np.uint64(1 << pos)
        
        self.removeField(position)
        self.board[character.lower()] |= mask
        if character.lower() == character:
            self.board["bl"] |= mask
        else:
            self.board["wh"] |= mask
    
    def getField(self, position):
        position = position[0].lower() +position[1]
        m = re.compile("[a-h][1-8]").match(position)
        
        if m is None:
            raise SyntaxError("The Syntax of the position is wrong! string:" + start)
        
        x = 7-int(ord(position[0])-ord("a"))
        y = int(position[1])-1
        pos = y*8+x
        mask = (np.uint64(1 << pos))
        for b in self.board:
            if b in ["wh", "bl"]:
                continue
                
            if bool(self.board[b] & mask):
                if bool(self.board["wh"] & mask):
                    return b.upper()
                elif bool(self.board["bl"] & mask):
                    return b.lower()
                break
        
        return None
    
    def findCharacter(self, character):
        if re.compile("[rnbqkpPRNBQK]").match(character) is None:
            raise SyntaxError("The Syntax of the character is wrong!")
        
        field = self.board[character.lower()]
        
        if character.lower() == character:
            field &= self.board["bl"]
        else:
            field &= self.board["wh"]
    
        positions = []
        for i in range(64):
            mask = np.uint64(1 << i)
            
            if mask & field != 0:
                positions.append(i)
        return positions
    
    def removeField(self, position):
        position = position[0].lower() +position[1]
        m = re.compile("[a-h][1-8]").match(position)
        
        if m is None:
            raise SyntaxError("The Syntax of the position is wrong!")
        
        x = 7-int(ord(position[0])-ord("a"))
        y = int(position[1])-1
        pos = y*8+x
        mask = ~(np.uint64(1 << pos))
        for b in self.board:
            self.board[b] &= mask
    
    def toMatrix(self):
        get_bin = lambda x, n: format(x, 'b').zfill(n)
        toBitmask = lambda x : np.array([np.bool(int(c)) for c in get_bin(x,64)])
    
        matrix = np.array(["." for i in range(64)])
        black = toBitmask(self.board["bl"])
        white = toBitmask(self.board["wh"])
        
        for key, value in self.board.items():
            if key in ["wh", "bl"]:
                continue
        
            mask = toBitmask(value)
            
            matrix[np.bitwise_and(mask, black)] = key.lower()
            matrix[np.bitwise_and(mask, white)] = key.upper()
        
        return matrix.reshape((8,8))
    
    # returns a fen string. Can be called via repr(board)
    def __repr__(self):
        matrix = self.toMatrix()
        
        fen = ""
        for line in matrix:
            count = 0
            for c in line:
                if c == ".":
                    count+=1
                else:
                    if count != 0:
                        fen += str(count)
                        count = 0
                    fen += c
                    
            if count != 0:
                fen += str(count)
            fen += "/"
        fen = fen[:len(fen)-1] + ' ' # delete last / and replace it with a space
        
        fen += self.player + " "
        fen += self.rochade + " "
        fen += self.enPassant + " "
        fen += str(self.halfRounds) + " "
        fen += str(self.roundCount)
        
        return fen
    
    # returns a human readable representation. can be called via str(board) or print(board)
    def __str__(self):
        matrix = self.toMatrix()
        
        s = "  abcdefgh\n"
        for i in range(matrix.shape[0]*matrix.shape[1]):
            if i%8==0:
                s+= str(8-(int(i/8))) + "|"
                
            s += matrix[int(i/8)][i%8]
            if (i+1)%8==0:
                s += "\n"
        s += ""
        s += "player:"+self.player + ", rochade:"+self.rochade+", enPassant:"+self.enPassant+", halfRounds:"+str(self.halfRounds)+", roundCount:"+str(self.roundCount)
        
        return s
    
    def stringHash(self):
        r = repr(self)
        return r.split(" ")[0]
    
    def __hash__(self):
        return hash(self.stringHash())
    
    """
    this function is called if you compare 2 boards with the '==' operator
    """    
    def __eq__(self, other):
        return self.board == other.board and self.player == other.player and self.rochade == other.rochade and self.enPassant == other.enPassant and self.halfRounds == other.halfRounds and self.roundCount == other.roundCount

def printBoard(self, bitboard):
    board = '{0:b}'.format(bitboard).zfill(64)
    board = board[::-1]
    indices = [0,8,16,24,32,40,48,56,]
    parts = [board[i:j] for i,j in zip(indices, indices[1:]+[None])]
    rows = [8,7,6,5,4,3,2,1]
    for i in range(1,9):
        parts[i-1] = str(rows[i-1])+'|'+ parts[i-1]
    parts.insert(0,"  abcdefgh")
    print('\n'.join(parts))
    
"""
main function
is only called if you directly execute this code, not just if you import it
"""
from copy import deepcopy
if __name__ == "__main__": 
    sample = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    rkStart = "8/8/8/8/8/8/qrbnNBRQ/krbnNBRK w - - 0 1"
    
    b = Board(rkStart)
    print(b)
    b.moveUCI("a2 a3")
    b.moveUCI("a3-a2")
    b.moveUCI("a2a3")
    print(b)
    
    #b2 = deepcopy(b)
    
    
    # default string representation
    #print(b)
    #print(b==b2)
    #b.setField("h3", "p")
    #print(b==b2)
    #print(repr(Board()))