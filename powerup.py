import pygame
import random
from settings import *

class PowerUp:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE)
        self.active = False
        self.type = "ERASER"
        self.color = PWR_ERASER
    
    def spawn(self):
        if not self.active:
            cx = random.randint(1, (WIDTH // GRID_SIZE) - 2) * GRID_SIZE
            cy = random.randint(1, (HEIGHT // GRID_SIZE) - 2) * GRID_SIZE
            self.rect.topleft = (cx, cy)
            self.active = True

            roll = random.randint(1, 100)
            if roll < 50: 
                self.type = "ERASER"
                self.color = PWR_ERASER
            elif roll < 80:
                self.type = "FREEZE"
                self.color = PWR_FREEZE
            else:
                self.type = "GHOST"
                self.color = PWR_GHOST

    def draw(self, surface):
        if self.active:
            cx = self.rect.x + GRID_SIZE // 2
            cy = self.rect.y + GRID_SIZE // 2
            pulse = (pygame.time.get_ticks() % 500) / 500
            size = GRID_SIZE // 2 + int(pulse * 2)
            
            pygame.draw.circle(surface, self.color, (cx, cy), size)
            pygame.draw.circle(surface, (255, 255, 255), (cx, cy), GRID_SIZE // 4)