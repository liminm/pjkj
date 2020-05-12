#from bitboard import racing_kings
import math

class KingIsAttackedCheck():

    def find_indiv_figs(self, WR, WN, WB, WQ, WK, BR, BN, BB, BQ, BK):

        moves_arr = [WR,WN,WB,WQ,WK,BR,BN,BB,BQ, BK]
        fig_moves = []
        # find all positions of figures of a type
        # eg for all white knights on starting position: indiv_moves_fig = [16,2048]
        for moves in moves_arr:
            count_bin_pos = 0
            indiv_moves_fig = []
            while(moves):
                if(moves & 1):
                    indiv_moves_fig.append(2**count_bin_pos)
                count_bin_pos += 1
                moves >>= 1
            fig_moves.append(indiv_moves_fig)
        return fig_moves

    def set_occupied_pos(self,WR,WN,WB,WQ,WK,BR,BN,BB,BQ):
        occupied_positions = WR+WN+WB+WQ+WK+BR+BN+BB+BQ
        return occupied_positions

    def calc_movesboard(self, fig_moves,occupied_positions):
        # line moveset diagonal, vertical, horizontal
        for fig in fig_moves:
            pos_exp = math.log2(fig)
            hor_range = list(range(8))
            for i in range(8):
                if(pos_exp in hor_range):
                    break
                hor_range = [num+8 for num in hor_range]
            #TODO handle edge cases
            diag_minus = (list(range(pos_exp,0,-9)) + list(range(pos_exp,64,9)))
            diag_right_border_values = list(range(7,64,8))
            diag_left_border_values = list(range(0,57,8))
            diag_plus = list(range(pos_exp, 64, 7)) + list(range(pos_exp, 0, -7))

            # delete moves overstepping edge cases
            if(bool(set(diag_minus) & set(diag_left_border_values))):
                common_val = [num for num in diag_minus if num in diag_left_border_values]
                out_of_board_vals = list(range(common_val[0]),64,9).remove(common_val[0])
                diag_minus += [num for num in diag_minus not in out_of_board_vals]
            if (bool(set(diag_minus) & set(diag_right_border_values))):
                common_val = [num for num in diag_minus if num in diag_right_border_values]
                out_of_board_vals = list(range(common_val[0]),-1,-9).remove((common_val[0]))
                diag_minus = [num for num in diag_minus not in out_of_board_vals]

            if (bool(set(diag_plus) & set(diag_right_border_values))):
                common_val = [num for num in diag_plus if num in diag_right_border_values]
                out_of_board_vals = list(range(common_val[0]), 64, 7).remove(common_val[0])
                diag_plus = [num for num in diag_plus not in out_of_board_vals]
            if (bool(set(diag_plus) & set(diag_left_border_values))):
                common_val = [num for num in diag_plus if num in diag_left_border_values]
                out_of_board_vals = list(range(common_val[0]), -1, -7).remove((common_val[0]))
                diag_plus = [num for num in diag_plus not in out_of_board_vals]

            occupied_diag_minus = sum([2**num for num in diag_minus])
            occupied_diag_plus = sum([2**num for num in diag_plus])
            mask_diag_plus_temp = occupied_diag_plus & occupied_positions
            mask_diag_minus_temp = occupied_diag_minus & occupied_positions



            vert_range = list(range(pos_exp % 8,pos_exp%8+57,8))
            occupied_hor = sum([2**num for num in hor_range])
            occupied_vert = sum([2**num for num in vert_range])
            mask_hor = occupied_hor & occupied_positions
            mask_vert_temp = occupied_vert & occupied_positions
            mask_vert = 0
            mask_diag_minus = 0
            mask_diag_plus = 0
            fig_slider_hor = 0
            # reverse fig bitboard
            fig_slider_vert = 0
            # use += in case fig is 0
            for i in range(8):
                if(11111111<<(8*i) & fig):
                    fig_slider_vert = (2**i)
                if(11111111<<(8*i) & fig):
                    fig_slider_hor = (11111111<<(8*i) & fig)>>(8*i)
                if(11111111<<(8*i) & fig):
                    fig_slider_diag_minus = (2**i)
                if(11111111<<(8*i) & fig):
                    fig_slider_diag_plus = (2**i)
                if(11111111<<(8*i) & mask_vert_temp):
                    mask_vert += (2**i)
                if(11111111<<(8*i) & mask_diag_minus_temp):
                    mask_diag_minus += (2**i)
                if(11111111<<(8*i) & mask_diag_plus_temp):
                    mask_diag_plus += (2**i)


            line_moves_hor = (mask_hor - 2*fig_slider_hor) ^ int(bin((int(bin(mask_hor)[:1:-1], 2) - 2*(int(bin(fig_slider_hor))))))
            line_moves_vert = (mask_vert - 2*fig_slider_vert) ^ int(bin((int(bin(mask_vert)[:1:-1], 2) - 2*(int(bin(fig_slider_vert))))))
            line_moves_diag_minus = (mask_diag_minus - 2*fig_slider_diag_minus) ^ int(bin((int(bin(mask_diag_plus)[:1:-1], 2) - 2*(int(bin(fig_slider_diag_minus))))))
            line_moves_diag_plus = (mask_diag_plus - 2*fig_slider_diag_plus) ^ int(bin((int(bin(mask_diag_plus)[:1:-1], 2) - 2*(int(bin(fig_slider_diag_plus))))))

            #king moveset
            #knight moveset

            # temp value TODO insert real King bitboard
            fig = 0
            king_mask = (fig>>1) + (fig<<1) + (fig>>8) + (fig<<8) + (fig<<7) + (fig<<9) + (fig>>9) + (fig>>7)
            knight_mask = (fig>>17) + (fig>>15) + (fig>>10) + (fig>>6) + (fig<<6) + (fig<<10) + (fig<<15) + (fig<<17)
            if(pos_exp in list(range(0,57,8))):
                king_mask -= (fig<<1) + (fig>>7) + (fig<<9)
                knight_mask -= (fig>>15) + (fig>>6) + (fig<<10) + (fig<<17)
            if(pos_exp in list(range(7,64,8))):
                king_mask -= (fig>>1) + (fig>>9) + (fig<<7)
                knight_mask -= (fig>>17) + (fig>>10) + (fig<<6) + (fig<<15)
            if(pos_exp in list(range(0,8,1))):
                king_mask -= (fig<<8)
                knight_mask -= (fig<<6) + (fig<<10) + (fig<<15) + (fig<<17)
            if(pos_exp in list(range(7,64,8))):
                king_mask -= (fig>>1)
                knight_mask -= (fig>>17) + (fig>>15) + (fig>>10) + (fig>>6)
            if(pos_exp in list(range(9,57,8))):
                knight_mask -= (fig>>6) + (fig<<10)
            if(pos_exp in list(range(9,15,1))):
                knight_mask -= (fig<<17) + (fig<<15)
            if(pos_exp in list(range(14,62,8))):
                knight_mask -= (fig>>10) + (fig<<6)
            if(pos_exp in list(range(49,55,1))):
                knight_mask -= (fig>>17) + (fig>>15)

            king_moves = king_mask
            knight_moves = knight_mask



    # compare king position with all possible opponent moves; if both binaries have no common 1s then king is safe
    def king_is_attacked(self,KP,movesboard):
        if(not(KP & movesboard)):
            return True
        else:
            return False


    def count_Set_Bits(self, binary):

        count = 0
        while(binary):
            count += binary & 1
            binary >>= 1
        return count
