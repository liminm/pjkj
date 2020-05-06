import numpy as np
from bitboard import Board
from generate_move_bitboard import MoveBoard


class ValidCheck:
    """
    With
    ValidCheck().check(FEN-Board-before, FEN-Board-after)
    you can check if the move is valid
    """

    def check(self, board_before, board_after):
        """
        Check if the given move if valid. Which figure moves and from-to will be calculated automaticly

        :param board_before: FEN-Board before the move
        :param board_after: FEN-Board after the move
        :return: True if the move is valid
        """
        result = self.calc_positions(board_before, board_after)
        return self.check_valid_move(result[0], result[1], result[2])


    def calc_positions(self, board_before, board_after):
        """
        Calcualtes the position of the moved figure

        :param board_before: FEN-board before the move
        :param board_after:  FEN-board after the move
        :return: figure-type, before-position, after-position-bitboard (string, tuple, bitboard)
        """
        before = Board(board_before)
        after = Board(board_after)

        figure = self.get_figure(before, after)
        if figure == "":
            return "", -1, -1

        if after.player == "w":
            bit_before = before.board[figure] & before.board['wh']
            bit_after  = after.board[figure]  & after.board['wh']
        else:
            bit_before = before.board[figure] & before.board['bl']
            bit_after  = after.board[figure]  & after.board['bl']

        mix = bit_before & bit_after
        bit_before = bit_before & ~mix
        bit_after = bit_after & ~mix

        # check if only one figure moves
        if (self.count_bits(bit_before) > 1) or (self.count_bits(bit_after) > 1):
            return "", -1, -1

        # todo?: check if figure of other player wasn't moved
        return figure, bit_before, bit_after


    def get_figure(self, before, after):
        """
        Get the figure that was moved

        :return: "" if: no figure moved or too many moves
        """
        player_mask_1 = 0
        player_mask_2 = 0
        fig_moved = 0
        curr_fig = ""
        if after.player == 'w':
            player_mask_1 = before.board['wh']
            player_mask_2 = after.board['wh']
        elif after.player == "b":
            player_mask_1 = before.board['bl']
            player_mask_2 = after.board['bl']
        for fig in "kbrnq":
            try:
                fig_board_before = before.board[fig] & player_mask_1
                fig_board_after  = after.board[fig]  & player_mask_2
            except KeyError:    # catch Error, if such figure doesn't exist
                continue
            if fig_board_before != fig_board_after:
                curr_fig = fig
                fig_moved += 1
        if (fig_moved == 1):
            return curr_fig
        return ""


    def get_position(self, bitboard):
        """
        :param bitboard: bitboard with ony one bit set
        :return: position of the figure on the bitboard
        """
        x = -1
        y = 7
        if bitboard == 0:
            return (-1, -1)
        while bitboard != 0:
            bitboard = bitboard >> np.uint64(1)
            x += 1
            if x >= 8:
                x = 0
                y -= 1
        return (x, y)


    def count_bits(self, number):
        i = 0
        while (number > 0):
            i += number & np.uint64(1)
            number = number >> np.uint64(1)
        return i


    def check_valid_move(self, figure, before_bit_position, after_bit_position):
        if (before_bit_position == after_bit_position):
            return False
        start_pos = self.get_position(before_bit_position)

        move_bitboard = np.uint64( MoveBoard().generate(figure, start_pos[0], start_pos[1]) )

        # TODO: check for jump over figures

        if (move_bitboard & after_bit_position != 0):
            return True
        return False


    def check_valid_move_old(self, figure, x, y, target_x, target_y):
        """
        Check if the move of the specific figure is correct

        :param figure: the figure, as char. 'k', 'b', ...
        :param x: startposition
        :param y: startposition
        :param target_x: target position
        :param target_y: target position
        :return: valid (True) or not valid (False) move
        """
        if ((target_x == x and target_y == y) or not (0 <= target_x <= 7 and 0 <= target_y <= 7)):
            print("unvalid target position or the start and target position have to be different")
            return False

        result = []
        (tmp_x, tmp_y) = (x, y)
        # Queen possbile moves
        if figure == 'Q':
            # diago case
            while (x < 7 and y < 7):
                result.append((x + 1, y + 1))
                x += 1
                y += 1
            (x, y) = (tmp_x, tmp_y)
            # diago case
            while (x > 0 and y > 0):
                result.append((x - 1, y - 1))
                x -= 1
                y -= 1
            (x, y) = (tmp_x, tmp_y)
            # vertical
            while (x < 7):
                result.append((x + 1, y))
                x += 1
            (x, y) = (tmp_x, tmp_y)
            # vertical
            while (x > 0):
                result.append((x - 1, y))
                x -= 1
            # horizontal
            (x, y) = (tmp_x, tmp_y)
            while (y < 7):
                result.append((x, y + 1))
                y += 1

            # horizontal
            (x, y) = (tmp_x, tmp_y)
            while (y > 1):
                result.append((x, y - 1))
                y -= 1
            if (target_x, target_y) in result:
                return True
            return False
        # Rook possible moves
        if figure == 'R':
            # vertical
            while (x < 7):
                result.append((x + 1, y))
                x += 1
            (x, y) = (tmp_x, tmp_y)
            # vertical
            while (x > 0):
                result.append((x - 1, y))
                x -= 1
            # horizontal
            (x, y) = (tmp_x, tmp_y)
            while (y < 7):
                result.append((x, y + 1))
                y += 1
            # horizontal
            (x, y) = (tmp_x, tmp_y)
            while (y > 1):
                result.append((x, y - 1))
                y -= 1
            if (target_x, target_y) in result:
                return True
            return False
        # King possible moves
        if figure == 'K':
            if ((target_x - x in (0, 1, -1)) and (target_y - y in (0, 1, -1))):
                return True
            return False
        # Knight possbile moves
        if figure == 'KN':
            if ((target_x - x in (2, -2)) and (target_y - y in (1, -1))):
                return True
            elif ((target_x - x in (1, -1)) and (target_y - y in (2, -2))):
                return True
            return False

        print("the given figure can not be identified or the unvalid position")
        return False


# Only called if you directly execute this code
if __name__ == "__main__":
    board1 = "1k6/8/8/8/1q6/8/8/r7 w - - 3 2"
    board2 = "2k5/8/8/8/1q6/8/8/r7 b - - 4 5"
    board3 = "2k5/8/8/8/1q6/8/8/7r b - - 4 5"
    board4 = "3k4/8/8/8/1q6/8/8/r7 b - - 4 5"
    board5 = "8/8/1r6/8/8/8/q1bnNBRQ/krbnNBRK b - - 0 1"
    board6 = "8/8/1r6/8/5N2/8/q1bn1BRQ/krbnNBRK w - - 0 1"

    #should be true (king move)
    valid = ValidCheck().check(board1, board2)
    print("Valid move?", valid)

    #should be false (too many moves)
    valid = ValidCheck().check(board1, board3)
    print("Valid move?", valid)

    #should be false (too many steps)
    valid = ValidCheck().check(board1, board4)
    print("Valid move?", valid)

    #should be true (ponny test)
    valid = ValidCheck().check(board5, board6)
    print("Valid move?", valid)



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

# TODO: check if only one figure moves - ok
# TODO: check if figure is not out of bounds -> happens before the bitboard-conversion -ok
# TODO: check if the translation is right (direction, board orientation) -> irrelevant -ok

#todo: check if figure doesnt 'jump' over other figures