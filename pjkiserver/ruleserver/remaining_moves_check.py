# from bitboard import racing_kings
import math
import numpy as np
from .racing_kings_check_check import Checkmate as Checkmate2

def noMovesPossible(board):
    cm = Checkmate()

    player = "playerA"
    if board.player == "b":
        player = "playerB"

    return cm.noMovesPossible(board.board["q"], board.board["k"], board.board["b"], board.board["n"], board.board["r"],
                        board.board["wh"], board.board["bl"], player)

def bmatrix(bitboard):
    save = bitboard
    bitboard = '{:>064b}'.format(bitboard)
    for c in range(7,0,-1):
        print(bitboard[(7-c)*8:-(c*8)])
    print(bitboard[7 * 8:])
    print(len(bitboard))
    print("\n")
    if (len(bitboard) == 83):
        print(save)

class Checkmate():

    def find_indiv_figs(self, moves_arr):
        # 1. Queen 2. King 3. Bishop 4. Knight 5. Rook

        fig_moves = []
        # find all positions of figures of a type
        # eg for all white knights on starting position: indiv_moves_fig = [16,2048]
        for moves in moves_arr:
            count_bin_pos = 0
            indiv_figs = []

            while (moves):
                if (moves & 1):
                    indiv_figs.append(2 ** count_bin_pos)
                    # print(2**count_bin_pos)
                    # print(indiv_figs)
                count_bin_pos += 1
                moves >>= 1
            fig_moves.append(indiv_figs)
        # 1. Queen 2. King 3. Bishop 4. Knight 5. Rook
        # print(fig_moves)

        return fig_moves

    def set_occupied_pos(self, q, k, b, n, r):
        occupied_positions = q + k + b + n + r
        return occupied_positions

    def calc_movesboard(self, fig_moves, occupied_positions):
        # line moveset diagonal, vertical, horizontal
        moves_board = 0
        # print(fig_moves)
        for i in range(0, len(fig_moves)):
            for fig in fig_moves[i]:
                #print("i: ", i)

                # print("Fig: ", fig)
                pos_exp = int(math.log2(fig))
                #print("Position Exponent: ", pos_exp)

                if (i == 1):
                    king_mask = (fig >> 1) + (fig << 1) + (fig >> 8) + (fig << 8) + (fig << 7) + (fig << 9) + (
                                fig >> 9) + (fig >> 7)
                    if (pos_exp in list(range(1, 7, 1))):
                        king_mask -= (fig >> 9) + (fig >> 8) + (fig >> 7)
                    if (pos_exp in list(range(57, 63, 1))):
                        king_mask -= (fig << 9) + (fig << 8) + (fig << 7)
                    if (pos_exp in list(range(8, 49, 8))):
                        king_mask -= (fig >> 9) + (fig >> 1) + (fig << 7)
                    if (pos_exp in list(range(15, 56, 8))):
                        king_mask -= (fig >> 7) + (fig << 1) + (fig << 9)
                    if (pos_exp == 0):
                        king_mask -= (fig >> 9) + (fig >> 8) + (fig >> 7) + (fig >> 1) + (fig << 7)
                    if (pos_exp == 7):
                        king_mask -= (fig >> 9) + (fig >> 8) + (fig >> 7) + (fig << 1) + (fig << 9)
                    if (pos_exp == 56):
                        king_mask -= (fig << 9) + (fig << 8) + (fig << 7) + (fig >> 9) + (fig >> 1)
                    if (pos_exp == 63):
                        king_mask -= (fig << 9) + (fig << 8) + (fig << 7) + (fig << 1) + (fig >> 7)

                    #bmatrix(king_mask)

                    #print("King Mask: ",king_mask)
                    #print(bin(king_mask))

                    #moves_board = moves_board | king_mask
                    moves_board = moves_board

                if (i == 3):
                    knight_move = (fig >> 17) + (fig >> 15) + (fig >> 10) + (fig >> 6) + (fig << 6) + (fig << 10) + (
                                fig << 15) + (fig << 17)

                    if(pos_exp in list(range(1,7,1))):
                        knight_move -= (fig >> 6) + (fig >> 10) + (fig >> 15) + (fig >> 17)
                    if(pos_exp in list(range(57,63,1))):
                        knight_move -= (fig << 17) + (fig << 15) + (fig << 10) + (fig << 6)
                    if (pos_exp in list(range(8, 49, 8))):
                        knight_move -= (fig << 15) + (fig << 6) + (fig >> 10) + (fig >> 17)
                    if (pos_exp in list(range(15, 56, 8))):
                        knight_move -= (fig >> 15) + (fig >> 6) + (fig << 10) + (fig << 17)
                    if (pos_exp == 0):
                        knight_move -= (fig >> 17) + (fig >> 15) + (fig >> 10) + (fig >> 6) + (fig << 6) + (fig << 15)
                    if (pos_exp == 7):
                        knight_move -= (fig >> 17) + (fig >> 15) + (fig >> 10) + (fig >> 6) + (fig << 10) + (fig << 17)
                    if (pos_exp == 56):
                        knight_move -= (fig << 17) + (fig << 15) + (fig << 10) + (fig << 6) + (fig >> 10) + (fig >> 17)
                    if (pos_exp == 63):
                        knight_move -= (fig << 17) + (fig << 15) + (fig << 10) + (fig << 6) + (fig >> 6) + (fig >> 15)

                    if (pos_exp in list(range(10, 14, 1))):
                        knight_move -= (fig >> 17) + (fig >> 15)
                    if (pos_exp in list(range(49, 53, 1))):
                        knight_move -= (fig << 17) + (fig << 15)
                    if (pos_exp in list(range(17, 42, 8))):
                        knight_move -= (fig >> 10) + (fig << 6)
                    if (pos_exp in list(range(22, 47, 8))):
                        knight_move -= (fig << 10) + (fig >> 6)
                    if (pos_exp in list(range(50, 53, 1))):
                        knight_move -= (fig << 17) + (fig << 15)
                    if (pos_exp == 9):
                        knight_move -= (fig >> 17) + (fig >> 15) + (fig >> 10) + (fig << 6)
                    if (pos_exp == 14):
                        knight_move -= (fig >> 17) + (fig >> 15) + (fig >> 6) + (fig << 10)
                    if (pos_exp == 49):
                        knight_move -= (fig >> 10) + (fig << 6) + (fig >> 15) + (fig >> 17)
                    if (pos_exp == 54):
                        knight_move -= (fig >> 6) + (fig << 10) + (fig >> 15) + (fig >> 17)

                    moves_board = moves_board | knight_move

                if (i == 2 or i == 0):
                    left_border = list(range(7, 64, 8))
                    right_border = list(range(0, 57, 8))

                    diag_minus_range = [pos_exp]
                    diag_plus_range = [pos_exp]

                    for j in range(8):
                        if (pos_exp + 9 * j not in left_border and (pos_exp + 9 * j <= 63 and pos_exp + 9 * j >= 0)):
                            diag_minus_range.append(pos_exp + 9 * j)
                        elif (pos_exp + 9 * j <= 63 and pos_exp + 9 * j >= 0) and (
                                len(set(diag_minus_range) & set(left_border)) == 0):
                            diag_minus_range.append(pos_exp + 9 * j)
                            break
                        else:
                            break

                    for j in range(8):
                        if (pos_exp - 9 * j not in right_border and (pos_exp - 9 * j <= 63 and pos_exp - 9 * j >= 0)):
                            diag_minus_range.append(pos_exp - 9 * j)
                        elif (pos_exp - 9 * j <= 63 and pos_exp - 9 * j >= 0) and (
                                len(set(diag_minus_range) & set(right_border)) == 0):
                            diag_minus_range.append(pos_exp - 9 * j)
                            break
                        else:
                            break

                    for j in range(8):
                        if (pos_exp + 7 * j not in right_border and (pos_exp + 7 * j <= 63 and pos_exp + 7 * j >= 0)):
                            diag_plus_range.append(pos_exp + 7 * j)
                        elif (pos_exp + 7 * j <= 63 and pos_exp + 7 * j >= 0) and (
                                len(set(diag_plus_range) & set(right_border)) == 0):
                            diag_plus_range.append(pos_exp + 7 * j)
                            break
                        else:
                            break

                    for j in range(8):
                        if (pos_exp - 7 * j not in left_border and (pos_exp - 7 * j <= 63 and pos_exp - 7 * j >= 0)):
                            diag_plus_range.append(pos_exp - 7 * j)
                        elif (pos_exp - 7 * j <= 63 and pos_exp - 7 * j >= 0) and (
                                len(set(diag_plus_range) & set(left_border)) == 0):
                            diag_plus_range.append(pos_exp - 7 * j)
                            break
                        else:
                            break

                    diag_minus_range = list(set(diag_minus_range))
                    diag_minus_range.sort()
                    diag_plus_range = list(set(diag_plus_range))
                    diag_plus_range.sort()

                    diag_minus_move = sum([2 ** num for num in diag_minus_range])
                    diag_plus_move = sum([2 ** num for num in diag_plus_range])
                    diag_minus_mask = diag_minus_move & occupied_positions
                    diag_plus_mask = diag_plus_move & occupied_positions
                    diag_minus_mask = sum([2 ** exp for exp in range(8) if (((255 << (8 * exp)) & diag_minus_mask))])
                    #delete ending 0s as out of range of slider
                    diag_minus_mask = diag_minus_mask >> int(diag_minus_range[0] / 8)
                    diag_plus_mask = sum([2 ** exp for exp in range(8) if ((255 << (8 * exp) & diag_plus_mask))])
                    #delete ending 0s as out of range of slider
                    diag_plus_mask = diag_plus_mask >> int(diag_plus_range[0] / 8)

                    diag_minus_fig_slider = sum([(2 ** column) for column in range(8) if (255 << (8 * column) & fig)])
                    diag_plus_fig_slider = sum([(2 ** column) for column in range(8) if (255 << (8 * column) & fig)])
                    #delete ending 0s as out of range of slider
                    diag_minus_fig_slider = diag_minus_fig_slider >> int(diag_minus_range[0] / 8)
                    diag_plus_fig_slider = diag_plus_fig_slider >> int(diag_plus_range[0] / 8)

                    form_string = '{:0' + str(len(diag_minus_range)) + 'b}'

                    # left side moves
                    # check if fig slider is not out of bounds (8bit)
                    if (diag_minus_mask >= 2 * diag_minus_fig_slider):
                        diag_minus_left_line_moves = diag_minus_mask - 2 * diag_minus_fig_slider
                    # reverse the bits and subtract (difference -1)
                    else:
                        diag_minus_left_line_moves = sum([2 ** num for num in range(len(diag_minus_range))]) - (2 * diag_minus_fig_slider - diag_minus_mask) + 1

                    #right side moves
                    if (int(form_string.format(diag_minus_mask)[::-1], 2) >= 2 * int(form_string.format(diag_minus_fig_slider)[::-1], 2)):
                        diag_minus_right_line_moves = int(form_string.format(int(form_string.format(np.uint(diag_minus_mask))[::-1], 2) - 2 * int(form_string.format(np.uint(diag_minus_fig_slider))[::-1], 2))[::-1], 2)
                    else:
                        diag_minus_right_line_moves = int(form_string.format(sum([2 ** num for num in range(len(diag_minus_range))]) - ((2 * int(form_string.format(np.uint8(diag_minus_fig_slider))[::-1], 2)) - int(form_string.format(np.uint8(diag_minus_mask))[::-1], 2)) + 1)[::-1], 2)

                    diag_minus_line_moves = diag_minus_left_line_moves ^ diag_minus_right_line_moves

                    form_string = '{:0' + str(len(diag_plus_range)) + 'b}'


                    # left side moves
                    # check if fig slider is not out of bounds (8bit)
                    if (diag_plus_mask >= 2 * diag_plus_fig_slider):
                        diag_plus_left_line_moves = diag_plus_mask - 2 * diag_plus_fig_slider
                    # reverse the bits and subtract (difference -1)
                    else:
                        diag_plus_left_line_moves = sum([2 ** num for num in range(len(diag_plus_range))]) - (2 * diag_plus_fig_slider - diag_plus_mask) + 1

                    #right side moves
                    if (int(form_string.format(diag_plus_mask)[::-1], 2) >= 2 * int(form_string.format(diag_plus_fig_slider)[::-1], 2)):
                        diag_plus_right_line_moves = int(form_string.format(int(form_string.format(np.uint(diag_plus_mask))[::-1], 2) - 2 * int(form_string.format(np.uint(diag_plus_fig_slider))[::-1], 2))[::-1], 2)
                    else:
                        diag_plus_right_line_moves = int(form_string.format(sum([2 ** num for num in range(len(diag_plus_range))]) - ((2 * int(form_string.format(np.uint8(diag_plus_fig_slider))[::-1], 2)) - int(form_string.format(np.uint8(diag_plus_mask))[::-1], 2)) + 1)[::-1], 2)

                    diag_plus_line_moves = diag_plus_left_line_moves ^ diag_plus_right_line_moves

                    form_string_minus = '{:>0' + str(len(diag_minus_range)) + 'b}'
                    form_string_plus = '{:>0' + str(len(diag_plus_range)) + 'b}'

                    diagonal_moves = sum([2 ** (diag_minus_range[0] + (exp*9)) for exp in range(len(diag_minus_range) ) if (form_string_minus.format(diag_minus_line_moves)[::-1][exp] == '1') ])  | sum([2 ** (diag_plus_range[0] + (exp*7)) for exp in range(len(diag_plus_range) ) if (form_string_plus.format(diag_plus_line_moves)[::-1][exp] == '1') ])

                    #print("Diagonal Minus Range: ", diag_minus_range)
                    #print("Diagonal Plus Range: ", diag_plus_range)
                    #print("Diagonal Minus Move: ", diag_minus_move)
                    #print("Diagonal Plus Move: ", diag_plus_move)
                    #print("Diagonal Minus Mask: ", diag_minus_mask)
                    #print("Diagonal Plus Mask: ", diag_plus_mask)
                    #print("Diagonal Minus Fig Slider: ", diag_minus_fig_slider)
                    #print("Diagonal Plus Fig Slider: ", diag_plus_fig_slider)
                    #print("Diagonal Minus Line Moves: ", diag_minus_line_moves)
                    #print("Diagonal Plus Line Moves: ", diag_plus_line_moves)
                    #print("Diagonal Moves: ", diagonal_moves)
                    #bmatrix(diagonal_moves)

                    moves_board = moves_board | diagonal_moves




                if (i == 4 or i == 0):
                    hor_fig_slider = sum(
                        [(((255 << (8 * row)) & fig) >> (8 * row)) for row in range(8) if (255 << (8 * row) & fig)])
                    vert_fig_slider = sum([(2 ** column) for column in range(8) if (255 << (8 * column) & fig)])
                    hor_range = [num + (8 * (int(pos_exp / 8))) for num in list(range(8))]
                    vert_range = list(range(pos_exp % 8, pos_exp % 8 + 57, 8))
                    hor_move = sum([2 ** (num) for num in hor_range ])
                    vert_move = sum([2 ** num for num in vert_range])
                    # all occupied positions in move mask
                    hor_mask = (hor_move & occupied_positions) >> 8* int(pos_exp / 8 )
                    vert_mask = vert_move & occupied_positions
                    vert_mask = sum([2 ** exp for exp in range(8) if ((255 << (8 * exp) & vert_mask))])

                    hor_line_moves = (np.uint8(hor_mask - 2 * hor_fig_slider).item()) ^ int('{:08b}'.format(np.uint8(
                        int('{:08b}'.format(hor_mask)[::-1], 2) - 2 * int('{:08b}'.format(hor_fig_slider)[::-1], 2)))[::-1], 2)

                    #bmatrix((hor_line_moves << (8 * (int(pos_exp / 8)))))


                    vert_line_moves = (np.uint8(vert_mask - 2 * vert_fig_slider).item()) ^ int('{:08b}'.format(np.uint8(
                        int('{:08b}'.format(vert_mask)[::-1], 2) - 2 * int('{:08b}'.format(vert_fig_slider)[::-1], 2)))[
                                                                                        ::-1], 2)

                    rook_moves = ((hor_line_moves << (8 * (int(pos_exp / 8)))) | sum([2 ** ((pos_exp % 8) + 8 * num) for num in range(8) if(((int('{:>08b}'.format((vert_line_moves >> num))[::-1], 2)) >> (7)) != 0)]))

                    #bmatrix(hor_line_moves << (8 * (int(pos_exp / 8))))
                    #bmatrix(rook_moves)

                    moves_board = moves_board | rook_moves

                    # print("Horizontal mask of occupied figs: ", hor_mask)
                    # print("Vertical mask of occupied figs: ", vert_mask)
                    # print("Vertical fig slider: ", vert_fig_slider)
                    # print("Horizontal fig slider: ", hor_fig_slider)
                    # print("Horizontal range: ",hor_range)
                    # print("Vertical range: ", vert_range)
                    # print("Horizontal occupied: ",hor_move)
                    # print("Vertical occupied: ",vert_move)
                    # print("Horizontal line moves: ", hor_line_moves)
                    # print("Vertical line moves: ", vert_line_moves)

        #print ("Moves board: ",moves_board)
        return moves_board

    # compare king position with all possible opponent moves; if both binaries have no common 1s then king is safe
    def king_is_attacked(self, own_king, enemy_king, own_move_board, enemy_move_board):
        if (enemy_king & own_move_board):
            return True
        elif (own_king & enemy_move_board):
            return True
        else:
            return False

    def noMovesPossible(self, q, k, b, n, r, wh, bl, player):
        board = Checkmate()
        bitboards = [q,k,b,n,r,wh,bl]
        for i in range(len(bitboards)):
            if(type(bitboards[i]).__module__ == np.__name__ ):
                bitboards[i] = bitboards[i].item()

        q = bitboards[0]
        k = bitboards[1]
        b = bitboards[2]
        n = bitboards[3]
        r = bitboards[4]
        wh = bitboards[5]
        bl = bitboards[6]

        white_figs, black_figs = board.split_color_figs(q, k, b, n, r, wh, bl)
        occupied_positions = board.set_occupied_pos(q, k, b, n, r)

        white_move_board = board.calc_movesboard(board.find_indiv_figs(white_figs), occupied_positions)
        black_move_board = board.calc_movesboard(board.find_indiv_figs(black_figs), occupied_positions)

        if (player == "playerA"):
            own_king = k & wh
            enemy_king = k & bl
            own_move_board = white_move_board
            enemy_move_board = black_move_board
        else:
            own_king = k & bl
            enemy_king = k & wh
            own_move_board = black_move_board
            enemy_move_board = white_move_board

        #print(own_move_board)
        #print(wh)
        #print(enemy_move_board)

        maxb = 18446744073709551615

        naOrnb = (maxb - own_move_board) | (maxb - wh)
        aAndnb = (own_move_board) & (maxb - wh)
        aOrnb = own_move_board | (maxb - wh)
        aOrb = own_move_board | wh

        # (-a or -b) and (a and -b) and (a or -b) and (a or b)
        own_move_board_pure = naOrnb & aAndnb & aOrnb & aOrb


        #print(own_move_board_pure)

        # do a check for king in check

        pos_exp = int(math.log2(own_king))
        king_mask = (own_king >> 1) + (own_king << 1) + (own_king >> 8) + (own_king << 8) + (own_king << 7) + (
                    own_king << 9) + (
                            own_king >> 9) + (own_king >> 7)
        if (pos_exp in list(range(1, 7, 1))):
            king_mask -= (own_king >> 9) + (own_king >> 8) + (own_king >> 7)
        if (pos_exp in list(range(57, 63, 1))):
            king_mask -= (own_king << 9) + (own_king << 8) + (own_king << 7)
        if (pos_exp in list(range(8, 49, 8))):
            king_mask -= (own_king >> 9) + (own_king >> 1) + (own_king << 7)
        if (pos_exp in list(range(15, 56, 8))):
            king_mask -= (own_king >> 7) + (own_king << 1) + (own_king << 9)
        if (pos_exp == 0):
            king_mask -= (own_king >> 9) + (own_king >> 8) + (own_king >> 7) + (own_king >> 1) + (own_king << 7)
        if (pos_exp == 7):
            king_mask -= (own_king >> 9) + (own_king >> 8) + (own_king >> 7) + (own_king << 1) + (own_king << 9)
        if (pos_exp == 56):
            king_mask -= (own_king << 9) + (own_king << 8) + (own_king << 7) + (own_king >> 9) + (own_king >> 1)
        if (pos_exp == 63):
            king_mask -= (own_king << 9) + (own_king << 8) + (own_king << 7) + (own_king << 1) + (own_king >> 7)


        # if moveboard is 0 then no move is possible
        if((own_move_board_pure | king_mask)  == 0):
            #if result == 1 then no move is possible
            result = True
            return result
        else:
            #if result == 0 then move is possible

            if (player == "playerA"):
                king_mask = king_mask & ~ wh
            else:
                king_mask = king_mask & ~ bl

            # If there are other moves possible besides the king or If movesboard (without king moves) & king moves has overlap that means a figure which is not a king can move return False
            if(own_move_board_pure or own_move_board_pure & king_mask ):
                return False

            nmove = 1
            board = Checkmate2()
            king_in_check_all_dir = 1

            for i in range(64):

                nq = q
                nk = (k & ~ own_king) | nmove
                nb = b
                nn = n
                nr = r



                if(king_mask & nmove):

                    if(player == "playerA"):
                        nwh = (wh & ~ own_king) | nmove
                        nbl = bl & ~nmove

                        if (nmove & q):
                            nq = q & ~ nmove
                        if (nmove & k):
                            nk = (k & ~ own_king) | nmove
                        if (nmove & b):
                            nb = b & ~ nmove
                        if (nmove & n):
                            nn = n & ~ nmove
                        if (nmove & r):
                            nr = r & ~ nmove

                    else:
                        nbl = (bl & ~ own_king) | nmove
                        nwh = wh & ~nmove

                        if (nmove & q):
                            nq = q & ~ nmove
                        if (nmove & k):
                            nk = (k & ~ own_king) | nmove
                        if (nmove & b):
                            nb = b & ~ nmove
                        if (nmove & n):
                            nn = n & ~ nmove
                        if (nmove & r):
                            nr = r & ~ nmove

                    if(board.checkmate(nq, nk, nb, nn, nr, nwh, nbl, player) == False):
                        king_in_check_all_dir = 0

                nmove = nmove << 1

            if(king_in_check_all_dir == 0):
                result = False
            else:
                result = True


        return result

    def split_color_figs(self, q, k, b, n, r, wh, bl):
        # 1. Queen 2. King 3. Bishop 4. Knight 5. Rook
        white_figs = [q & wh, k & wh, b & wh, n & wh, r & wh]
        black_figs = [q & bl, k & bl, b & bl, n & bl, r & bl]

        return white_figs, black_figs



if __name__ == '__main__':
    board = Checkmate()


    # 1. Queen 2. King 3. Bishop 4. Knight 5. Rook 6. White 7. Black 8. Player
    # Numbers set to start position
    # result == True if King is in chess; False if King is not attacked
    result = board.noMovesPossible(129, np.uint64(33024), np.uint64(9252), np.uint64(6168), np.uint64(16962), np.uint64(3855), np.uint64(61680), 'playerA')
    #print(result)