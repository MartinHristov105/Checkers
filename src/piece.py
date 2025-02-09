from src.constants import *

class Piece:
    """Клас, който представлява пуловете."""

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
        """Изчислява позицията на фигурата спрямо размерите на квадратите"""
        s = self.square_size
        self.x = s * self.col + s // 2
        self.y = s * self.row + s // 2

    def make_king(self) -> None:
        """Преобразува фигурата в крал"""
        self.king = True

    def draw(self, win: Surface) -> None:
        """Изчертава фигурата върху екрана"""
        radius= self.square_size // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row: int, col: int) -> None:
        """Премества пула в нов ред и колона"""
        self.row, self.col = row, col
        self.calc_pos()