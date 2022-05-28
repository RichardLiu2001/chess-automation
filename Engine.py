import chess
import chess.engine

class Engine:

    def __init__(self, color):
        self.engine = chess.engine.SimpleEngine.popen_uci("/Users/richardliu/chess-automation/Stockfish-master/src/stockfish")
        self.board = chess.Board()
        self.color = color

    def process_move(self, move):
        self.board.push_san(move)

    def get_engine_move(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=1))
        return result.move
