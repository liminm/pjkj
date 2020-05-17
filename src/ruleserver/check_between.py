'''
@Authors: Heyi Li with help of Sebastian Piotr Polak
@Version: 2020-05-17
'''
import numpy as np

class CheckBetween:

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

        if (direction == -1): # sholdn't happen
            return False, "CheckBetween:Move direction can not be detected";

        if (direction == 0): # no figure betweeen
            return True, "";

        return self.calc_if_figure_betweeen(direction, steps, before_pos, after_pos, board_after)


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
        bigger_bitboard_tmp = bigger_bitboard

        while (bigger_bitboard_tmp > smaller_bitboard):
            bigger_bitboard_tmp = np.uint64(bigger_bitboard_tmp) >> np.uint64(1)
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
            wall_check_1 = np.uint64(smaller_bitboard) & np.uint64(9331882296111890817)
            wall_check_2 = np.uint64(bigger_bitboard) & np.uint64(9331882296111890817)
            if (wall_check_1 >= 1 and wall_check_2 >= 1):
                steps = counter
                dir = 1
                return dir, steps #wall-to-wall move
            return 0, 0 #one-step diagonal

        return -1, -1;

    def calc_if_figure_betweeen(self, direction, steps, before_pos, after_pos, board):
        if (not self.negative):
            temp = np.uint64((before_pos | board) & ~after_pos)
            while(steps > 1):
                before_pos = np.uint64(before_pos) << np.uint64(direction)
                if (temp & np.uint64(before_pos) >= 1):
                    return False, "There is a figure in between"
                steps -= 1
        else:
            temp = np.uint64((after_pos | board) & ~before_pos)
            while(steps > 1):
                after_pos = np.uint64(after_pos) << np.uint64(direction)
                if (temp & np.uint64(after_pos) >= 1):
                    return False, "There is a figure in between"
                steps -= 1

        return True, ""


if __name__ == "__main__":
    val = CheckBetween()
    a = np.int64(1)
    b = np.int64(262144)
    b = np.int64(128)
    c = np.int64(16)
    print (val.check(a,b,c)) #should be false



