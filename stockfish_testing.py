import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("/Users/richardliu/chess-automation/Stockfish-master/src/stockfish")

board = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
limit = chess.engine.Limit(time=1.0)
print(engine.play(board, limit))
