'''
@Author: Sebastian Piotr Polak
@Version: 2020-05-17
'''

import numpy as np
from bitboard import Board

class MoveBoard:
    """
    Generate possible move-bitboards for a figure on a certain field

    Current field is not included
    """

    def generate(self, figure, x, y, player='w', game_mode="RK"):
        '''
        Generates possible valid position for the given figure.
        It's current position is not included.
        Standard GameMode is RacingKings

        :param figure: char of the figure
        :param x: 0 to 7 (may be mirrored for your implementation)
        :param y: 0 to 7 (may be mirrored for your implementation)
        :param game_mode: "RK" for RacingKings, "JS" for JumpSturdy
        :return: bitboard as uint64-digit
        '''
        if game_mode == "RK":
            if  (figure == 'k'):    # King
                return self.k(x,y)
            elif(figure == 'q'):    # Queen
                return self.q(x,y)
            elif(figure == 'b'):    # Bishop
                return self.b(x,y)
            elif(figure == 'n'):    # Knight
                return self.n(x,y)
            elif(figure == 'r'):    # Rook
                return self.r(x,y)
            elif(figure == 'p'):    # Pawn
                return self.p(x,y)

        white = True
        if player == 'b':
            white = False

        if game_mode == "JS":     # (up-down)
            if  (figure in "bB"):    # white or black
                return self.js_b(x, y, white)
            elif(figure in "qkQK"):   # white-black / white-white or black-white / black-black
                return self.js_qk(x, y, white)

        raise SyntaxError("Invalid input in MoveBoardGenerator!")
        return 0


# Racing Kings

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
        E = -1   # East
        W = 1  # West

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

        if x<=6:
            if y >= 2:
                bitboard |= self.shift(bit_position, 1 * W, 2 * S)
            if y <= 5:
                bitboard |= self.shift(bit_position, 1 * W, 2 * N)
            if x<=5:
                if y>=1:
                    bitboard |= self.shift(bit_position, 2 * W, 1 * S)
                if y<=6:
                    bitboard |= self.shift(bit_position, 2 * W, 1 * N)

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

# Jump Sturdy

    def js_b(self, x, y, white):
        """
        JumpSturdy: Single figure
        """
        bitboard = bit_position = np.uint64(1) << np.uint64(x + 8 * y)

        if x > 0:
            bitboard |= bitboard >> np.uint64(1)
        if x < 7:
            bitboard |= bitboard << np.uint64(1)

        if white and y<7:
            bitboard |= bitboard << np.uint(8)
        elif not white and y>0:
            bitboard |= bitboard >> np.uint(8)

        return self.del_edges(bitboard & ~bit_position)


    def js_qk(self, x, y, white):
        """
        JumpSturdy: Double figure
        """
        bit_position = np.uint64(1) << np.uint64(x + 8 * y)
        if bit_position == 0:
            raise SyntaxError("Invalid position!")
            return 0
        bitboard = self.n(x, (7-y)) # Earlier funtions assumed a mirrored y-axsis

        temp = np.uint(1)
        while bit_position & temp == 0:
            temp |= temp << np.uint64(1)

        if white:
            bitboard &= ~temp
        else:
            bitboard &= temp

        return self.del_edges(bitboard)


    def del_edges(self, bitboard):
        '''
        Delete edges from bitboard (useful for JumpSturdy)
        :param bitboard:
        :return:
        '''
        edges = np.uint64(9295429630892703873)
        return np.uint64(bitboard) & ~edges

# Only called if you directly execute this code
if __name__ == "__main__":
    out = MoveBoard().generate('k', 6, 6, 'b', "JS")
    #out = MoveBoard().generate('q', 0, 0)
    #print(out)
    Board().printBoard(out)
