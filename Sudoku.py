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
# Sudoku kurallarına göre uygunluğu kontrol eden fonksiyon
def isValid(board, row, col, num):
    # Satır ve sütun kontrolü
    for i in range(9):
        if board[row][i] == num:
            return False
        if board[i][col] == num:
            return False
    
    # 3x3 alt kare kontrolü
    startRow = row - (row % 3)
    startCol = col - (col % 3)
    for i in range(3):
        for j in range(3):
            if board[startRow + i][startCol + j] == num:
                return False

    return True

# Her hücre için başlangıç domainleri oluştur. Dolu hücreler için domain, o hücrenin tek değerinden oluşur.
def startingDomains(board):
    domains = {}
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                domains[(row, col)] = [i for i in range(1, 10)]
            else:
                domains[(row, col)] = [board[row][col]]
    return domains

# Domain'leri güncelle
def forwardChecking(domains, row, col, num):
    """
    Forward Checking: sayı eklendipi zaman aynı satır, sütun ve 3x3 karedeki domainlerden o sayıyı çıkarır.
    Domain tamamen boşalan bir hücre olursa None döndürerek bu yolun hatalı olduğunu belirtir. geri dönerek başka yoldan ilerlememiz gerekir
    """
    updated = copy.deepcopy(domains)
    updated[(row, col)] = [num]  # tek değer kaldı

    # Satır ve sütundaki domainlerden sayıyı çıkar
    for i in range(9):
        # Satır
        if (row, i) != (row, col) and num in updated[(row, i)]:
            updated[(row, i)].remove(num)
            if len(updated[(row, i)]) == 0:
                return None
        # Sütun
        if (i, col) != (row, col) and num in updated[(i, col)]:
            updated[(i, col)].remove(num)
            if len(updated[(i, col)]) == 0:
                return None
    
    # 3x3 kare
    sr, sc = 3 * (row // 3), 3 * (col // 3)
    for rr in range(sr, sr + 3):
        for cc in range(sc, sc + 3):
            if (rr, cc) != (row, col) and num in updated[(rr, cc)]:
                updated[(rr, cc)].remove(num)
                if len(updated[(rr, cc)]) == 0:
                    return None

    return updated

def nextCell(board, domains):
    """
    MRV + Degree Heuristic ile doldurulacak bir sonraki hücreyi seçer.
    1) MRV: Domain boyutu en küçük olan hücreleri bul
    2) Eğer birden fazla hücre aynı domain boyutuna sahipse Degree Heuristic ile en çok kısıta sahip (boş komşuları fazla) hücreyi seç
    Bu seçim, "en sıkışık" veya "en kritik" hücreden başlamayı sağlayarak, Backtracking'in hızlı hatayı görmesine yardımcı olur.
    """
    emptyCells = []
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                emptyCells.append((row, col))
    
    # Hiç boş hücre yoksa, çözüm tamam
    if not emptyCells:
        return -1, -1

    # 1) MRV: Domain boyutu küçükten büyüğe sıralama
    emptyCells.sort(key=lambda cell: len(domains[cell]))
    
    # Domain'i en küçük olan ilk hücrenin boyutu
    smallest_domain_size = len(domains[emptyCells[0]])
    
    # Aynı domain boyutuna sahip adayları alalım Rütbesel sezgi için
    candidates = [cell for cell in emptyCells if len(domains[cell]) == smallest_domain_size]

    # Eğer eşitlik yoksa direk dönebiliriz sonucu
    if len(candidates) == 1:
        return candidates[0]

    # 2) Degree Heuristic: Kısıtı en fazla olan hücreyi seçelim
    def degree_of(cell):
        r, c = cell
        degreeCount = 0 #kısıtları tek tek sayıyoruz yani 0 sayısı

        # Satır
        for i in range(9):
            if board[r][i] == 0 and i != c:
                degreeCount += 1
            if board[i][c] == 0 and i != r:
                degreeCount += 1
        # 3x3 kare
        sr, sc = 3*(r//3), 3*(c//3)
        for j in range(sr, sr+3):
            for i in range(sc, sc+3):
                if (j, i) != (r, c) and board[j][i] == 0:
                    degreeCount += 1

        return degreeCount

    # En çok dereceye sahip olan hücreyi bul (kısıtı en fazla)
    best_cell = max(candidates, key=degree_of)
    return best_cell

def SudokuSolver(board, domains):
    """
    Backtracking algoritmasının uygulandığı method 
    Backtracking + Forward Checking + MRV + Degree Heuristic birleştirilmiş çözüm.
    """
    # Hücre seçimi: MRV + Rütbesel Sezgi
    row, col = nextCell(board, domains)
    
    # çözüm tamam
    if row == -1 and col == -1:
        return True

    # O hücrenin domainindeki değerleri deneyelim
    for num in domains[(row, col)]: #tüm sayıları gezmek için
        if isValid(board, row, col, num): # Uygunluk kontrolü
            updatedDomains = forwardChecking(domains, row, col, num) #forward checking
            if updatedDomains is not None:
                board[row][col] = num  # Hücreye yerleştir

                if SudokuSolver(board, updatedDomains): #recursive call
                    return True

                # Başarısızsa geri al
                board[row][col] = 0

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
                domain = startingDomains(selected_board)
                solved_board = SudokuSolver(selected_board,domain)
                
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