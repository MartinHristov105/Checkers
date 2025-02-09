from copy import deepcopy
from src.algorithm import *

def test_simulate_move():
    """Тества дали simulate_move() коректно мести пул и премахва прескочените фигури."""
    board = Board()
    piece = Piece(2, 3, RED, 100)
    board.board[2][3] = piece
    board.board[3][4] = 0  

    new_board = simulate_move(piece, (3, 4), board, None)
    moved_piece = new_board.get_piece(3, 4)

    assert moved_piece is not None  
    assert moved_piece.color == piece.color 
    assert moved_piece.row == 3 and moved_piece.col == 4  
    assert new_board.get_piece(2, 3) == 0

def test_simulate_move_with_capture():
    """Тества дали simulate_move() премахва прескочената фигура при вземане."""
    board = Board()
    piece = Piece(2, 3, RED, 100)
    enemy_piece = Piece(3, 4, WHITE, 100)
    board.board[2][3] = piece
    board.board[3][4] = enemy_piece
    board.board[4][5] = 0 

    new_board = simulate_move(piece, (4, 5), deepcopy(board), [enemy_piece])
    moved_piece = new_board.get_piece(4, 5)

    assert moved_piece != 0  
    assert new_board.get_piece(3, 4) == 0  

def test_get_all_moves():
    """Тества дали get_all_moves() връща валидни ходове за даден цвят."""
    board = Board()
    piece = Piece(2, 3, RED, 100)
    board.board[2][3] = piece
    board.board[3][4] = 0

    all_moves = get_all_moves(board, RED)

    assert len(all_moves) > 0  

def test_minimax_depth_zero():
    """Тества дали Minimax връща оценката на позицията при depth=0."""
    board = Board()
    score, best_move = minimax(board, 0, True)

    assert score == board.evaluate()
    assert best_move == board 
    
def test_minimax_white_wins():
    """Тества дали Minimax разпознава победа за белите."""
    board = Board()
    board.red_left = 0  

    score, best_move = minimax(board, 3, True)

    assert score == 1000000 
    assert best_move is not None 

def test_minimax_red_wins():
    """Тества дали Minimax разпознава победа за червените."""
    board = Board()
    board.white_left = 0 
    
    score, best_move = minimax(board, 3, True)

    assert score == -1000000  
    assert best_move is not None 

def test_minimax_finds_best_move():
    """Тества дали Minimax намира най-добрия ход в начална позиция."""
    board = Board()
    score, best_move = minimax(board, 3, True)

    assert best_move is not None  
    assert isinstance(score, float)