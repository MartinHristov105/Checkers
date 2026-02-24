from src.piece import *

def test_piece_calc_pos():
    """Tests whether the positions is correclty calculated."""
    piece = Piece(1, 1, RED, 100)
    piece.calc_pos()
    assert piece.x == 150 and piece.y == 150

def test_piece_move():
    """Tests whether the piece is correclty moved."""
    piece = Piece(1, 1, RED, 100)
    piece.move(2, 2)
    assert piece.row == 2 and piece.col == 2