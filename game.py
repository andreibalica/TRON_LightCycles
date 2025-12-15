import pygame
import sys
import random

from settings import *
from ui import Button
from powerup import PowerUp
from player import LightCycle
from ai_player import AIPlayer
from audio import AudioManager

class Game:
    
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TRON: Ultimate Edition")
        self.clock = pygame.time.Clock()
        
        self.audio = AudioManager()
        
        self.font_big = pygame.font.SysFont("arialblack", 50)
        self.font_ui = pygame.font.SysFont("arialblack", 30)
        self.font_hud = pygame.font.SysFont("monospace", 30, bold=True)
        self.font_small = pygame.font.SysFont("monospace", 15)

        self.score1 = 0
        self.score2 = 0
        self.winner_msg = ""
        
        self.shake_offset = [0, 0]
        self.shake_timer = 0
        self.countdown_timer = 0
        self.countdown_beep_played = False
        self.crash_delay = 0

        self.state = MENU_START
        self.mode = "SINGLE"
        
        self.load_background()
        self.init_ui()
        self.audio.play_music("intro")

    def load_background(self):
        try:
            bg_img = pygame.image.load("background.jpg").convert()
            self.background = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
            dark = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
            dark.fill((0, 0, 0, 100))
            self.background.blit(dark, (0, 0))
            print("Background loaded.")
        except:
            print("Background.jpg missing. Using generated background.")
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((10, 10, 30))
            for x in range(0, WIDTH, 40):
                pygame.draw.line(self.background, (30, 30, 50), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, 40):
                pygame.draw.line(self.background, (30, 30, 50), (0, y), (WIDTH, y))

    def init_ui(self):
        cx = WIDTH // 2
        self.btn_start = Button("START GAME", cx - 150, 350, 300, 60, self.font_ui)
        self.btn_1p = Button("1 PLAYER (vs AI)", cx - 160, 250, 320, 60, self.font_ui)
        self.btn_2p = Button("2 PLAYERS (PvP)", cx - 160, 350, 320, 60, self.font_ui)

    def start_match(self):
        self.score1 = 0
        self.score2 = 0
        self.audio.play_music("game")
        self.start_round()

    def start_round(self):
        c1 = (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT)
        c2 = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT)
        
        self.p1 = LightCycle(GRID_SIZE * 4, HEIGHT // 2, P1_COLOR, c1)
        self.p1.crashed = False
        
        if self.mode == "SINGLE":
            self.p2 = AIPlayer(WIDTH - GRID_SIZE * 5, HEIGHT // 2, BOT_COLOR)
        else:
            self.p2 = LightCycle(WIDTH - GRID_SIZE * 5, HEIGHT // 2, P2_COLOR, c2)
        self.p2.crashed = False
            
        self.powerups = []
        self.countdown_timer = 4 * FPS
        self.countdown_beep_played = False
        self.state = COUNTDOWN

    def spawn_explosion(self):
        self.audio.pause_music()
        self.audio.play_sound("boom")
        self.shake_timer = 15
    
    def apply_shake(self):
        if self.shake_timer > 0:
            self.shake_offset[0] = random.randint(-8, 8)
            self.shake_offset[1] = random.randint(-8, 8)
            self.shake_timer -= 1
        else:
            self.shake_offset = [0, 0]

    def handle_events(self):
        mouse = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.state == MENU_START:
                if self.btn_start.is_clicked(e):
                    self.audio.play_sound("click")
                    self.state = MENU_MODE
            
            elif self.state == MENU_MODE:
                if self.btn_1p.is_clicked(e):
                    self.audio.play_sound("click")
                    self.mode = "SINGLE"
                    self.start_match()
                elif self.btn_2p.is_clicked(e):
                    self.audio.play_sound("click")
                    self.mode = "MULTI"
                    self.start_match()
            
            elif self.state == GAME_OVER:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    self.audio.play_music("intro")
                    self.state = MENU_START

        if self.state == PLAYING:
            keys = pygame.key.get_pressed()
            self.p1.handle_input(keys)
            if not isinstance(self.p2, AIPlayer):
                self.p2.handle_input(keys)

        if self.state == MENU_START:
            self.btn_start.check_mouse_over(mouse)
        elif self.state == MENU_MODE:
            self.btn_1p.check_mouse_over(mouse)
            self.btn_2p.check_mouse_over(mouse)

    def update_countdown(self):
        if not self.countdown_beep_played:
            self.audio.play_sound("countdown")
            self.countdown_beep_played = True
        
        self.countdown_timer -= 1
        
        if self.countdown_timer < 0:
            self.state = PLAYING
    
    def update_ai(self):
        if isinstance(self.p2, AIPlayer):
            all_trails = self.p1.trail + self.p2.trail
            self.p2.ai_logic(all_trails)
    
    def spawn_powerups(self):
        if len(self.powerups) < 3 and random.randint(0, 100) < 3:
            new_powerup = PowerUp()
            new_powerup.spawn()
            if new_powerup.active:
                self.powerups.append(new_powerup)
    
    def handle_collisions(self):
        h1 = self.check_collision(self.p1, self.p2)
        h2 = self.check_collision(self.p2, self.p1)

        if h1 or h2:
            if self.crash_delay == 0:
                if h1:
                    self.spawn_explosion()
                    self.p1.crashed = True
                if h2:
                    self.spawn_explosion()
                    self.p2.crashed = True
                
                self.crash_delay = FPS * 2
            
            self.crash_delay -= 1
            if self.crash_delay <= 0:
                if h1 and h2:
                    self.end_round(0)
                elif h1:
                    self.end_round(2)
                elif h2:
                    self.end_round(1)
                self.crash_delay = 0
    
    def handle_powerup_pickups(self):
        for powerup in self.powerups[:]:
            if powerup.active:
                hit_p = None
                if self.p1.rect.colliderect(powerup.rect):
                    hit_p = self.p1
                elif self.p2.rect.colliderect(powerup.rect):
                    hit_p = self.p2
                
                if hit_p:
                    self.audio.play_sound("power")
                    self.powerups.remove(powerup)
                    
                    if powerup.type == "ERASER":
                        self.p1.trail = []
                        self.p2.trail = []
                    elif powerup.type == "GHOST":
                        hit_p.ghost_timer = 120
                    elif powerup.type == "FREEZE":
                        enemy = self.p2 if hit_p == self.p1 else self.p1
                        enemy.freeze_timer = 75

    def update(self):
        if self.state == COUNTDOWN:
            self.update_countdown()
            return
        
        if self.state != PLAYING:
            return
        
        self.apply_shake()
        self.update_ai()
        self.spawn_powerups()
        
        self.handle_powerup_pickups()
        
        if self.crash_delay == 0:
            self.p1.update()
            self.p2.update()
        
        self.handle_collisions()

    def check_collision(self, player, enemy):
        if player.ghost_timer > 0:
            return False

        if not (0 <= player.rect.x < WIDTH and 0 <= player.rect.y < HEIGHT):
            return True
        
        trails = player.trail[:-2] + enemy.trail
        if player.rect.collidelist(trails) != -1:
            return True
        
        return False

    def end_round(self, winner_idx):
        if winner_idx == 1:
            self.score1 += 1
        elif winner_idx == 2:
            self.score2 += 1
        
        self.audio.play_music("game")

        if self.score1 >= WIN_SCORE:
            self.winner_msg = "PLAYER 1 WINS!"
            self.state = GAME_OVER
        elif self.score2 >= WIN_SCORE:
            self.winner_msg = "PLAYER 2 WINS!"
            self.state = GAME_OVER
        else:
            self.start_round()

    def draw_turbo_bars(self):
        bar_width = 150
        bar_height = 15
        
        p1_bar_x = 20
        p1_bar_y = HEIGHT - 40
        pygame.draw.rect(self.screen, (50, 50, 50), (p1_bar_x, p1_bar_y, bar_width, bar_height))
        p1_fill = int((self.p1.turbo_bar / self.p1.turbo_max) * bar_width)
        if self.p1.turbo_bar < 30:
            bar_color = (255, 50, 50)
        elif self.p1.turbo_bar < 70:
            bar_color = (255, 255, 0)
        else:
            bar_color = (0, 255, 255)
        pygame.draw.rect(self.screen, bar_color, (p1_bar_x, p1_bar_y, p1_fill, bar_height))
        pygame.draw.rect(self.screen, TEXT_COLOR, (p1_bar_x, p1_bar_y, bar_width, bar_height), 2)
        turbo_txt = self.font_small.render("TURBO", True, TEXT_COLOR)
        self.screen.blit(turbo_txt, (p1_bar_x, p1_bar_y - 18))
        
        p2_bar_x = WIDTH - bar_width - 20
        p2_bar_y = HEIGHT - 40
        pygame.draw.rect(self.screen, (50, 50, 50), (p2_bar_x, p2_bar_y, bar_width, bar_height))
        p2_fill = int((self.p2.turbo_bar / self.p2.turbo_max) * bar_width)
        if self.p2.turbo_bar < 30:
            bar_color = (255, 50, 50)
        elif self.p2.turbo_bar < 70:
            bar_color = (255, 255, 0)
        else:
            bar_color = (255, 50, 255)
        pygame.draw.rect(self.screen, bar_color, (p2_bar_x, p2_bar_y, p2_fill, bar_height))
        pygame.draw.rect(self.screen, TEXT_COLOR, (p2_bar_x, p2_bar_y, bar_width, bar_height), 2)
        turbo_txt = self.font_small.render("TURBO", True, TEXT_COLOR)
        self.screen.blit(turbo_txt, (p2_bar_x, p2_bar_y - 18))
    
    def draw(self):
        if self.state in [MENU_START, MENU_MODE]:
            self.screen.blit(self.background, self.shake_offset)
        else:
            self.screen.fill((0, 0, 0))
            if self.shake_offset != [0, 0]:
                temp = pygame.Surface((WIDTH, HEIGHT))
                temp.fill((0, 0, 0))
                self.screen.blit(temp, self.shake_offset)
        
        if self.state == MENU_START:
            t = self.font_big.render("TRON: LIGHT CYCLES", True, P1_COLOR)
            s_rect = t.get_rect(center=(WIDTH // 2, 150))
            self.screen.blit(t, s_rect)
            self.btn_start.draw(self.screen)
        
        elif self.state == MENU_MODE:
            t = self.font_ui.render("SELECT MODE", True, TEXT_COLOR)
            s_rect = t.get_rect(center=(WIDTH // 2, 150))
            self.screen.blit(t, s_rect)
            self.btn_1p.draw(self.screen)
            self.btn_2p.draw(self.screen)

        elif self.state == COUNTDOWN:
            for powerup in self.powerups:
                powerup.draw(self.screen)
            self.p1.draw(self.screen)
            self.p2.draw(self.screen)
            
            s_txt = self.font_hud.render(f"{self.score1} - {self.score2}", True, TEXT_COLOR)
            self.screen.blit(s_txt, (WIDTH // 2 - s_txt.get_width() // 2, 10))
            
            self.draw_turbo_bars()
            
            count_num = self.countdown_timer // FPS
            if count_num >= 1 and count_num <= 3:
                cnt_txt = self.font_big.render(str(count_num), True, (255, 255, 0))
                self.screen.blit(cnt_txt, (WIDTH // 2 - cnt_txt.get_width() // 2, HEIGHT // 2 - 50))
            elif count_num == 0:
                start_txt = self.font_big.render("START!", True, (0, 255, 0))
                self.screen.blit(start_txt, (WIDTH // 2 - start_txt.get_width() // 2, HEIGHT // 2 - 50))
        
        elif self.state == PLAYING or self.state == GAME_OVER:
            for powerup in self.powerups:
                powerup.draw(self.screen)
            self.p1.draw(self.screen)
            self.p2.draw(self.screen)

            s_txt = self.font_hud.render(f"{self.score1} - {self.score2}", True, TEXT_COLOR)
            self.screen.blit(s_txt, (WIDTH // 2 - s_txt.get_width() // 2, 10))
            
            self.draw_turbo_bars()
            
            if self.p1.ghost_timer > 0:
                lbl = self.font_small.render("GHOST", True, PWR_GHOST)
                self.screen.blit(lbl, (10, 10))
            if self.p2.ghost_timer > 0:
                lbl = self.font_small.render("GHOST", True, PWR_GHOST)
                self.screen.blit(lbl, (WIDTH - 60, 10))
            if self.p1.freeze_timer > 0:
                lbl = self.font_small.render("FROZEN", True, PWR_FREEZE)
                self.screen.blit(lbl, (10, 30))
            if self.p2.freeze_timer > 0:
                lbl = self.font_small.render("FROZEN", True, PWR_FREEZE)
                self.screen.blit(lbl, (WIDTH - 70, 30))

            if self.state == GAME_OVER:
                over = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                over.fill((0, 0, 0, 200))
                self.screen.blit(over, (0, 0))
                
                w = self.font_big.render(self.winner_msg, True, P1_COLOR)
                self.screen.blit(w, (WIDTH // 2 - w.get_width() // 2, HEIGHT // 2 - 50))
                r = self.font_small.render("Press SPACE to Restart", True, TEXT_COLOR)
                self.screen.blit(r, (WIDTH // 2 - r.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
