from bitboard import racing_kings


class ValidCheck():
    # get the figure that was moved
    # return "" if:
    #               no figure moved
    #               too many moves
    def get_figure(self, before, after):
        if after.player == 'w':
            return self.get_figure_w(before, after, 0)
        elif after.player == "b":
            return self.get_figure_b(before, after, 0)
        else:
            return ""

    def get_figure_w(self, before, after, fig_moved):
        curr_fig = ""
        for fig in "KBNRQ":
            try:
                fig_board_before = before.white_board[fig]
                fig_board_after  = after.white_board[fig]
            except KeyError:
                continue
            if fig_board_before != fig_board_after:
                curr_fig = fig
                fig_moved += 1
        if (fig_moved == 1):
            return curr_fig
        return ""

    def get_figure_b(self, before, after, fig_moved):
        curr_fig = ""
        for fig in "kbrnq":
            try:
                fig_board_before = before.black_board[fig]
                fig_board_after  = after.black_board[fig]
            except KeyError:
                continue
            if fig_board_before != fig_board_after:
                curr_fig = fig
                fig_moved += 1
        if (fig_moved == 1):
            return curr_fig
        return ""

    def get_position(self, bitboard): #todo fix?
        x = -1
        y = 0
        if bitboard == 0:
            return (-1, -1)
        while bitboard != 0:
            bitboard = bitboard >> 1
            x += 1
            if x >= 8:
                x = 0
                y += 1
        return (x, y)

    def calc_positions(self, board_before, board_after):
        before = racing_kings()
        after  = racing_kings()

        before.toBitBoard(board_before)
        after.toBitBoard(board_after)

        figure = self.get_figure(before, after)
        if figure == "":
            return figure, (0,0) ,(0,0)

        if after.player == "w":
            bit_before = before.white_board[figure]
            bit_after = after.white_board[figure]
        else:
            bit_before = before.black_board[figure]
            bit_after = after.black_board[figure]

        #print("before: ","{0:b}".format(bit_before))
        #print("after:  ","{0:b}".format(bit_after))

        mix = bit_before & bit_after # todo check alternative (doesnt work?)
        bit_before = bit_before - mix
        bit_after  = bit_after  - mix

        #print("mix:    ","{0:b}".format(mix))

        ##todo: check if only one figure moves

        start_pos = self.get_position(bit_before)
        end_pos   = self.get_position(bit_after)

        return figure, start_pos, end_pos


check = ValidCheck()

#board1 = "r7/8/8/8/1q7/8/8/r7 w - - 3 2" # produces wrong board -> overflow?
#board2 = "1r6/8/8/8/1q7/8/8/r7 b - - 4 5"

board1 = "2r5/8/8/8/1q7/8/8/r7 w - - 3 2"
board2 = "1r6/8/8/8/1q7/8/8/r7 b - - 4 5"

move = check.calc_positions(board1, board2)
print(move)
# game.toBitBoard(board1)
# state = game.cur_state
# game.printBoard(game.black_board['r'])
# game.printBoard(state)
# print(game.cur_state)

# example
# a1 = 0b00110000000010
# a2 = 0b10110000000000
# print("{0:b}".format(a1))
# print("{0:b}".format(a2))

# move = check.calc_positions(a1, a2)
# print("Figure, (x,y):     ",move)

# TODO: check if only one figure moves
# TODO: check if figure is not out of bounds
# TODO: check if the translation is right (direction, board orientation)
# TODO: add actual check

# print(game.cur_state)
# before = "8/8/8/1K6/8/8/8/8 w"
# after  = "8/8/8/2K5/8/8/8/8 w"

# print("{0:b}".format(test))
