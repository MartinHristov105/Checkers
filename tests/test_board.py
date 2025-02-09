from src.board import *

def test_create_board():
    board = Board()
    board.create_board()
    for row in range(board.rows):
        for col in range(board.cols):
            piece = board.get_piece(row, col)

            if col % 2 == (row + 1) % 2:
                if row < board.white_rows:
                    assert piece is not None
                    assert piece.color == WHITE
                elif row >= board.rows - board.red_rows:
                    assert piece is not None
                    assert piece.color == RED
                else:
                    assert piece == 0
            else:
                assert piece == 0

def test_move():
    """Тества дали местенето на пул работи коректно."""
    piece = Piece(2, 3, WHITE, 100)
    board = Board()
    board.board[2][3] = piece

    board.move(piece, 3, 4)

    assert board.get_piece(3, 4) == piece
    assert board.get_piece(2, 3) == 0
    assert piece.row == 3 and piece.col == 4

def test_get_piece():
    """Тества дали правилно се връща пул или None."""
    piece = Piece(4, 5, RED, 100)
    board = Board()
    board.board[4][5] = piece

    assert board.get_piece(4, 5) == piece
    assert board.get_piece(2, 2) == 0

def test_get_all_pieces():
    """Тества дали връща правилния брой пулове за даден цвят."""
    board = Board()
    white_pieces = board.get_all_pieces(WHITE)
    red_pieces = board.get_all_pieces(RED)

    assert len(white_pieces) == 12
    assert len(red_pieces) != 13

def test_get_valid_moves():
    """Тества дали връща възможните ходове за даден пул."""
    piece = Piece(4, 4, WHITE, 100)
    board = Board()
    board.board[4][4] = piece

    moves = board.get_valid_moves(piece)

    assert all(isinstance(key, tuple) for key in moves.keys())

def test_remove():
    """Тества дали премахването на пулове работи коректно."""
    piece1 = Piece(2, 2, WHITE, 100)
    piece2 = Piece(3, 3, RED, 100)

    board = Board()
    board.board[2][2] = piece1
    board.board[3][3] = piece2

    board.remove([piece1, piece2])

    assert board.get_piece(2, 2) == 0
    assert board.get_piece(3, 3) == 0

def test_has_valid_moves():
    """Тества дали правилно се проверяват валидните ходове."""
    piece1 = Piece(4, 4, WHITE, 100)
    piece2 = Piece(5, 5, RED, 100)

    board = Board()
    board.board[4][4] = piece1
    board.board[5][5] = piece2

    assert board.has_valid_moves(WHITE) is True
    assert board.has_valid_moves(RED) is True

def test_winner():
    """Тества дали правилно се определя победителят."""
    board = Board()
    board.red_left = 0
    assert board.winner() == WHITE

    board.white_left = 0
    board.red_left = 1
    assert board.winner() == RED

    board.white_left = 1
    assert board.winner() is None  
    
def test_traverse_left_empty_path():
    """Тества дали `_traverse_left` намира валидни ходове по празен диагонал."""
    piece = Piece(4, 4, WHITE, 100)
    board = Board()
    board.board[4][4] = piece

    moves = board._traverse_left(3, 0, -1, WHITE, 3)

    assert (3, 3) in moves
    assert isinstance(moves[(3, 3)], list) and len(moves[(3, 3)]) == 0

def test_traverse_left_with_capture():
    """Тества дали `_traverse_left` намира правилния ход при възможно вземане."""
    piece = Piece(4, 4, WHITE, 100)
    enemy_piece = Piece(3, 3, RED, 100)
    board = Board()
    board.board[4][4] = piece
    board.board[3][3] = enemy_piece

    moves = board._traverse_left(3, 0, -1, WHITE, 3)

    assert (2, 2) in moves  
    assert moves[(2, 2)] == [enemy_piece]

def test_traverse_left_blocked():
    """Тества дали `_traverse_left` спира, ако пътят е блокиран."""
    piece = Piece(4, 4, WHITE, 100)
    blocker = Piece(3, 3, WHITE, 100)
    board = Board()
    board.board[4][4] = piece
    board.board[3][3] = blocker

    moves = board._traverse_left(3, 0, -1, WHITE, 3)

    assert moves == {}

def test_traverse_right_empty_path():
    """Тества дали `_traverse_right` намира валидни ходове по празен диагонал."""
    piece = Piece(4, 4, WHITE, 100)
    board = Board()
    board.board[4][4] = piece

    moves = board._traverse_right(3, 0, -1, WHITE, 5)

    assert (3, 5) in moves
    assert isinstance(moves[(3, 5)], list) and len(moves[(3, 5)]) == 0

def test_traverse_right_with_capture():
    """Тества дали `_traverse_right` намира правилния ход при възможно вземане."""
    piece = Piece(4, 4, WHITE, 100)
    enemy_piece = Piece(3, 5, RED, 100)
    board = Board()
    board.board[4][4] = piece
    board.board[3][5] = enemy_piece

    moves = board._traverse_right(3, 0, -1, WHITE, 5)

    assert (2, 6) in moves  
    assert moves[(2, 6)] == [enemy_piece]

def test_traverse_right_blocked():
    """Тества дали `_traverse_right` спира, ако пътят е блокиран."""
    piece = Piece(4, 4, WHITE, 100)
    blocker = Piece(3, 5, WHITE, 100)
    board = Board()
    board.board[4][4] = piece
    board.board[3][5] = blocker  

    moves = board._traverse_right(3, 0, -1, WHITE, 5)

    assert moves == {}

def test_evaluate():
    """Тества функцията `evaluate`, като проверява числовия резултат."""
    board = Board()
    board.red_left = 5
    board.white_left = 7
    board.red_kings = 1
    board.white_kings = 2

    score = board.evaluate()

    assert score == 3.350000000000001