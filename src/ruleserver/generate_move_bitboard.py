import numpy as np
from bitboard import Board

class MoveBoard:
    """
    Generate possible move-bitboards for a figure on a certain field

    Current field is not included
    """

    def generate(self, figure, x, y):
        if  (figure == 'k'):
            return self.k(x,y)
        elif(figure == 'q'):
            return self.q(x,y)
        elif(figure == 'b'):
            return self.b(x,y)
        elif(figure == 'n'):
            return self.n(x,y)
        elif(figure == 'r'):
            return self.p(x,y)
        elif(figure == 'r'):
            return self.p(x,y)
        return 0

    def k(self, x, y):
        """
        King (Koenig)
        """
        bitboard = np.uint64(0)
        pos = 0
        for i in range(0, 8):
            for j in range(7, -1, -1):
                mask = np.uint64(9223372036854775808 >> pos)
                if self.xor( abs(x - j)<=1 and abs(y - i)<=1, x == j and y == i):
                    bitboard |= mask
                pos += 1
        return bitboard


    def q(self, x, y):
        """
        Queen (Dame)
        """
        return self.b(x, y) | self.r(x, y)


    def p(self, x,y):
        """
        Pawn (Bauer) - not used
        """
        return 0


    def b(self, x,y):
        """
        Bishop (Laeufer)
        """
        bitboard = np.uint64(0)
        pos = 0
        for i in range(0, 8):
            for j in range(7, -1, -1):
                mask = np.uint64(9223372036854775808 >> pos)
                if self.xor( (self.__b_calc(x, y, i, j)), x == j and y == i ):
                    bitboard |= mask
                pos += 1
        return bitboard


    def __b_calc(self, x, y, i, j):
        x_1 = x - j
        y_1 = y - i
        x_2 = j - x
        y_2 = i - y
        if not (x_1 < 0 or y_1 < 0) and x_1 == y_1:
            return True
        if not (x_2 > 7 or y_2 > 7) and x_2 == y_2:
            return True
        if not (x_1 < 0 or y_2 > 7) and x_1 == y_2:
            return True
        if not (x_2 < 0 or y_1 > 7) and x_2 == y_1:
            return True
        return False


    def n(self, x,y):
        """
        Knight (Springer)
        """
        N = -8  # North
        S = 8   # South
        E = 1   # East
        W = -1  # West

        bitboard = np.uint64(0)
        pos = 0
        for i in range (0, y):
            for j in range (0,8):
                pos += 1
        pos += 7-x

        bit_position = np.uint64(9223372036854775808 >> pos)

        if x>=1:
            if y>=2:
                bitboard |= self.shift(bit_position, 1*E, 2*S)
            if y<=5:
                bitboard |= self.shift(bit_position, 1*E, 2*N)
            if x>=2:
                if y>=1:
                    bitboard |= self.shift(bit_position, 2*E, 1*S)
                if y<=6:
                    bitboard |= self.shift(bit_position, 2*E, 1*N)
        if x<=5:
            if y>=1:
                bitboard |= self.shift(bit_position, 2*W, 1*S)
            if y<=6:
                bitboard |= self.shift(bit_position, 2*W, 1*N)
            if x<=6:
                if y>=2:
                    bitboard |= self.shift(bit_position, 1*W, 2*S)
                if y<=5:
                    bitboard |= self.shift(bit_position, 1*W, 2*N)

        return bitboard


    def shift(self,position, x, y):
        if y > 0:
            return position << np.uint64(x+y)
        else:
            return position >> np.uint64(abs(y)-x)


    def r(self, x, y):
        """
        Rook - Turm
        """
        bitboard = np.uint64(0)
        pos = 0
        for i in range(0, 8):
            for j in range(7, -1, -1):
                mask = np.uint64(9223372036854775808 >> pos)
                if self.xor(x == j, y == i):
                    bitboard |= mask
                pos += 1
        return bitboard


    def xor(self, first, second):
        return (first or second) and not (first and second)


# Only called if you directly execute this code
if __name__ == "__main__":
    out = MoveBoard().generate('k', 3, 7)
    # first position is (0,0) which is equivalent to (h,1)
    Board().printBoard(out)
