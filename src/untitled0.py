"""
Notation:
a trun will alway be FEN i.e: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1    
we start at the top row number 8
small letters for the black figuees and capital letters for white 
r - rook (Turm), n - knight(Springer), b - bishop(laeufer), q - queen (Koenigin), k - king (koenig)
--> racing king is not played with pawns
an 8 is tells us the amount of empty fields, if we have a king on the third tile from the left : 2k5
the first letter after the board description is the current player
the KQkq we can ignore and will be replaced with - (chess only rules)
the - wont be changed (again chess rules that do not apply to racing kings)
the 0 is the amount of halfturns since the last figure was killed TODO languge 
1 the round number that is currently played
"""
class racing_kings():
    
    def __init__(self,  board = None):
        self.start = "8/8/8/8/8/8/krbnKRBN/qrbnQRBN w - - 0 1"
        self.turns = []
        self.player = ''
        self.figures = ["krbnqKRBNQ"]
        self.black_board = {
                'k': 0<<63,
                'b': 0<<63,
                'n': 0<<63,
                'r': 0 << 63,
                'q': 0<<63,
                }
        self.white_board = {
                'K': 0 << 63,
                'B': 0<<63,
                'N': 0 << 63,
                'R': 0<<63,
                'Q': 0 << 63,
                }
        self.cur_state = 0<<63
        self.black_board_last = {
                'k': 0<<63,
                'b': 0<<63,
                'n': 0<<63,
                'r': 0 << 63,
                'q': 0<<63,
                }
        self.white_board_last = {
                'K': 0 << 63,
                'B': 0<<63,
                'N': 0 << 63,
                'R': 0<<63,
                'Q': 0 << 63,
                }
        self.last_state = 0<<63
        
        if board == None :
            self.toBitBoard(self.start)
            self.turns.append(self.start)
            self.player = 'w'
        else :
            self.toBitBoard(board)
            self.turns.append(board)
            parts = board.split()
            
            self.player = parts[1]
        
    def toBitBoard(self, turn):
        """
        turn will be a FEN string, where we will take the the first, second, fith and sixth part
        """
        pos = 0
        turn_parts = turn.split()
        self.last_state = self.cur_state
        self.black_board_last = self.black_board.copy()
        self.white_board_last = self.white_board.copy()
      
        self.resetBoard()
        
        for elem in turn_parts[0]:
            if ord(elem) < 57 and ord(elem) > 48:  #we have a number with 1-8 49-56
                pos += int(elem)
            else: 
                if elem == 'k':
                    self.black_board['k'] = 1 << pos
                    self.cur_state += 1<< pos
                elif elem == 'b':
                    self.black_board[elem] = self.black_board.get(elem,0) +  1 << pos 
                    self.cur_state += 1<< pos
                elif elem == 'r':
                    self.black_board[elem] = self.black_board.get(elem,0) +  1 << pos 
                    self.cur_state += 1<< pos
                elif elem == 'n':
                    self.black_board[elem] = self.black_board.get(elem,0) +  1 << pos 
                    self.cur_state += 1<< pos
                elif elem == 'q':
                    self.black_board['q'] = 1 << pos
                    self.cur_state += 1<< pos
                elif elem == 'K':
                    self.white_board['K'] = 1 << pos
                    self.cur_state += 1<< pos
                elif elem == 'B':
                    self.white_board[elem] = self.white_board.get(elem,0) +  1 << pos 
                    self.cur_state += 1<< pos
                elif elem == 'R':
                    self.white_board[elem] = self.white_board.get(elem,0) +  1 << pos 
                    self.cur_state += 1<< pos
                elif elem == 'N':
                    self.white_board[elem] = self.white_board.get(elem,0) +  1 << pos 
                    self.cur_state += 1<< pos
                elif elem == 'Q':
                    self.white_board['Q'] = 1 << pos
                    self.cur_state += 1<< pos
                
                if elem != '/':
                    pos += 1
            
    def printBoard(self, bitboard):
        board = '{0:b}'.format(bitboard).zfill(64)
        board = board[::-1]
        indices = [0,8,16,24,32,40,48,56,]
        parts = [board[i:j] for i,j in zip(indices, indices[1:]+[None])]
        rows = [8,7,6,5,4,3,2,1]
        for i in range(1,9):
            parts[i-1] = str(rows[i-1])+'|'+ parts[i-1]
        parts.insert(0,"  abcdefgh")
        print('\n'.join(parts))
    
    def player(self, turn):
        pass
    
    def resetBoard(self):
        self.black_board.clear()
        self.white_board.clear()
        self.cur_state = 0<< 63
        
    def moved(self):
        """
        Goal is to return the figure k,r,n,b,q,K,R,N,B or Q and field number i.e. r-63-60
        with 63 being the start field and 60 the end field.
        """
        ret = ''
        w = []
        b = []
        keys = ['k','b','r','n','q']
        move = []
        for x in keys:
            y = x.upper()
            if ((self.white_board_last[y] & (-self.white_board[y] -1)) != 0 ):
                move = str(self.white_board_last[y] & self.white_board[y]).split()
                print(move)
                w.append(y)    
           # print(bool(self.black_board_last[x] & self.black_board[x]), "for", self.black_board_last[x], "and", self.black_board[x])
            if ((self.black_board_last[x] & (-self.black_board[x] -1 )) != 0):
                print("whiole :", '{0:b}'.format(self.black_board_last[x] ^ self.black_board[x]))
                move = str(self.black_board_last[x] ^ self.black_board[x]).split('1')
                for i in range(len(move)):
                    parts = move[i]
                    length = len(move[i])
                for i in parts:
                    val = int(i)+
                    ret = ret +x+' '+int(i)+
                b.append(x)
        print(b)
        print(w)
        return ret
    
    
        
                
            
game = racing_kings()
game.printBoard(game.cur_state)
#print('{0:b}'.format(game.black_board['r']))
#print(game.black_board['r'])
game.toBitBoard("8/8/8/8/8/r7/k1bnKRBN/qrbnQRBN w - - 0 1")
#game.printBoard(game.cur_state)
#game.printBoard(game.last_state)
#print(game.black_board_last['r'])
#print('{0:b}'.format(game.black_board['r']))
game.moved()
test = "8/8/8/8/8/r7/k1bnKRBN/qrbnQRBN w - - 0 1"
parts = test.split()

