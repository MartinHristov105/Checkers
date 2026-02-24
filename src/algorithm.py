from copy import deepcopy
from src.constants import *
from src.board import *

def minimax(position: Board, depth: int, max_player: bool, alpha: float = float('-inf'), beta: float = float('inf')) -> Tuple[float, Optional[Board]]:
    """Find the best move using Minimax algorithm with Alpha-Beta."""    
    
    winner = position.winner()
    if depth == 0 or winner:
        if depth == 0:
            return position.evaluate(), position
        return (1000000, position) if winner == WHITE else (-1000000, position)

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE):
            evaluation = minimax(move, depth-1, False, alpha, beta)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED):
            evaluation = minimax(move, depth-1, True, alpha, beta)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break          
        return minEval, best_move

def simulate_move(piece: Piece, move: Tuple[int, int], board: Board, skip: Optional[List[Piece]]) -> Board:
    """Make a move and return the new board state."""
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

def get_all_moves(board: Board, color: Tuple[int, int, int]) ->List[Board]:
    """Returns all new possible board states for a player."""
    return [
        simulate_move(temp_board.get_piece(piece.row, piece.col), move, temp_board, skip)
        for piece in board.get_all_pieces(color)
        for move, skip in board.get_valid_moves(piece).items()
        for temp_board in [deepcopy(board)]
    ]