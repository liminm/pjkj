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

    def __init__(self,  board = None):
        self.start = "8/8/8/8/8/8/krbnKRBN/qrbnQRBN w - - 0 1"
        self.fen = self.start
        self.last_fen = ""
        self.allFens = []
        self.player = 'w'
        self.player_last = ''
        self.figures = ["krbnqKRBNQ"]
        self.pattern = re.compile(
            "([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8}) ([wb]) (\-|KQ?k?q?|K?Qk?q?|K?Q?kq?|K?Q?k?q) (\-|[a-f][1-8]) (\d+) (\d+)")
        self.board_white = {
            'K': 0,
            'B': 0,
            'N': 0,
            'R': 0,
            'Q': 0,
        }
        self.board_black = {
            'k': 0,
            'b': 0,
            'n': 0,
            'r': 0,
            'q': 0,
        }
        self.board_white_last = {
            'K': 0,
            'B': 0,
            'N': 0,
            'R': 0,
            'Q': 0,
        }
        self.board_black_last = {
                'k': 0,
                'b': 0,
                'n': 0,
                'r': 0,
                'q': 0,
        }



        if board == None :
            self.toBitBoard(self.start)
            self.allFens.append(self.start)
            self.player = 'w'
        else :
            self.toBitBoard(board)
            self.allFens.append(board)

    """
    scan if fen String is valid
    return ??
    """
    def scan(self, fen):
        m = self.pattern.match(fen)

        if m is None:
            raise SyntaxError("The FEN string is not valid!")

        return [m.group(i) for i in range(1, int(self.pattern.groups + 1))]

    """
    
    """
    def checkFigures(self, lines):
        if len(lines) != 8:
            return False

        for l in lines:
            figures = 0
            for c in l:
                if c.isdigit():
                    figures += int(c)
                else:
                    figures += 1

            if figures != 8:
                return False
        return True

    """
    stores and overwrite board_white and bord_black using resetBoard()
    """
    def toBitBoard(self, fen):
        pos = 0
        self.scan(fen)
        turn_parts = fen.split()
        self.board_black_last = self.board_black.copy()
        self.board_white_last = self.board_white.copy()

        self.player = turn_parts[1]
        self.fen = turn_parts[0];
        white = {
            'K': list("{0:b}".format(0).zfill(64)),
            'B': list("{0:b}".format(0).zfill(64)),
            'N': list("{0:b}".format(0).zfill(64)),
            'R': list("{0:b}".format(0).zfill(64)),
            'Q': list("{0:b}".format(0).zfill(64)),
        }
        black = {
            'k': list("{0:b}".format(0).zfill(64)),
            'b': list("{0:b}".format(0).zfill(64)),
            'n': list("{0:b}".format(0).zfill(64)),
            'r': list("{0:b}".format(0).zfill(64)),
            'q': list("{0:b}".format(0).zfill(64)),
        }
        pos = 0
        for elem in turn_parts[0]:
            if elem == 'K':
                white['K'][pos] = '1'
                pos += 1
            elif elem == 'B':
                white['B'][pos] = '1'
                pos += 1
            elif elem == 'N':
                white['N'][pos] = '1'
                pos += 1
            elif elem == 'R':
                white['R'][pos] = '1'
                pos += 1
            elif elem == 'Q':
                white['Q'][pos] = '1'
                pos += 1
            elif elem == 'k':
                black['k'][pos] = '1'
                pos += 1
            elif elem == 'b':
                black['b'][pos] = '1'
                pos += 1
            elif elem == 'n':
                black['n'][pos] = '1'
                pos += 1
            elif elem == 'r':
                black['r'][pos] = '1'
                pos += 1
            elif elem == 'q':
                black['q'][pos] = '1'
                pos += 1
            elif elem != '/':
                pos += int(elem)

        for k, v in self.board_white.items():
            white[k] = int("".join(white[k]), base = 2)
        for k,v in self.board_black.items():
            black[k] = int("".join(black[k]), base = 2)

        bitboards = [white, black]
        print(bitboards)
        self.resetBoard(bitboards)
        return (bitboards)


        """
        stores and overwrite board_white and board_black 
        bitboards = [white, black]
        """
    def resetBoard(self, bitboards = []):

        if len(bitboards) == 0:
            for k, v in self.board_white.items():
                self.board_white_last[k] = self.board_white[k]
                self.board_white[k] = 0
            for k, v in self.board_black.items():
                self.board_black_last[k] = self.board_black[k]
                self.board_black[k] = 0
            self.player_last = self.player

        else:
            print(bitboards[0]['K'])
            for k, v in self.board_white.items():
                self.board_white[k] = bitboards[0][k]
                print("hier")
                print(self.board_white[k])
            for k, v in self.board_black.items():
                self.board_black[k] = bitboards[1][k]


    """
    print bitboard using self.fen
    """
    def printBoard(self):
        pos = 0
        res = ""
        for elem in self.fen:
            if pos == 8:
                pos = 0
                res += "\n"
            if ord(elem) < 57 and ord(elem) > 48:  # we have a number with 1-8 49-56
                for i in range(int(elem)):
                    res += '0'
                    pos += 1
            else:
                if elem != "/":
                    res += elem
                    pos += 1
        print(res)

game = Board()
print(game.board_white)
print("{0:b}".format(game.board_white['N']).zfill(64))
