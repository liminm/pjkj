from bitboard import racing_kings


class ValidCheck():

    # Calcualtes the position of the moved figure
    # @board_before: FEN-board before the move
    # @board_after:  FEN-board after the move
    # @return: figure-type, before-position, after-position    example: 'r', (1,0), (2,3)
    def calc_positions(self, board_before, board_after):
        before = racing_kings()
        after  = racing_kings()

        before.toBitBoard(board_before)
        after.toBitBoard(board_after)

        figure = self.get_figure(before, after)
        if figure == "":
            return figure, (-1,-1) ,(-1,-1)

        if after.player == "w":
            bit_before = before.white_board[figure]
            bit_after = after.white_board[figure]
        else:
            bit_before = before.black_board[figure]
            bit_after = after.black_board[figure]

        #print("before: ","{0:b}".format(bit_before))
        #print("after:  ","{0:b}".format(bit_after))

        mix = bit_before & bit_after
        bit_before = bit_before - mix
        bit_after  = bit_after  - mix

        #print("mix:    ","{0:b}".format(mix))

        # check if only one figure moves
        if (self.count_bits(bit_before) > 1) or (self.count_bits(bit_after) > 1):
            return "", (-1, -1), (-1, -1)

        # todo?: check if figure of other player wasn't moved

        start_pos = self.get_position(bit_before)
        end_pos   = self.get_position(bit_after)

        return figure, start_pos, end_pos

    # get the figure that was moved
    # return "" if: - no figure moved
    #               - too many moves
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
            except KeyError: # catch Error, if such figure doesn't exist
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

    # req: only one bit set (one figure on bitboard)
    # @return: position of the figure on the bitboard
    def get_position(self, bitboard):
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

    def count_bits(self, number):
        i = 0
        while (number > 0):
            i += number & 1
            number = number >> 1
        return i

check = ValidCheck()

#board1 = "r7/8/8/8/1q7/8/8/r7 w - - 3 2" # produces wrong board -> overflow?
#board2 = "1r6/8/8/8/1q7/8/8/r7 b - - 4 5"

board1 = "r7/8/8/8/1q7/8/8/8 w - - 3 2"
board2 = "2r5/8/8/8/1q7/8/8/8 b - - 4 5"

# game = racing_kings()
# game.toBitBoard(board1)
# game.printBoard(game.black_board['r'])

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
# TODO: check if figure is not out of bounds -> happens before the bitboard-conversion
# TODO: check if the translation is right (direction, board orientation) -> irrelevant
# TODO: add actual check ->HeyiLee

# print(game.cur_state)
# before = "8/8/8/1K6/8/8/8/8 w"
# after  = "8/8/8/2K5/8/8/8/8 w"

# print("{0:b}".format(test))
