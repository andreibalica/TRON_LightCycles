import pygame
from settings import *

class LightCycle:
    
    def __init__(self, x, y, color, controls=None):
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        self.color = color
        self.original_color = color
        self.controls = controls
        
        self.trail = []
        self.dir_x = -GRID_SIZE if x > WIDTH/2 else GRID_SIZE
        self.dir_y = 0
        
        self.ghost_timer = 0
        self.freeze_timer = 0
        self.turbo_active = False
        self.crashed = False
        
        self.turbo_bar = 100
        self.turbo_max = 100
        self.turbo_drain_rate = 4
        self.turbo_recharge_rate = 1

    def handle_input(self, keys):
        if not self.controls:
            return
        
        up, down, left, right, turbo_key = self.controls
        
        if keys[up] and self.dir_y == 0:
            self.dir_x, self.dir_y = 0, -GRID_SIZE
        elif keys[down] and self.dir_y == 0:
            self.dir_x, self.dir_y = 0, GRID_SIZE
        elif keys[left] and self.dir_x == 0:
            self.dir_x, self.dir_y = -GRID_SIZE, 0
        elif keys[right] and self.dir_x == 0:
            self.dir_x, self.dir_y = GRID_SIZE, 0
        
        self.turbo_active = keys[turbo_key] and self.turbo_bar > 0 and self.freeze_timer == 0

    def update(self):
        if self.ghost_timer > 0:
            self.ghost_timer -= 1
            if (self.ghost_timer // 5) % 2 == 0:
                self.color = (255, 255, 255)
            else:
                self.color = self.original_color
        else:
            self.color = self.original_color

        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            return
        
        if self.turbo_active:
            self.turbo_bar -= self.turbo_drain_rate
            if self.turbo_bar <= 0:
                self.turbo_bar = 0
                self.turbo_active = False
        else:
            self.turbo_bar += self.turbo_recharge_rate
            if self.turbo_bar > self.turbo_max:
                self.turbo_bar = self.turbo_max

        speed = 1
        if self.turbo_active:
            speed = 2
        
        self.trail.append(self.rect.copy())
        
        if speed == 2:
            mid_rect = self.rect.copy()
            mid_rect.x += self.dir_x
            mid_rect.y += self.dir_y
            self.trail.append(mid_rect)
        
        self.rect.x += int(self.dir_x * speed)
        self.rect.y += int(self.dir_y * speed)
        
        if len(self.trail) > MAX_TRAIL_LENGTH:
            self.trail.pop(0)

    def draw(self, surface):
        for segment in self.trail:
            col = self.original_color if self.ghost_timer == 0 else (100, 100, 100)
            pygame.draw.rect(surface, col, segment)
            pygame.draw.rect(surface, BG_COLOR, segment, 1)
        if not self.crashed:
            pygame.draw.rect(surface, (255, 255, 255), self.rect)