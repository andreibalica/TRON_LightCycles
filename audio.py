import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sound_boom = None
        self.sound_power = None
        self.sound_countdown = None
        self.sound_click = None
        
        self.load_sounds()

        self.sound_map = {
            "boom": self.sound_boom,
            "power": self.sound_power,
            "countdown": self.sound_countdown,
            "click": self.sound_click,
        }
    
    def load_sounds(self):
        try:
            self.sound_boom = pygame.mixer.Sound("crash.mp3")
            self.sound_power = pygame.mixer.Sound("point.mp3")
            self.sound_countdown = pygame.mixer.Sound("beep.mp3")
            self.sound_click = pygame.mixer.Sound("click.mp3")

            self.sound_boom.set_volume(0.5)
            self.sound_power.set_volume(0.5)
            self.sound_countdown.set_volume(0.6)
            self.sound_click.set_volume(0.4)
            
            print("SFX (MP3) loaded.")
        except Exception as e:
            print(f"Could not find all audio files: {e}")
    
    def play_music(self, track_type):
        try:
            if track_type == "intro":
                pygame.mixer.music.load("intro.mp3")
                pygame.mixer.music.set_volume(0.4)
            elif track_type == "game":
                pygame.mixer.music.load("game.mp3")
                pygame.mixer.music.set_volume(0.15)
            
            pygame.mixer.music.play(-1, fade_ms=2000)
        except Exception as e:
            print(f"Could not find music file: {track_type}.mp3 - {e}")
    
    def pause_music(self):
        pygame.mixer.music.pause()
    
    def play_sound(self, sound_name):
        sound = self.sound_map.get(sound_name)
        if sound:
            sound.play()
    
    def stop_sound(self, sound_name):
        sound = self.sound_map.get(sound_name)
        if sound:
            sound.stop()
