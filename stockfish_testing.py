from stockfish import Stockfish
stockfish = Stockfish("/Users/richardliu/chess-automation/Stockfish-master/src/stockfish")
print(str(stockfish.get_best_move()))