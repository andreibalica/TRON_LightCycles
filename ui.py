import pygame
from settings import *

class Button:
    def __init__(self, text, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.rendered_text = font.render(text, True, TEXT_COLOR)
        self.text_position = self.rendered_text.get_rect(center=self.rect.center)
        self.mouse_over = False

    def draw(self, surface):
        color = MOUSE_OVER_COLOR if self.mouse_over else BTN_COLOR
        s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        s.fill((*color, 200))
        surface.blit(s, self.rect.topleft)
        
        pygame.draw.rect(surface, (255,255,255), self.rect, 2)
        surface.blit(self.rendered_text, self.text_position)

    def check_mouse_over(self, mouse_pos):
        self.mouse_over = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.mouse_over
        return False