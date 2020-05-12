import numpy as np
import re
from bitboard import Board
from check_between import CheckBetween
from generate_move_bitboard import MoveBoard


class ValidCheck:
    def check(self, first_string, second_string, game_mode="RK"):
        '''
        Function to check , if the givent movement is valid. Default GameMode is RacingKings (RK).
        Consider different input for RacingKings and JumpSturdy! RK accepts two FEN-Strings.
        JS accepts FEN-String before the move and a UCI-Move-String (like "a2-a3").

        :param first_string: FEN-Board before the move
        :param second_string:
         RacingKings: FEN-Board after the move  -
         JumpSturdy: UCI-Move-String
        :param game_mode: "RK" for RacingKings or "JS" for JumpSturdy.
        :return: True if the move is valid
        '''
        if game_mode == "RK":
            return ValidCheckRacingKings().check(first_string, second_string)
        elif game_mode == "JS":
            return ValidCheckJumpSturdy().check(first_string, second_string)
        else:
            raise SyntaxError("game_mode is not valid! Needs to be \"RK\" or \"JS\"!")
            return False


    def tranaslate_uci(self, uci_string):
        '''
        Translates the UCI-String to intern-used format
        :param uci_string:
        :return: x1, y1, x2, y2 (all Int)
        '''
        m = re.compile("([a-h][1-8])[- ]?([a-h][1-8])").match(uci_string.lower())
        if m is None:
            raise SyntaxError("The UCI-String \"" + uci_string+  "\" is not valid!")
        a = m.group(1)
        b = m.group(2)
        x1 = 7 - int(ord(a[0]) - ord("a"))
        y1 = int(a[1]) - 1
        x2 = 7 - int(ord(b[0]) - ord("a"))
        y2 = int(b[1]) - 1
        return x1, y1, x2, y2


