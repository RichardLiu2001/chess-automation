import chess
import chess.engine

class Engine:

    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci("/Users/richardliu/chess-automation/Stockfish-master/src/stockfish")
        self.board = chess.Board()

    def process_move(self, move):
        
        if '=' in move:
            
            reformat_move = move[1:] + move[0]
            if '#' in reformat_move:
               reformat_move = reformat_move.replace('#', '') + '#' 
            
            self.board.push_san(reformat_move)

        else:
            self.board.push_san(move)

    def get_engine_move(self):
        uci_Move = self.engine.play(self.board, chess.engine.Limit(time=0.5))
        uci = uci_Move.move.uci()

        move = self.board.parse_uci(uci)
        san = self.board.san(move)
        #print(str(uci, san))
        return uci, san
    
    def reset(self):
        self.board.reset()

