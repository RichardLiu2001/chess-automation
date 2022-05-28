from stockfish import Stockfish
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("stockfish")
stockfish = Stockfish("/Users/richardliu/chess-automation/Stockfish-master/src/stockfish")
stockfish.set_skill_level()


print(str(stockfish.get_best_move_time(1000)))

engine = chess.engine.SimpleEngine.popen_uci("stockfish")

board = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
limit = chess.engine.Limit(time=1.0)
engine.play(board, limit)
