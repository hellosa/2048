import pygame
import random

# 初始化 pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
GRID_COLOR = (187, 173, 160)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# 设置窗口大小
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
CELL_SIZE = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2048')

font = pygame.font.SysFont('Arial', 40)

def draw_board(board):
    for y in range(4):
        for x in range(4):
            pygame.draw.rect(screen, GRID_COLOR, pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if board[y][x] != 0:
                color = TILE_COLORS.get(board[y][x], (0, 0, 0))
                text = font.render(str(board[y][x]), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x*CELL_SIZE + CELL_SIZE//2, y*CELL_SIZE + CELL_SIZE//2))
                
                # 减小 cell 的大小以创建分界线
                pygame.draw.rect(screen, color, pygame.Rect(x*CELL_SIZE + 5, y*CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))
                screen.blit(text, text_rect)

def initialize_game():
    board = [[0 for _ in range(4)] for _ in range(4)]
    add_tile(board)
    add_tile(board)
    return board


def add_tile(board):
    empty_cells = [(x, y) for y in range(4) for x in range(4) if board[y][x] == 0]
    (x, y) = random.choice(empty_cells)
    board[y][x] = random.choice([2, 4])

def move(board, direction):
    # direction: 2=Up, 1=Right, 0=Down, 3=Left
    rotated_board = [row[:] for row in board]
    # 这部分代码的目的是将游戏板旋转，使我们只需要处理从右向左的移动
    for _ in range((direction + 1) % 4):  # 调整旋转的方向
        rotated_board = [list(row) for row in zip(*rotated_board[::-1])]

    for row in rotated_board:
        merged = [False] * 4  # 用于跟踪哪些数字已经翻倍过
        while 0 in row:
            row.remove(0)
        while len(row) < 4:
            row.append(0)
        i = 3
        while i > 0:
            if row[i] == row[i-1] and row[i] != 0 and not merged[i] and not merged[i-1]:  # 检查 merged 标志
                row[i-1] *= 2
                row[i] = 0
                merged[i-1] = True  # 标记该数字已翻倍
                i -= 2  # 跳过下一个数字，因为它已经合并
            else:
                i -= 1

    for _ in range((3 - direction) % 4):  # 调整旋转回原始方向
        rotated_board = [list(row) for row in zip(*rotated_board[::-1])]

    return rotated_board


def main():
    board = initialize_game()
    running = True

    while running:
        screen.fill(WHITE)
        draw_board(board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT):
                    directions = {
                        pygame.K_UP: 2,
                        pygame.K_RIGHT: 1,
                        pygame.K_DOWN: 0,
                        pygame.K_LEFT: 3
                    }
                    new_board = move(board, directions[event.key])
                    if new_board != board:
                        board = new_board
                        add_tile(board)

    pygame.quit()


if __name__ == '__main__':
    main()

