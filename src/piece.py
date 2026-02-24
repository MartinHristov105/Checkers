from src.constants import *

class Piece:
    """A class that represents the checkers."""

    PADDING: int = 10
    OUTLINE: int = 3

    def __init__(self, row: int, col: int, color: Tuple[int, int, int], square_size: Optional[int] = None) -> None:
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.square_size = square_size
        self.x= 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self) -> None:
        """Calculates the position of the figure relative to the dimensions of the squares."""
        s = self.square_size
        self.x = s * self.col + s // 2
        self.y = s * self.row + s // 2

    def make_king(self) -> None:
        """Transforms the piece into a king."""
        self.king = True

    def draw(self, win: Surface) -> None:
        """Draws the shape on the screen."""
        radius= self.square_size // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row: int, col: int) -> None:
        """Moves the checker to a new row and column."""
        self.row, self.col = row, col
        self.calc_pos()