from src.game import *
from src.algorithm import *

pygame.init()

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos: Tuple[int, int], square_size: int) -> Tuple[int, int]:
    """Returns the row and column of the mouse position in board coordinates."""
    x, y = pos
    return y // square_size, x // square_size

def menu() -> Optional[str]:
    """Displays the home menu, allows selection of game mode."""
    run = True
    selected_mode = None
    font = pygame.font.SysFont("comicsans", 40)

    btn_player_ai = pygame.Rect(WIDTH // 2 - 100, 200, 250, 70)
    btn_player_player = pygame.Rect(WIDTH // 2 - 100, 300, 250, 70)
    btn_ai_ai = pygame.Rect(WIDTH // 2 - 100, 400, 250, 70)

    while run:
        WIN.fill(BLACK)
        title_text = font.render("Choose game mode", 1, WHITE)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        pygame.draw.rect(WIN, RED, btn_player_ai)
        pygame.draw.rect(WIN, RED, btn_player_player)
        pygame.draw.rect(WIN, RED, btn_ai_ai)

        text_player_ai = font.render("Player vs AI", 1, WHITE)
        text_player_player = font.render("PvP", 1, WHITE)
        text_ai_ai = font.render("AI vs AI", 1, WHITE)

        WIN.blit(text_player_ai, (btn_player_ai.x + (btn_player_ai.width - text_player_ai.get_width()) // 2, btn_player_ai.y + (btn_player_ai.height - text_player_ai.get_height()) // 2))
        WIN.blit(text_player_player, (btn_player_player.x + (btn_player_player.width - text_player_player.get_width()) // 2, btn_player_player.y + (btn_player_player.height - text_player_player.get_height()) // 2))
        WIN.blit(text_ai_ai, (btn_ai_ai.x + (btn_ai_ai.width - text_ai_ai.get_width()) // 2, btn_ai_ai.y + (btn_ai_ai.height - text_ai_ai.get_height()) // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_player_ai.collidepoint(pos):
                    selected_mode = "PLAYER_AI"
                    run = False
                elif btn_player_player.collidepoint(pos):
                    selected_mode = "PLAYER_PLAYER"
                    run = False
                elif btn_ai_ai.collidepoint(pos):
                    selected_mode = "AI_AI"
                    run = False

    return selected_mode

def difficulty_menu(mode: str) -> Dict[str, int] | None:
    """Difficulty selection menu depending on game mode."""
    font = pygame.font.SysFont("comicsans", 40)
    difficulty_mapping = {"Easy": 1, "Medium": 3, "Hard": 5}

    def draw_menu(title):
        WIN.fill(BLACK)
        title_text = font.render(title, 1, WHITE)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    if mode == "PLAYER_AI":
        selected_difficulty = None
        btn_easy = pygame.Rect(WIDTH // 2 - 100, 200, 200, 50)
        btn_medium = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
        btn_hard = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)
        run = True

        while run:
            draw_menu("Choose difficulty level")
            pygame.draw.rect(WIN, RED, btn_easy)
            pygame.draw.rect(WIN, RED, btn_medium)
            pygame.draw.rect(WIN, RED, btn_hard)

            text_easy = font.render("Easy", 1, WHITE)
            text_medium = font.render("Medium", 1, WHITE)
            text_hard = font.render("Hard", 1, WHITE)

            WIN.blit(text_easy, (btn_easy.x + (btn_easy.width - text_easy.get_width()) // 2, btn_easy.y + (btn_easy.height - text_easy.get_height()) // 2))
            WIN.blit(text_medium, (btn_medium.x + (btn_medium.width - text_medium.get_width()) // 2, btn_medium.y + (btn_medium.height - text_medium.get_height()) // 2))
            WIN.blit(text_hard, (btn_hard.x + (btn_hard.width - text_hard.get_width()) // 2, btn_hard.y + (btn_hard.height - text_hard.get_height()) // 2))
           
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if btn_easy.collidepoint(pos):
                        selected_difficulty = difficulty_mapping["Easy"]
                        run = False
                    elif btn_medium.collidepoint(pos):
                        selected_difficulty = difficulty_mapping["Medium"]
                        run = False
                    elif btn_hard.collidepoint(pos):
                        selected_difficulty = difficulty_mapping["Hard"]
                        run = False
        return {"AI": selected_difficulty}

    elif mode == "AI_AI":
        difficulties = {}
        for color, title in [("RED", "Choose difficulty level for RED"), ("WHITE", "Choose difficulty level for WHITE")]:
            selected_difficulty = None
            run = True
            btn_easy = pygame.Rect(WIDTH // 2 - 100, 200, 200, 50)
            btn_medium = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
            btn_hard = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)
            while run:
                draw_menu(title)
                pygame.draw.rect(WIN, RED, btn_easy)
                pygame.draw.rect(WIN, RED, btn_medium)
                pygame.draw.rect(WIN, RED, btn_hard)
                text_easy = font.render("Easy", 1, WHITE)
                text_medium = font.render("Medium", 1, WHITE)
                text_hard = font.render("Hard", 1, WHITE)

                WIN.blit(text_easy, (btn_easy.x + (btn_easy.width - text_easy.get_width()) // 2, btn_easy.y + (btn_easy.height - text_easy.get_height()) // 2))
                WIN.blit(text_medium, (btn_medium.x + (btn_medium.width - text_medium.get_width()) // 2, btn_medium.y + (btn_medium.height - text_medium.get_height()) // 2))
                WIN.blit(text_hard, (btn_hard.x + (btn_hard.width - text_hard.get_width()) // 2, btn_hard.y + (btn_hard.height - text_hard.get_height()) // 2))
               
                pygame.display.update()
               
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return None
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if btn_easy.collidepoint(pos):
                            selected_difficulty = difficulty_mapping["Easy"]
                            run = False
                        elif btn_medium.collidepoint(pos):
                            selected_difficulty = difficulty_mapping["Medium"]
                            run = False
                        elif btn_hard.collidepoint(pos):
                            selected_difficulty = difficulty_mapping["Hard"]
                            run = False
            difficulties[color] = selected_difficulty
        return difficulties

def color_menu(mode: str) -> Optional[Dict[str, Tuple[int, int, int]]]:
    """Player color selection menu."""
    font = pygame.font.SysFont("comicsans", 40)
    clock = pygame.time.Clock()
    
    btn_red = pygame.Rect(WIDTH // 2 - 150, 250, 130, 50)
    btn_white = pygame.Rect(WIDTH // 2 + 20, 250, 130, 50)
    
    run = True
    selected_color = None
    while run:
        clock.tick(60)
        WIN.fill(BLACK)
        
        title_text = font.render("Choose color", 1, WHITE)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))
        
        pygame.draw.rect(WIN, RED, btn_red)
        pygame.draw.rect(WIN, WHITE, btn_white)
        
        text_red = font.render("RED", 1, BLACK)
        text_white = font.render("WHITE", 1, BLACK)

        WIN.blit(text_red, (btn_red.x + (btn_red.width - text_red.get_width()) // 2, btn_red.y + (btn_red.height - text_red.get_height()) // 2))
        WIN.blit(text_white, (btn_white.x + (btn_white.width - text_white.get_width()) // 2, btn_white.y + (btn_white.height - text_white.get_height()) // 2))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_red.collidepoint(pos):
                    selected_color = RED
                    run = False
                elif btn_white.collidepoint(pos):
                    selected_color = WHITE
                    run = False
                    
    if mode == "PLAYER_AI":
            return {"player": selected_color, "AI": WHITE if selected_color == RED else RED}
    elif mode == "PLAYER_PLAYER":
            return {"player1": selected_color, "player2": WHITE if selected_color == RED else RED}
    return None

def board_size_menu() -> Optional[Tuple[int, int]]:
    """Menu for selecting board size (rows and columns)."""
    font = pygame.font.SysFont("comicsans", 40)
    clock = pygame.time.Clock()

    rows_input, cols_input = "", ""
    input_active = "rows"
    run = True

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        prompt = f"Enter number of {'rows' if input_active == 'rows' else 'columns'} (5-15): {rows_input if input_active == 'rows' else cols_input}"
        text_surface = font.render(prompt, True, WHITE)
        WIN.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - text_surface.get_height() // 2))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_active == "rows":
                        if rows_input.isdigit() and 5 <= int(rows_input) <= 15:
                            input_active = "cols"
                        else:
                            rows_input = ""
                    else: 
                        if cols_input.isdigit() and 5 <= int(cols_input) <= 15:
                            run = False
                        else:
                            cols_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    if input_active == "rows":
                        rows_input = rows_input[:-1]
                    else:
                        cols_input = cols_input[:-1]
                else:
                    if event.unicode.isdigit():
                        if input_active == "rows":
                            rows_input += event.unicode
                        else:
                            cols_input += event.unicode
                            
    return int(rows_input), int(cols_input)

def main() -> None:
    """The main function to initialize the game."""
    mode = menu()

    board_size = board_size_menu()

    colors = color_menu(mode) if mode in ("PLAYER_AI", "PLAYER_PLAYER") else None
    
    difficulties = difficulty_menu(mode)

    run = True
    clock = pygame.time.Clock()
    game = Game(WIN, colors, board_size)

    while run:
        clock.tick(FPS)

        if mode == "AI_AI":
            depth = difficulties["RED"] if game.turn == RED else difficulties["WHITE"]
            new_board = minimax(game.get_board(), depth, game.turn == WHITE)[1]
            game.ai_move(new_board)
            if game.track_position():
                print("Играта завършва наравно поради повторение на позицията!")
                run = False
        elif mode == "PLAYER_AI":
            if game.turn == colors["AI"]:
                depth = difficulties["AI"]
                new_board = minimax(game.get_board(), depth, game.turn == WHITE)[1]
                game.ai_move(new_board)

        pygame.time.delay(500)

        if game.winner() is not None:
            print("Winner:", game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == "PLAYER_PLAYER" or (mode == "PLAYER_AI" and game.turn == colors["player"]):
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos, game.board.square_size)
                    game.select(row, col)

        game.update()

    pygame.quit()

if __name__ == "__main__":
    main()