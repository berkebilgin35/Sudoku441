import random
import time
import pygame
import copy

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
def count_conflicts(board, row, col, num):
    """
    Belirtilen hücrede num değeri varsa, aynı satır, sütun ve 3x3 blok
    içinde kaç tane çakışma (aynı num) olduğunu sayar.
    """
    conflicts = 0
    # Satır kontrolü
    for j in range(9):
        if j != col and board[row][j] == num:
            conflicts += 1
    # Sütun kontrolü
    for i in range(9):
        if i != row and board[i][col] == num:
            conflicts += 1
    # 3x3 blok kontrolü
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            r, c = start_row + i, start_col + j
            if (r != row or c != col) and board[r][c] == num:
                conflicts += 1
    return conflicts

def initialize_board(board):
    """
    Her satırda, sabit (girilen) hücreleri koruyarak eksik rakamları,
    rastgele bir sırayla boş hücrelere yerleştirir.
    Böylece her satır 1-9 rakamlarının bir permütasyonu haline gelir.
    """
    fixed = {(i, j) for i in range(9) for j in range(9) if board[i][j] != 0}
    for i in range(9):
        # Satırdaki sabit rakamlar
        used = {board[i][j] for j in range(9) if (i, j) in fixed}
        missing = list(set(range(1, 10)) - used)
        random.shuffle(missing)
        for j in range(9):
            if (i, j) not in fixed:
                board[i][j] = missing.pop()
    return fixed

def min_conflict_solver(board, max_iterations=100000):
    """
    Minimum Conflict yaklaşımını kullanarak Sudoku'yu çözer.
    İlk atamada, sabit hücreleri koruyarak her satırı permütasyon haline getirir.
    Daha sonra, belirli iterasyonlar boyunca yerel iyileştirme olarak aynı satırdaki
    iki değiştirilebilir hücre arasında swap yapar.
    """
    fixed = initialize_board(board)
    
    for iteration in range(max_iterations):
        conflicted = []
        # Tüm satır ve sütunlarda çakışma yaşayan (sabit olmayan) hücreleri topla.
        for i in range(9):
            for j in range(9):
                if (i, j) not in fixed and count_conflicts(board, i, j, board[i][j]) > 0:
                    conflicted.append((i, j))
        if not conflicted:
            return True  # Çakışma kalmamışsa çözüm bulunmuştur.
        
        # Rastgele çakışma yaşayan bir hücre seç.
        i, j = random.choice(conflicted)
        # Aynı satırdaki, değiştirilebilir diğer hücreleri aday olarak al.
        candidates = [col for col in range(9) if (i, col) not in fixed and col != j]
        current_conflict = count_conflicts(board, i, j, board[i][j])
        best_conflict = current_conflict
        best_swap = j
        
        # Her aday hücre ile swap yaparak toplam çakışmayı seçilen ve swap yapılan hücreler hesapla.
        for col in candidates:
            # Swap işlemi
            board[i][j], board[i][col] = board[i][col], board[i][j]
            new_conflict = count_conflicts(board, i, j, board[i][j]) + count_conflicts(board, i, col, board[i][col])
            if new_conflict < best_conflict:
                best_conflict = new_conflict
                best_swap = col
            # Swap işlemini eski haline getirmek
            board[i][j], board[i][col] = board[i][col], board[i][j]
        
        # İyileştirme sağlayan bir swapi ypapmak
        if best_swap != j:
            board[i][j], board[i][best_swap] = board[i][best_swap], board[i][j]
        else:
            # Yerel minimuma takıldıysak, rastgele bir swap yaparak sistemi sars.
            if candidates:
                col = random.choice(candidates)
                board[i][j], board[i][col] = board[i][col], board[i][j]
    return False  # max_iterations sonunda çözüm bulunamazsa.
# Örnek kullanımı:

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
        
        if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button_easy.collidepoint(mouse_pos):
                selected_board = copy.deepcopy(sudoku_easy)
            elif button_medium.collidepoint(mouse_pos):
                selected_board = copy.deepcopy(sudoku_medium)
            elif button_hard.collidepoint(mouse_pos):
                selected_board = copy.deepcopy(sudoku_hard)
            
            if selected_board is not None:
                initial_board_str = board_to_string(selected_board)
                start_time = time.perf_counter()
                # Burada IDS yerine dummy_solver_ids veya dummy_solver_mch
                # Örneğin IDS ile deniyorsak:
                solved_board = min_conflict_solver(selected_board)
                
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
                else:
                    result = "Çözüm bulunamadı"
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