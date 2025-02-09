from src.constants import *
from src.board import *

class Game:
    """Клас, който управлява логиката на играта и състоянието на дъската."""

    def __init__(self, win: Surface, colors: Optional[List[Tuple[int, int, int]]] = None, board_size: Tuple[int, int] = (8, 8)) -> None:
        self.colors = colors
        self.win = win
        self.board_size = board_size
        self.position_history = {}
        self.selected = None
        self.board = Board(self.board_size)
        self.turn = RED
        self.valid_moves = {}

    def update(self) -> None:
        """Обновява екрана, рисува дъската и валидните ходове."""
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def select(self, row: int, col: int) -> bool:
        """Избира пул на дадена позиция."""
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def _move(self, row: int, col: int) -> bool:
        """Опитва да премести избрания пул на ново място."""
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
            return True
        return False

    def draw_valid_moves(self, moves: List[Tuple[int, int]]) -> None:
        """Начертава валидните ходове като сини кръгове върху дъската."""
        s = self.board.square_size 
        [pygame.draw.circle(self.win, BLUE, (col * s + s // 2, row * s + s // 2), 15) for row, col in moves]

    def change_turn(self) -> None:
        """Променя хода на играча (червените/белите)."""
        self.valid_moves = {}
        self.turn = WHITE if self.turn == RED else RED

    def winner(self) -> Optional[Tuple[int, int, int]]:
        """Връща победителя, ако има такъв, или None ако няма."""
        return self.board.winner()
    
    def get_board(self) -> Board:
        """Връща дъската."""
        return self.board

    def ai_move(self, board) -> None:
        """Извършва ход от изкуствения интелект."""
        self.board = board
        self.change_turn()

    def generate_position_key(self) -> str:
        """Генерира уникален ключ за текущата позиция на дъската."""
        key = ''.join(
            f"{piece.color}{piece.row}{piece.col}"
            for row in range(self.board.rows)
            for col in range(self.board.cols)
            if isinstance(self.board.board[row][col], Piece)
            for piece in [self.board.board[row][col]]
        )
        return key

    def track_position(self) -> bool:
        """Следи историята на позициите на дъската за да открие зацикляне."""
        position_key = self.generate_position_key()
        self.position_history[position_key] = self.position_history.get(position_key, 0) + 1
        return self.position_history[position_key] == 3