from src.game import *

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def test_select_valid_piece():
    """Tests whether it correctly selects a checker if it is the turn of its color."""
    piece = Piece(2, 3, RED, 100)
    game = Game(WIN)
    game.board.board[2][3] = piece

    assert game.select(2, 3) is True
    assert game.selected == piece
    assert game.valid_moves == game.board.get_valid_moves(piece)

def test_select_invalid_piece():
    """Tests whether it does not choose a checker if it is not in the move or there is none."""
    piece = Piece(2, 3, WHITE, 100)
    game = Game(WIN)
    game.board.board[2][3] = piece 

    assert game.select(2, 3) is False
    assert game.selected is None

def test_change_turn():
    """Tests whether change_turn() changes turns correctly."""
    game = Game(WIN)
    assert game.turn == RED
    game.change_turn()
    assert game.turn == WHITE
    game.change_turn()
    assert game.turn == RED

def test_winner():
    """Tests whether winner() returns the winner under various conditions."""
    game = Game(WIN)
    game.board.red_left = 0  
    assert game.winner() == WHITE

    game.board.white_left = 0  
    game.board.red_left = 1
    assert game.winner() == RED

    game.board.red_left = 2
    game.board.white_left = 2
    assert game.winner() is None

def test_ai_move():
    """Tests whether ai_move() updates the board and changes the order."""
    game = Game(WIN)
    new_board = Board()
    game.ai_move(new_board)
    assert game.board == new_board
    assert game.turn == WHITE

def test_generate_position_key():
    """Tests whether generate_position_key() returns a unique position key."""
    game = Game(WIN)
    key1 = game.generate_position_key()
    game.board.board[0][0] = Piece(0, 0, RED, 100)
    key2 = game.generate_position_key()
    key3 = game.generate_position_key()
    assert key1 != key2  
    assert key2 == key3

def test_track_position():
    """Tests whether track_position() correctly tracks repeating positions."""
    game = Game(WIN)
    game.track_position()
    
    assert game.track_position() == False
    assert game.track_position() == True

def test_move_valid():
    """Tests whether move() successfully moves a checker on a valid move."""
    game = Game(WIN)
    piece = Piece(2, 3, RED, 100)
    game.board.board[2][3] = piece
    game.select(2, 3) 
    game.valid_moves = {(3, 4): []}

    assert game._move(3, 4) is True
    assert game.board.get_piece(3, 4) == piece
    assert game.turn == WHITE 

def test_move_invalid():
    """Tests whether move() does not move a checker on an invalid move."""
    game = Game(WIN)
    piece = Piece(2, 3, RED, 100)
    game.board.board[2][3] = piece
    game.select(2, 3)

    assert game._move(4, 5) is False
    assert game.board.get_piece(2, 3) == piece
    assert game.turn == RED

def test_get_board():
    """Tests whether get_board() returns the correct board."""
    game = Game(WIN)

    assert game.get_board() == game.board