import copy
import time
import pygame

"""# Sudoku tahtasını ekrana yazdırmak için fonksiyon. 2D arrayi Sudoku tahtası formatını getirip çıktı verir.
def printBoard(board):
    for i in range(9):
        # 3 satırda bir çizgi
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            # 3 sütunda bir dikey çizgi
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            
            if board[i][j] == 0:
                # Boş hücrelere '*' bas
                print("*", end=" ")
            else:
                print(board[i][j], end=" ")
        print()  # satır sonu

"""
def is_valid(board, row, col, num):
    """AYNI."""
    # Satır kontrolü
    if num in board[row]:
        return False

    # Sütun kontrolü
    for r in range(9):
        if board[r][col] == num:
            return False

    # 3x3 blok kontrolü
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def get_blank_positions(board):
    """Sudoku tahtasındaki tüm boş hücrelerin koordinatlarını döner."""
    blanks = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                blanks.append((i, j))
    return blanks

def dls(board, blanks, index, limit):
    """
    Derinlik Sınırlı Arama (Depth-Limited Search)
    board     : mevcut board durumu
    blanks    : boş hücrelerin listesi (satır, sütun)
    index     : şu an hangi boş hücre üzerinde olduğumuzu ifade eder
    limit     : geçerli derinlik limiti (kaç hücre doldurulabilecek)
    """
    if index == len(blanks):
        # Tüm boşluklar doldurulmuşsa çözüme ulaşılmıştır.
        return True

    # Eğer şu anki derinlik index, limit'e ulaştıysa (yani arama bu derinlikle sınırlı)
    if index >= limit:
        return False  # Bu dalda daha fazla ilerleyemeyiz. başa dön

    row, col = blanks[index]
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if dls(board, blanks, index + 1, limit):
                return True
            board[row][col] = 0  # Geri izleme (backtracking)
    return False

def iterative_deepening_solver(board):
    """
    Yinelemeli Derinleşen Arama yöntemi ile Sudoku çözer.
    Board üzerinde değişiklik yapar ve çözüme ulaşırsa True, aksi halde False döner.
    """
    blanks = get_blank_positions(board)
    total_blanks = len(blanks)
    # Derinlik sınırı, boş hücre sayısına kadar artırılarak denenir.
    for limit in range(1, total_blanks + 1):
        board_copy = copy.deepcopy(board)
        if dls(board_copy, blanks, 0, limit):
            # Çözüme ulaşıldıysa board_copy sonuç board'a aktarılır.
            for i in range(9):
                board[i] = board_copy[i][:]
            return True
    return False


pygame.init()

# Pencere boyutu ve ayarlar
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku Çözücü - Kolay, Orta, Zor")
font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()

# Renkler
white = (255, 255, 255)
black = (0, 0, 0)
light_blue = (173, 216, 230)

# Sudoku Problemleri:
sudoku_easy = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

sudoku_medium = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

sudoku_hard = [
    [0, 0, 5, 3, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 7, 0, 0, 1, 0, 5, 0, 0],
    
    [4, 0, 0, 0, 0, 5, 3, 0, 0],
    [0, 1, 0, 0, 7, 0, 0, 0, 6],
    [0, 0, 3, 2, 0, 0, 0, 8, 0],
    
    [0, 6, 0, 5, 0, 0, 0, 0, 9],
    [0, 0, 4, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 9, 7, 0, 0]
]


def board_to_string(board):
    result = ""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            result += "-" * 21 + "\n"
        for j in range(9):
            if j % 3 == 0 and j != 0:
                result += "| "
            if board[i][j] == 0:
                result += "* "
            else:
                result += str(board[i][j]) + " "
        result += "\n"
    return result


# Menü düğmeleri (butonlar)
button_easy = pygame.Rect(50, 50, 200, 50)
button_medium = pygame.Rect(300, 50, 200, 50)
button_hard = pygame.Rect(550, 50, 200, 50)

# Uygulama durumu: "menu" veya "result"
state = "menu"
selected_board = None
initial_board_str = ""
solved_board_str = ""
solve_time = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Menü durumundayken; fare tıklaması ile buton seçimi
        if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button_easy.collidepoint(mouse_pos):
                selected_board = copy.deepcopy(sudoku_easy)
            elif button_medium.collidepoint(mouse_pos):
                selected_board = copy.deepcopy(sudoku_medium)
            elif button_hard.collidepoint(mouse_pos):
                selected_board = copy.deepcopy(sudoku_hard)
            
            if selected_board is not None:
                initial_board_str = board_to_string((selected_board))
                start_time = time.perf_counter()
                # Burada IDS yerine dummy_solver_ids veya dummy_solver_mch
                # Örneğin IDS ile deniyorsak:
                solved_board = iterative_deepening_solver(selected_board)
                
                if solved_board:
                        result = ""
                        for i in range(9):
                            if i % 3 == 0 and i != 0:
                                result += "-" * 21 + "\n"
                            for j in range(9):
                                if j % 3 == 0 and j != 0:
                                    result += "| "
                                if selected_board[i][j] == 0:
                                    result += "* "
                                else:
                                    result += str(selected_board[i][j]) + " "
                            result += "\n"

                end_time = time.perf_counter()
                solve_time = end_time - start_time
                solved_board_str = result
                state = "result"
        
        # Sonuç durumunda, herhangi bir tuşa basılırsa menüye dön
        if state == "result" and event.type == pygame.KEYDOWN:
            state = "menu"
            selected_board = None



    screen.fill(white)
    
    if state == "menu":
        # Menü başlığı
        title = font.render("Sudoku Çözücü - Seviye Seçiniz", True, black)
        screen.blit(title, (width//2 - title.get_width()//2, 10))
        # Butonları çiz
        pygame.draw.rect(screen, light_blue, button_easy)
        pygame.draw.rect(screen, light_blue, button_medium)
        pygame.draw.rect(screen, light_blue, button_hard)
        text_easy = font.render("Kolay", True, black)
        text_medium = font.render("Orta", True, black)
        text_hard = font.render("Zor", True, black)
        screen.blit(text_easy, (button_easy.x + 70, button_easy.y + 15))
        screen.blit(text_medium, (button_medium.x + 70, button_medium.y + 15))
        screen.blit(text_hard, (button_hard.x + 70, button_hard.y + 15))
    elif state == "result":
        header1 = font.render("Başlangıç Tahtası", True, black)
        header2 = font.render("Çözülen Tahtası", True, black)
        screen.blit(header1, (50, 120))
        screen.blit(header2, (width//2 + 50, 120))
        
        # Başlangıç tahtasını çiz
        y_offset = 150
        for line in initial_board_str.split("\n"):
            rendered_line = font.render(line, True, black)
            screen.blit(rendered_line, (50, y_offset))
            y_offset += rendered_line.get_height() + 2
            
        # Çözülen tahtayı çiz
        y_offset = 150
        for line in solved_board_str.split("\n"):
            rendered_line = font.render(line, True, black)
            screen.blit(rendered_line, (width//2 + 50, y_offset))
            y_offset += rendered_line.get_height() + 2

        # Çalışma süresi
        time_text = font.render(f"Çalışma Süresi: {solve_time:.4f} saniye", True, black)
        screen.blit(time_text, (50, height - 50))
        instruct_text = font.render("Menüye dönmek için herhangi bir tuşa basın.", True, black)
        screen.blit(instruct_text, (50, height - 25))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()