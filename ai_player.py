import pygame
import random
from settings import *
from player import LightCycle

class AIPlayer(LightCycle):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color, controls=None)
    
    def handle_input(self, keys):
        pass
    
    def check_collision_ahead(self, obstacles):
        fx = self.rect.x + self.dir_x
        fy = self.rect.y + self.dir_y
        f_rect = pygame.Rect(fx, fy, GRID_SIZE, GRID_SIZE)
        
        if not (0 <= fx < WIDTH and 0 <= fy < HEIGHT):
            return True
        if f_rect.collidelist(obstacles) != -1:
            return True
        return False
    
    def find_safe_direction(self, obstacles):
        if self.dir_x != 0:
            moves = [(0, -GRID_SIZE), (0, GRID_SIZE)]
        else:
            moves = [(-GRID_SIZE, 0), (GRID_SIZE, 0)]
        
        random.shuffle(moves)
        
        for nx, ny in moves:
            tr = pygame.Rect(self.rect.x + nx, self.rect.y + ny, GRID_SIZE, GRID_SIZE)
            if (0 <= tr.x < WIDTH and 0 <= tr.y < HEIGHT) and tr.collidelist(obstacles) == -1:
                return nx, ny
        
        return moves[0]
    
    def ai_logic(self, obstacles):
        collision_1 = self.check_collision_ahead(obstacles)
        
        if collision_1:
            self.turbo_active = False
            new_dir = self.find_safe_direction(obstacles)
            self.dir_x, self.dir_y = new_dir
            return
        
        fx2 = self.rect.x + self.dir_x * 2
        fy2 = self.rect.y + self.dir_y * 2
        r2 = pygame.Rect(fx2, fy2, GRID_SIZE, GRID_SIZE)
        collision_2 = (fx2 < 0 or fx2 >= WIDTH or fy2 < 0 or fy2 >= HEIGHT or 
                      r2.collidelist(obstacles) != -1)
        
        if collision_2:
            self.turbo_active = False
        elif self.turbo_bar > 70:
            self.turbo_active = (random.randint(0, 100) < 20)
        else:
            self.turbo_active = False
