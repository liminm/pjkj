import numpy as np
from bitboard import Board
from check_between import check_betweeen
from generate_move_bitboard import MoveBoard


class ValidCheck:
    """
    With
    ValidCheck().check(FEN-Board-before, FEN-Board-after)
    you can check if the move is valid
    """

    def check(self, board_before, board_after):
        """
        Check if the given move if valid. Which figure moves and from-to will be calculated automaticly.
        IT DOES NOT check, if a king is in check, or if the given player wins

        :param board_before: FEN-Board before the move
        :param board_after: FEN-Board after the move
        :return: True if the move is valid
        """
        result = self.calc_positions(board_before, board_after)
        if (self.check_valid_move(result[0], result[1], result[2])):
            if result[0] in "qbr": # check for figures in between
                board = Board(board_after)
                all_figures = board.board['wh'] | board.board['bl']
                if(check_betweeen().check(result[1], result[2], all_figures)):
                    return True
                else:
                    return False
            else:
                return True
        return False


    def calc_positions(self, board_before, board_after):
        """
        Calcualtes the position of the moved figure

        :param board_before: FEN-board before the move
        :param board_after:  FEN-board after the move
        :return: figure-type, before-position, after-position (string, bitboard, bitboard)
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
        bit_pos_before = bit_before & ~mix
        bit_pos_after  = bit_after & ~mix

        # check if only one figure moves
        if (self.count_bits(bit_pos_before) > 1) or (self.count_bits(bit_pos_after) > 1):
            return "", -1, -1

        return figure, bit_pos_before, bit_pos_after


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
        '''
        With the given Bitbords (where only one bit for the position is set),
        this function checks if the given figure does a valid move
        :param figure: figure as a char
        :param before_bit_position: bitboard with one bit set
        :param after_bit_position: bitboard with one bit set
        :return: true if the figure moves like it should (example: knight-like-move)
        '''
        if (before_bit_position == after_bit_position):
            return False
        start_pos = self.get_position(before_bit_position)

        move_bitboard = np.uint64( MoveBoard().generate(figure, start_pos[0], start_pos[1]) )

        if (move_bitboard & after_bit_position != 0):
            return True
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
    print("True?", valid)

    #should be false (too many moves)
    valid = ValidCheck().check(board1, board3)
    print("False?", valid)

    #should be false (too many steps)
    valid = ValidCheck().check(board1, board4)
    print("False?", valid)

    #should be true (ponny test)
    valid = ValidCheck().check(board5, board6)
    print("True?", valid)