class ValidCheckJumpSturdy:

    def __init__(self, fen_before = None):
        if fen_before == None:
            self.board_before = None
        else:
            self.board_before = Board(fen_before)


    def check(self, fen_before, uci_move):
        '''
        Check if the given move is valid. Includes checking figures compability.

        :param fen_before: FEN-Board before the move
        :param uci_move: string. example: "a2-b3"
        :return: True if the move is valid
        '''
        if self.board_before is None:
            self.board_before = Board(fen_before)

        x1, y1, x2, y2 = ValidCheck().tranaslate_uci(uci_move)
        start_figure = self.get_figure(x1, y1, self.board_before)
        end_figure   = self.get_figure(x2, y2, self.board_before)
        if (start_figure == ''):
            return False    # no figure at start position

        if ((x1 == 0 or x1 == 7) and (y1 == 0 or y1 == 7)) or ((x2 == 0 or x2 == 7) and (y2 == 0 or y2 == 7)):
            return False    # movement out of borders

        valid_movement = self.check_movement(start_figure, end_figure, x1, y1, x2, y2)
        return valid_movement


    def get_figure(self, x, y, board):
        '''
        Returns which figure is at given coordinates. Capitalization is retained.

        :param x: Integer
        :param y: Integer
        :param board: Board()
        :return: Char
        '''
        bit_position = self.get_bitposition(x, y)
        for fig in "bBkKqQ":
            try:
                player = "bl"
                fig_temp = fig
                if fig.isupper():
                    player = "wh"
                    fig_temp = fig.lower()
                fig_board = board.board[fig_temp] & board.board[player]
            except KeyError:    # catch Error, if such figure doesn't exist
                continue
            if (fig_board & bit_position > 0):
                return fig
        return ''


    def check_movement(self, fig1, fig2, x1, y1, x2, y2):
        '''
        Check if the the given figure at given coordinates can move to destination coordinates on the second figure.

        :param fig1: Figure at start-position
        :param fig2: Figure at destination (can be empty '')
        :param x1: start-position
        :param y1: start-position
        :param x2: destination
        :param y2: destination
        :return: True, if the movement is valid
        '''
        if not self.compare_figures(fig1, fig2):
            return False    # figures are not compatible

        player = self.board_before.player

        bit_pos2 = self.get_bitposition(x2, y2)

        if bit_pos2 & MoveBoard().generate(fig1, x1, y1, player, "JS") == 0:
            return False    # wrong figure movement

        if (fig1 in "bB"):  # check single-figure movement
            return self.check_single(fig1, fig2, x1, y1, x2, y2)

        return True


    def check_single(self, fig1, fig2, x1, y1, x2, y2):
        '''
        If the figure is a single one ('b' or 'B'), this funktion checks if it is
        a normal or attack-move and if the figure can move on the other figure.

        :param fig1: Figure from start-coordinates
        :param fig2: Figure at destination (can be '')
        :param x1: start-coordinates
        :param y1: start-coordinates
        :param x2: destination
        :param y2: destination
        :return: False, if it is another figure or a wrong move was made
        '''
        if fig1 not in "bB":
            return False

        x_diff = abs(x1-x2)
        y_diff = abs(y1-y2)

        # check for black/white because there needs to be a certain figure in case of attack/normal_move

        if x_diff != y_diff:
            # normal move
            if fig1.islower() and (fig2 == 'b' or fig2 == ''):   # black player
                return True
            elif fig1.isupper() and (fig2 == 'B' or fig2 == ''): # white player
                return True
        else:
            # attack move
            if fig1.islower() and fig2 in "BKQ":    # black player
                return True
            elif fig1.isupper() and fig2 in "bkq":  # white player
                return True

        return False


    def compare_figures(self, fig1, fig2):
        '''
        Check figures compability

        :param fig1: attacking figure
        :param fig2: attacked figure
        :return: can fig1 attack fig2? (True/False)
        '''
        if fig2 == '':
            return True
        if ("BKQ" in fig1 and fig2 == 'Q') or ("bkq" in fig1 and fig2 == 'q'):
            return False
        elif ("BKQ" in fig1 and fig2 == 'K') or ("bkq" in fig1 and fig2 == 'k'):
            return False
        return True


    def get_bitposition(self, x, y):
        return np.uint64(1) << np.uint64(8 * y + x)



class ValidCheckRacingKings: # will be ValidCheckRacingKings later
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
                if(CheckBetween().check(result[1], result[2], all_figures)):
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



def test_rk():
    board1 = "1k6/8/8/8/1q6/8/8/r7 w - - 3 2"
    board2 = "2k5/8/8/8/1q6/8/8/r7 b - - 4 5"
    board3 = "2k5/8/8/8/1q6/8/8/7r b - - 4 5"
    board4 = "3k4/8/8/8/1q6/8/8/r7 b - - 4 5"
    board5 = "8/8/1r6/8/8/8/q1bnNBRQ/krbnNBRK b - - 0 1"
    board6 = "8/8/1r6/8/5N2/8/q1bn1BRQ/krbnNBRK w - - 0 1"

    # should be true (king move)
    valid = ValidCheck().check(board1, board2)
    print("True?", valid)

    # should be false (too many moves)
    valid = ValidCheck().check(board1, board3)
    print("False?", valid)

    # should be false (too many steps)
    valid = ValidCheck().check(board1, board4)
    print("False?", valid)

    # should be true (ponny test)
    valid = ValidCheck().check(board5, board6)
    print("True?", valid)

def test_js():
    b1 = "1bbbbbb1/1b1k1b2/8/4b3/4B3/8/1B1KBB2/1BBB1BB1 b - - 0 12"
    b2 = "2bbbbb1/1k1k1b2/8/4b3/4B3/8/1B1KBB2/1BBB1BB1 w - - 0 13"
    m1 = "b8" + "b7"
    v1 = ValidCheck().check(b1, m1, "JS")
    print(v1)

# Only called if you directly execute this code
if __name__ == "__main__":
    test_rk()
    test_js()
