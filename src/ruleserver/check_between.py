import numpy as np

class check_betweeen:


    '''
    input: before_pos, after_pos ( 1 bit is set by each board)
           board_after  (play situation as bitboard)
    output: True there is a figur between
            False no figur betweeen
    '''

    def check(self, before_pos , after_pos ,board_after):


        if (before_pos > after_pos):
            direction, steps = self.check_direction(before_pos, after_pos)
        else:
            direction, steps = self.check_direction(after_pos, before_pos)

        if (direction == -1):
            print("move direction can not be detected")
            return False;

        if (direction == 0):
            print ("no figure betweeen")
            return False;

        if (before_pos > after_pos):
            return self.calc_if_figure_betweeen(direction,steps, before_pos, after_pos, board_after)
        else:
            return self.calc_if_figure_betweeen(direction, steps,after_pos, before_pos, board_after)

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
                1 for vertical
                2 for horizontal
                3 for diagonal


                steps
    '''
    def check_direction(self, bigger_bitboard, smaller_bitboard):
        counter = 0
        smaller_bitboard_len = self.calc_length(smaller_bitboard)
        while (bigger_bitboard > smaller_bitboard):
            bigger_bitboard = bigger_bitboard >> 1
            counter += 1

        if (counter in [8, 9, 1]):
            return 0

        if (counter > 9 and counter % 9 == 0):
            steps = counter / 9
            dir = 3
            return dir, steps
        if (counter > 8 and counter % 8 == 0):
            steps = counter / 8
            dir = 1
            return dir, steps
        if (counter < 7):
            steps = counter
            dir = 2
            return dir, steps
        else:
            return -1;


    def calc_if_figure_betweeen(self, dir, steps, bigger_bitboard, smaller_bitboard, board):
        if (dir == 2):
            temp = (bigger_bitboard | smaller_bitboard | board) >> 1
            while (temp > 1):
                if ((temp & 1) == 1):
                    return True
            return False

        if (dir == 1):
            temp = (bigger_bitboard | smaller_bitboard | board) >> 8
            while (steps > 1):
                if ((temp & 1) == 1):
                    return True
                steps -= 1
                temp = temp >> 8
            return False

        if (dir == 3):
            temp = (bigger_bitboard | smaller_bitboard | board) >> 9
            while (steps > 1):
                if ((temp & 1) == 1):
                    return True
                steps -= 1
                temp = temp >> 9
                return False

        print("fail to calculate")
        return True


    def calc_length(self, bitnumber):
        counter = 0
        while (bitnumber > 0):
             bitnumber = bitnumber >> 1
             counter += 1
        return counter


if __name__ == "__main__":
    val = check_betweeen()
    a = np.int64(1)
    b = np.int64(262144)
    c = np.int64(512)
    print (val.check(a,b,c))



