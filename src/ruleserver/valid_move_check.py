import numpy as np
from bitboard import Board


class ValidCheck():

    # Calcualtes the position of the moved figure
    # @board_before: FEN-board before the move
    # @board_after:  FEN-board after the move
    # @return: figure-type, before-position, after-position    example: 'r', (1,0), (2,3)
    def calc_positions(self, board_before, board_after):
        before = Board(board_before)
        after = Board(board_after)

        figure = self.get_figure(before, after)
        if figure == "":
            return figure, (-1, -1), (-1, -1)

        if after.player == "w":
            bit_before = before.board[figure] & before.board['wh']
            bit_after  = after.board[figure]  & after.board['wh']
        else:
            bit_before = before.board[figure] & before.board['bl']
            bit_after  = after.board[figure]  & after.board['bl']

        mix = bit_before & bit_after
        bit_before = bit_before - mix
        bit_after = bit_after - mix

        # check if only one figure moves
        if (self.count_bits(bit_before) > 1) or (self.count_bits(bit_after) > 1):
            return "", (-1, -1), (-1, -1)

        # todo?: check if figure of other player wasn't moved

        start_pos = self.get_position(bit_before)
        end_pos = self.get_position(bit_after)

        return figure, start_pos, end_pos

    # get the figure that was moved
    # return "" if: - no figure moved
    #               - too many moves
    def get_figure(self, before, after):
        player_mask = 0
        fig_moved = 0
        curr_fig = ""
        if after.player == 'w':
            player_mask = after.board['wh']
        elif after.player == "b":
            player_mask = after.board['bl']
        for fig in "kbrnq":
            try:
                fig_board_before = before.board[fig] & player_mask
                fig_board_after = after.board[fig] & player_mask
            except KeyError:    # catch Error, if such figure doesn't exist
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
            bitboard = bitboard >> np.uint64(1)
            x += 1
            if x >= 8:
                x = 0
                y += 1
        return (x, y)

    def count_bits(self, number):
        i = 0
        while (number > 0):
            i += number & np.uint64(1)
            number = number >> np.uint64(1)
        return i

    # Check if the mofe of the specific figure is correct
    # @figure: the figure, as char. Ex.: 'k', 'b', ...
    # @(x, y): startposition
    # @(target_x, target_y): target position
    # @return: valid (True) or not valid (False) move
    def check_valid_move(self, figure, x, y, target_x, target_y):
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
    check = ValidCheck()
    board1 = "1r6/8/8/8/1q6/8/8/r7 w - - 3 2"
    board2 = "2r5/8/8/8/1q6/8/8/r7 b - - 4 5"

    move = check.calc_positions(board1, board2)
    print(move)

    check.check_valid_move(move[0], (move[1])[0], (move[1])[1], (move[2])[0], (move[2])[1])


# TODO: check if only one figure moves - ok
# TODO: check if figure is not out of bounds -> happens before the bitboard-conversion
# TODO: check if the translation is right (direction, board orientation) -> irrelevant
# TODO: add actual check ->HeyiLee
