import pygame
import random

# 颜色定义
COLORS = [
    (0, 0, 0),         # 黑色（背景）
    (255, 0, 0),       # 红色
    (0, 150, 0),       # 绿色
    (0, 0, 255),       # 蓝色
    (255, 120, 0),     # 橙色
    (255, 255, 0),     # 黄色
    (180, 0, 255),     # 紫色
    (0, 220, 220)      # 青色
]

# 方块形状（7种经典俄罗斯方块）
SHAPES = [
    [[1, 1, 1, 1]],    # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],        # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

class Tetris:
    def __init__(self, width=10, height=20, block_size=30):
        pygame.init()
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen = pygame.display.set_mode((width*block_size + 150, height*block_size))
        pygame.display.set_caption("俄罗斯方块")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.grid = [[0] * self.width for _ in range(self.height)]
        self.score = 0
        self.new_piece()
        
    def new_piece(self):
        self.current_shape = random.choice(SHAPES)
        self.current_color = random.randint(1, len(COLORS)-1)
        self.current_x = self.width // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        
        if self.check_collision(self.current_x, self.current_y, self.current_shape):
            self.reset_game()  # 游戏结束

    def check_collision(self, x, y, shape):
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col]:
                    new_x = x + col
                    new_y = y + row
                    if (new_x < 0 or new_x >= self.width or
                        new_y >= self.height or
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return True
        return False

    def rotate_shape(self):
        rotated = [[self.current_shape[y][x]
                   for y in range(len(self.current_shape))]
                   for x in reversed(range(len(self.current_shape[0])))]
        if not self.check_collision(self.current_x, self.current_y, rotated):
            self.current_shape = rotated

    def move(self, dx, dy):
        new_x = self.current_x + dx
        new_y = self.current_y + dy
        if not self.check_collision(new_x, new_y, self.current_shape):
            self.current_x = new_x
            self.current_y = new_y
            return True
        return False

    def drop(self):
        while self.move(0, 1):
            pass
        self.fix_piece()

    def fix_piece(self):
        for row in range(len(self.current_shape)):
            for col in range(len(self.current_shape[row])):
                if self.current_shape[row][col]:
                    self.grid[self.current_y + row][self.current_x + col] = self.current_color
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        lines_cleared = 0
        new_grid = []
        for row in self.grid:
            if 0 in row:
                new_grid.append(row)
            else:
                lines_cleared += 1
        self.score += lines_cleared ** 2 * 100
        self.grid = [[0]*self.width for _ in range(lines_cleared)] + new_grid

    def draw_block(self, x, y, color):
        pygame.draw.rect(self.screen, COLORS[color],
                         (x*self.block_size, y*self.block_size,
                          self.block_size-1, self.block_size-1))

    def draw(self):
        self.screen.fill(COLORS[0])
        
        # 绘制游戏区域
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x]:
                    self.draw_block(x, y, self.grid[y][x])
        
        # 绘制当前方块
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[y])):
                if self.current_shape[y][x]:
                    self.draw_block(self.current_x + x, self.current_y + y, self.current_color)
        
        # 绘制得分
        font = pygame.font.SysFont('arial', 30)
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(text, (self.width*self.block_size + 20, 50))
        
        pygame.display.update()

    def run(self):
        fall_time = 0
        fall_speed = 500  # 毫秒
        
        while True:
            self.clock.tick(60)
            current_time = pygame.time.get_ticks()
            fall_time += current_time - self.last_time
            self.last_time = current_time
            
            if fall_time >= fall_speed:
                if not self.move(0, 1):
                    self.fix_piece()
                fall_time = 0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_shape()
                    elif event.key == pygame.K_SPACE:
                        self.drop()
            
            self.draw()

if __name__ == '__main__':
    game = Tetris()
    game.last_time = pygame.time.get_ticks()
    game.run()