from bitboard import racing_kings


class ValidCheck():
    def get_position(self, bitboard):
        x = -1
        y = 0
        if bitboard == 0: # todo: check if only one bit is set (only one figure moves)
            return (-1, -1)
        while bitboard != 0:
            bitboard = bitboard >> 1
            x += 1
            if x >= 8:
                x = 0
                y += 1
        return (x, y)

    def get_direction(self, board_before, board_after):
        mix = board_before & board_after
        board_before = board_before - mix
        board_after  = board_after  - mix

        start_pos = self.get_position(board_before)
        end_pos   = self.get_position(board_after)

        if start_pos == (-1,-1) or end_pos == (-1,-1):
            return (0, 0)
        x_dir = end_pos[0] - start_pos[0]
        y_dir = end_pos[1] - start_pos[1]
        return (x_dir, y_dir)


# print("{0:b}".format(test))
game  = racing_kings()
check = ValidCheck()
#board = "r7/8/8/8/8/8/8/7r w"
#game.toBitBoard(board)
#state = game.cur_state
#game.printBoard(game.black_board['r'])
#print(game.black_board)

a1 = 0b00110000000010
a2 = 0b10110000000000
# print("{0:b}".format(a1))
# print("{0:b}".format(a2))
b = a1 & a2
b1 = a1 - b
b2 = a2 - b

print("start position: ", check.get_position(b1))
print("destination:    ", check.get_position(b2))

move = check.get_direction(a1,a2)
print("move (x,y):     ",move)

# TODO: check if only one figure moves
# TODO: check if figure is not out of bounds
# TODO: check if the translation is right (direction, board orientation)
# TODO: add actual check

# print(game.cur_state)
# before = "8/8/8/1K6/8/8/8/8 w"
# after  = "8/8/8/2K5/8/8/8/8 w"
