import numpy as np
from bitboard import Board

class check_betweeen:

    def __init__(self):
        self.negative = False


    def check(self, before_pos , after_pos ,board_after):
        '''
        :param before_pos: before_pos (1 bit set)
        :param after_pos: after_pos (1 bit set)
        :param board_after: play situation as bitboard
        :return: False if no figure betweeen
        '''

        if (before_pos > after_pos):
            direction, steps = self.check_direction(before_pos, after_pos)
            self.negative = True
        else:
            direction, steps = self.check_direction(after_pos, before_pos)

        if (direction == -1):
            print("move direction can not be detected")
            return False;

        if (direction == 0): # no figure betweeen
            return True;

        return self.calc_if_figure_betweeen(direction, steps, before_pos, after_pos, board_after)
        #if (before_pos > after_pos):
        #    return self.calc_if_figure_betweeen(direction, steps, before_pos, after_pos, board_after)
        #else:
        #    return self.calc_if_figure_betweeen(direction, steps, after_pos, before_pos, board_after)


    def check_direction(self, bigger_bitboard, smaller_bitboard):
        '''
            check_direction is used to find out in which direction the figure is moved
            for racing king
                a horizontal move means if the bigger bitboard havs to be shiftet
                 less than 8 times more than 1 times
                a vertical move means if the bigger bitboard has to be shiftet x times,
                x is a multiple of 8
                a diagonal move means if the bigger bitboard has to be shiftet x times,
                x is a multiple of 9

            todo edge case 1.00000001 -> 10000000 which is a horizontal move
                           2.when the shift number is 56 there are 2 moves
                             7x8(vertical) or 8x7(vertical)
             input: 2 bitboards
            output:
                    -1 move can not be detected
                    0 no space between
                    8 for vertical
                    1 for horizontal
                    9 for diagonal left
                    7 for diagonal right


                    steps
        '''
        counter = 0
        while (bigger_bitboard > smaller_bitboard):
            bigger_bitboard = np.uint64(bigger_bitboard) >> np.uint64(1)
            counter += 1

        if (counter in [8, 9, 1]): # one step #8, 9, 1
            return 0, 0

        if (counter > 9 and (counter % 9) == 0): # diagonal left
            steps = counter / 9
            dir = 9
            return dir, steps
        if (counter > 8 and (counter % 8) == 0): # vertical
            steps = counter / 8
            dir = 8
            return dir, steps
        if (counter > 7 and (counter % 7) == 0): # diagonal right
            steps = counter / 7
            dir = 7
            return dir, steps
        if (counter < 7): # horizontal
            steps = counter
            dir = 1
            return dir, steps
        if (counter == 7): # horizontal wall-to-wall or one step diagonal right
            #TODO check if it is a wall-to-wall move
            return 0, 0

        return -1, -1;

    def calc_if_figure_betweeen(self, direction, steps, before_pos, after_pos, board):
        if (not self.negative):
            temp = np.uint64((before_pos | board) & ~after_pos)
            while(steps > 1):
                before_pos = np.uint64(before_pos) << np.uint64(direction)
                if (temp & before_pos >= 1):
                    return False
                steps -= 1
        else:
            temp = np.uint64((after_pos | board) & ~before_pos)
            while(steps > 1):
                after_pos = np.uint64(after_pos) << np.uint64(direction)
                if (temp & np.uint64(after_pos) >= 1):
                    return False
                steps -= 1

        return True

    def calc_if_figure_betweeen_old(self, dir, steps, bigger_bitboard, smaller_bitboard, board):
        if (dir == 2):
            temp = np.uint64(bigger_bitboard | smaller_bitboard | board) >> np.uint64(1)
            while (temp > 1):
                if ((temp & np.uint64(1)) == 1):
                    return True
            return False

        if (dir == 1):
            temp = np.uint64(bigger_bitboard | smaller_bitboard | board) >> np.uint64(8)
            while (steps > 1):
                if ((temp & np.uint64(1)) == 1):
                    return True
                steps -= 1
                temp = temp >> np.uint64(8)
            return False

        if (dir == 3):
            temp = np.uint64(bigger_bitboard | smaller_bitboard | board) >> np.uint64(9)
            while (steps > 1):
                if (temp & np.uint64(smaller_bitboard) == smaller_bitboard):
                    return False
                steps -= 1
                temp = temp >> np.uint64(9)
            return True

        if (dir == 4):
            temp = np.uint64(bigger_bitboard | smaller_bitboard | board) >> np.uint64(7)
            while (steps > 1):
                if ((temp & np.uint64(1)) == 1):
                    return True
                steps -= 1
                temp = temp >> np.uint64(7)
            return True


        print("fail to calculate")
        return True



if __name__ == "__main__":
    val = check_betweeen()
    a = np.int64(1)
    b = np.int64(262144)
    c = np.int64(512)
    Board().printBoard(a)
    Board().printBoard(b)
    Board().printBoard(c)
    print (val.check(a,b,c)) #should be false



