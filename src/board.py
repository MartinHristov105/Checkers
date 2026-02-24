from src.constants import *
from src.piece import *

class Board:
    """A class that represents the playing field of checkers."""

    def __init__(self, board_size: Tuple[int, int] = (8, 8)) -> None:
        self.rows, self.cols = board_size
        self.square_size = WIDTH // max(self.cols, self.rows)  
        self.white_rows = self.rows // 2 - 1
        self.red_rows = self.rows // 2 - 1
        
        self.board = []
        self.red_left = self.white_left = self.red_kings = self.white_kings = 0
        self.create_board()

    def create_board(self) -> None:
        """Creates the game board."""
        for row in range(self.rows):
            row_pieces = []
            for col in range(self.cols):
                if col % 2 == (row + 1) % 2:
                    if row < self.white_rows:
                        row_pieces.append(Piece(row, col, WHITE, self.square_size))
                        self.white_left += 1
                    elif row >= self.rows - self.red_rows:
                        row_pieces.append(Piece(row, col, RED, self.square_size))
                        self.red_left += 1
                    else:
                        row_pieces.append(0)
                else:
                    row_pieces.append(0)
            self.board.append(row_pieces)

    def draw_squares(self, win: Surface) -> None:
        """Draws the squares on the playing field."""
        win.fill(BLACK)
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(win, RED, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def draw(self, win: Surface) -> None:
        """Draws the entire board along with the checkers."""
        self.draw_squares(win)
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.board[row][col]
                if piece:
                    piece.square_size = self.square_size
                    piece.draw(win)

    def move(self, piece: Piece, row: int, col: int) -> None:
        """Moves a checker to a new place on the board."""
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row in (0, self.rows - 1):
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Returns a checker at the given location or None if there is none."""
        return self.board[row][col]

    def get_all_pieces(self, color: Tuple[int, int, int]) -> List[Piece]:
        """Returns a list of all checkers of a given color."""
        return [piece for row in self.board for piece in row if piece != 0 and piece.color == color]

    def get_valid_moves(self, piece: Piece) -> Dict[Tuple[int, int], List[Piece]]:
        """Returns the valid moves for a given checker."""
        moves = {}
        left, right, row = piece.col - 1, piece.col + 1, piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, self.rows), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, self.rows), 1, piece.color, right))
        return moves

    def _traverse_left(self, start: int, stop: int, step: int, color: Tuple[int, int, int], left: int, skipped: List[Piece] = []) -> Dict[Tuple[int, int], List[Piece]]:
        """Traverses the fields diagonally to the left and returns valid moves."""
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    new_stop = max(r - 3, 0) if step == -1 else min(r + 3, self.rows)
                    moves.update(self._traverse_left(r + step, new_stop, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, new_stop, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start: int, stop: int, step: int, color: Tuple[int, int, int], right: int, skipped: List[Piece] = []) -> Dict[Tuple[int, int], List[Piece]]:
        """Traverses the squares diagonally to the right and returns valid moves."""
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= self.cols:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    new_stop = max(r - 3, 0) if step == -1 else min(r + 3, self.rows)
                    moves.update(self._traverse_left(r + step, new_stop, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, new_stop, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves

    def remove(self, pieces: List[Piece]) -> None:
        """Removes checkers from the board."""
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece:
                self.red_left -= piece.color == RED
                self.white_left -= piece.color == WHITE

    def has_valid_moves(self, color: Tuple[int, int, int]) -> bool:
        """Checks if the given color has valid moves."""
        pieces = self.get_all_pieces(color)
        
        if not pieces:
            return self.white_left > 0 if color == RED else self.red_left > 0
        
        return any(self.get_valid_moves(piece) for piece in pieces)

    def winner(self) -> Optional[Tuple[int, int, int]]:
        """Returns the winner, if there is one, or None if there is none."""
        if self.red_left == 0 or not self.has_valid_moves(RED):
            return WHITE
        elif self.white_left == 0 or not self.has_valid_moves(WHITE):
            return RED
        return None

    def evaluate(self) -> int:
        """Estimates the current state of the game based on the number of checkers and their position."""
        evaluation = 0
        evaluation += (self.white_left - self.red_left) * 1.0
        evaluation += (self.white_kings - self.red_kings) * 1.5
        
        center_x, center_y = self.cols / 2, self.rows / 2
        max_distance = center_x + center_y

        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.board[row][col]
                if piece:
                    distance = abs(col - center_x) + abs(row - center_y)
                    center_bonus = (max_distance - distance) / max_distance * 0.1
                    if piece.color == WHITE:
                        evaluation += center_bonus
                    else:
                        evaluation -= center_bonus

                    if piece.color == WHITE:
                        advancement = row / (self.rows - 1)
                        evaluation += advancement * 0.1
                    else:
                        advancement = (self.rows - 1 - row) / (self.rows - 1)
                        evaluation -= advancement * 0.1

                    if piece.king:
                        center_row = self.rows / 2
                        king_center_bonus = (1 - abs(row - center_row) / center_row) * 2
                        if piece.color == WHITE:
                            evaluation += king_center_bonus
                        else:
                            evaluation -= king_center_bonus

        return evaluation