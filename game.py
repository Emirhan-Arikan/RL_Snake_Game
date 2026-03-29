import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

# Yönleri belirlemek için Enum sınıfı
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# Renk sabitleri
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 40 # Eğitimi hızlandırmak için bu değeri artırabilirsin (Örn: 80, 100)

class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # Ekranı oluştur
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Yapay Zeka Yılan Oyunu')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # Oyun başlangıç durumu
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0 # Yapay zekanın sonsuz döngüye girmesini önlemek için

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE ) // BLOCK_SIZE ) * BLOCK_SIZE 
        y = random.randint(0, (self.h - BLOCK_SIZE ) // BLOCK_SIZE ) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def step(self, action):
        self.frame_iteration += 1
        
        # 1. Kullanıcı girdilerini kontrol et (Pencereyi kapatmak için)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. Yılanı hareket ettir
        self._move(action) # Aksiyonu uygula
        self.snake.insert(0, self.head)
        
        # 3. Oyun bitti mi kontrol et
        reward = 0
        game_over = False
        # Çarpışma var mı veya yapay zeka çok uzun süre boş mu dolandı?
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10 # Ceza!
            return reward, game_over, self.score
            
        # 4. Yem yedi mi?
        if self.head == self.food:
            self.score += 1
            reward = 10 # Ödül!
            self._place_food()
        else:
            self.snake.pop() # Yem yemediyse kuyruğun sonunu sil (ilerleme efekti)
        
        # 5. Ekranı güncelle
        self._update_ui()
        self.clock.tick(SPEED)
        
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Sınırlara çarpma kontrolü
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # Kendine çarpma kontrolü
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        
        # Yılanı çiz
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        # Yemi çiz
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Skoru yaz
        text = font.render("Skor: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # Aksiyonlar -> [Düz Git, Sağa Dön, Sola Dön]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # Düz devam et
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # Sağa dön
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # Sola dön

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)