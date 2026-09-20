import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Размеры экрана и игровой сетки
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

# Создание игрового окна
screen = pygame.display.set_index((WIDTH, HEIGHT))
pygame.display.set_caption('Змейка на Python')

# Настройка таймера для управления FPS (скоростью игры)
clock = pygame.time.Clock()

def run_game():
    # Начальные параметры змейки
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0
    
    snake_body = [[x, y]]
    snake_length = 1

    # Генерация первой еды
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    while True:
        # 1. Обработка событий (нажатия клавиш)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, BLOCK_SIZE

        # 2. Обновление позиции головы змейки
        x += dx
        y += dy

        # Проверка столкновения со стенами
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            break  # Конец игры

        # Движение тела змейки
        snake_body.append([x, y])
        if len(snake_body) > snake_length:
            del snake_body[0]

        # Проверка столкновения с самим собой
        for part in snake_body[:-1]:
            if part == [x, y]:
                break
        else:
            # 3. Логика поедания пищи
            if x == food_x and y == food_y:
                food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                snake_length += 1

            # 4. Отрисовка объектов на экране
            screen.fill(BLACK)
            
            # Рисуем еду
            pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
            
            # Рисуем змейку
            for part in snake_body:
                pygame.draw.rect(screen, GREEN, [part[0], part[1], BLOCK_SIZE, BLOCK_SIZE])

            # Отображение счета
            font = pygame.font.SysFont("bahnschrift", 25)
            score_text = font.render(f"Счёт: {snake_length - 1}", True, WHITE)
            screen.blit(score_text, [10, 10])

            pygame.display.update()
            
            # Контроль скорости змейки (10 кадров в секунду)
            clock.tick(10)
            continue
        break

    # Если вылетели из цикла — игра окончена
    print(f"Игра окончена! Ваш финальный счёт: {snake_length - 1}")
    pygame.quit()

if __name__ == "__main__":
    run_game()
