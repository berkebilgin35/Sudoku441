import heapq
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
    """aynı """
    # Satır kontrolü
    for j in range(9):
        if board[row][j] == num:
            return False
    # Sütun kontrolü
    for i in range(9):
        if board[i][col] == num:
            return False
    # 3x3 blok kontrolü
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def get_possible_values(board, row, col):
    possibilities = []
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            possibilities.append(num)
    return possibilities

def find_empty_cell(board):
    """
    MRV stratejisi kullanarak boş hücreleri inceler.
    En az adede sahip boş hücreyi (veya ilk bulunanı) seçer rütbesel sezgi de eklenebilirdi. İlk algoritma çok üzerinde durdum diye böyle denedim
    """
    min_count = float('inf')
    best = None
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                poss = get_possible_values(board, i, j)
                if len(poss) < min_count:
                    min_count = len(poss)
                    best = (i, j)
                if min_count == 1:
                    return best
    return best

def heuristic(board):
    """
    Basit h(n): Toplam boş (0) hücre sayısı.
    """
    count = 0
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                count += 1
    return count

def a_star_solver(board):
    """
    A* algoritmasını kullanarak Sudoku'yu çözer.
    Her durum, board ve 'g' (atama sayısı) değeriyle temsil edilir.
    
    h(n) olarak basitçe boş hücre sayısını kullanıyoruz. 
    Yeni durumlar oluştururken, boş hücrelerden MRV stratejisini baz alarak
    aday değerler üretip her durumu yeni bir atama ile oluşturuyoruz.
    """
    start_state = (board, 0)  # board, g = 0
    h = heuristic(board)
    f = h  # f(n) = g(n) + h(n), burada g = 0
    heap = []
    # Heap elemanı: (f, g, board)
    heapq.heappush(heap, (f, 0, board))
    
    while heap:
        f, g, current = heapq.heappop(heap)
        
        # Eğer board doluysa, çözüm bulunmuştur.
        if heuristic(current) == 0:
            return current
        
        cell = find_empty_cell(current)
        if cell is None:
            continue
        row, col = cell
        poss = get_possible_values(current, row, col)
        for val in poss:
            new_board = copy.deepcopy(current)
            new_board[row][col] = val
            new_g = g + 1
            new_h = heuristic(new_board)
            new_f = new_g + new_h
            heapq.heappush(heap, (new_f, new_g, new_board))
    return None


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

# Board'u tablo şeklinde string'e çeviren fonksiyon (0 yerine '*' yazılır)
def board_to_string(board):
    lines = []
    for i, row in enumerate(board):
        line = ""
        for j, num in enumerate(row):
            ch = str(num) if num != 0 else "*"
            line += ch + " "
            if j == 2 or j == 5:
                line += "| "
        lines.append(line)
        if i == 2 or i == 5:
            lines.append("- " * 15)
    return "\n".join(lines)

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
                selected_board = sudoku_easy
            elif button_medium.collidepoint(mouse_pos):
                selected_board = sudoku_medium
            elif button_hard.collidepoint(mouse_pos):
                selected_board = sudoku_hard
            
            if selected_board is not None:
                initial_board_str = board_to_string(selected_board)
                start_time = time.perf_counter()
                solved_board = a_star_solver(copy.deepcopy(selected_board))
                end_time = time.perf_counter()
                solve_time = end_time - start_time
                solved_board_str = board_to_string(solved_board)
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