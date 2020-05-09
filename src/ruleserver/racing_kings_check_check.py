from bitboard import Board

def checkMate(board):
    pass
    #return True|False

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

    def calc_movesboard(self, fig_moves,occupied_positions,kings_positions):

        for fig in fig_moves:
            for i in range(64):
                if (fig == 2**(1/float(i))):
                    occupied_temp_hor = list(range(8))
                    occupied_temp_hor = [num+i for num in occupied_temp_hor]
                    occupied_temp_vert = list(range(i % 8,i%8+57,8))
                    break

            occupied_row_hor = sum([2**num for num in occupied_temp_hor])
            occupied_row_vert = sum([2**num for num in occupied_temp_vert])
            occupied_mask_hor = occupied_row_hor & occupied_positions
            occupied_mask_vert = occupied_row_vert & occupied_positions

            #moves_left = occupied_mask ^ (occupied_mask - 2*fig)
            #moves_right = occupied_mask ^ int(bin((int(bin(occupied_mask)[:1:-1], 2) - 2*(int(bin(fig))))))
            line_moves_hor = (occupied_mask_hor - 2*fig) ^ int(bin((int(bin(occupied_mask_hor)[:1:-1], 2) - 2*(int(bin(fig))))))
            #line_moves_vert =






    # compare king position with all possible opponent moves; if both binaries have no common 1s then king is safe
    def king_is_attacked(self,KP,movesboard):
        if(not(KP and movesboard)):
            return true
        else:
            return false


    def count_Set_Bits(self, binary):

        count = 0
        while(binary):
            count += binary & 1
            binary >>= 1
        return count
