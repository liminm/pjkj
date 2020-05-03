import numpy as np
import re

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
            raise SyntaxError("The FEN string is not valid!")
            
        return [m.group(i) for i in range(1, int(self.pattern.groups+1) )]
        
    def parse(self, fen):
        turn_parts = self.scan(fen)

        self.fields = turn_parts[0];
        self.player = turn_parts[9]
        self.rochade = turn_parts[10]
        self.enPassant = turn_parts[11]
        self.halfRounds = turn_parts[12]
        self.roundCount = turn_parts[13]
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
    
    """
    
    this functions sets a field on the bitboard. You have to give a location, for example 'f2' and a character in fen style, like 'Q' or 'q', for white and black queens.
    
    """
    def setField(self, position, character):
        position = position[0].lower() +position[1]
        m = re.compile("[a-h][1-8] [qQkKrRpPnN]").match(position + " " + character)
        
        if m is None:
            raise SyntaxError("The Syntax of the position or character is wrong!")
        
        x = 7-int(ord(position[0])-ord("a"))
        y = int(position[1])-1
        pos = y*8+x
        print(pos)
        mask = np.uint64(1 << pos)
        
        self.removeField(position)
        self.board[character.lower()] |= mask
        if character.lower() == character:
            self.board["bl"] |= mask
        else:
            self.board["wh"] |= mask
    
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
    
    # returns a fen string
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
    
    # returns a human readable representation
    def __str__(self):
        matrix = self.toMatrix()
        
        s = ""
        for i in range(matrix.shape[0]*matrix.shape[1]):
            s += matrix[int(i/8)][i%8]
            if (i+1)%8==0:
                s += "\n"
        s += "player:"+self.player + ", rochade:"+self.rochade+", enPassant:"+self.enPassant+", halfRounds:"+str(self.halfRounds)+", roundCount:"+str(self.roundCount)
        
        return s


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
if __name__ == "__main__": 
    sample = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    rkStart = "8/8/8/8/8/8/qrbnNBRQ/krbnNBRK w - - 0 1"
    b = Board(rkStart)
    
    # default string representation
    b.setField("h3", "p")
    print(b)
    print(repr(b))