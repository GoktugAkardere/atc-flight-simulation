import pygame
import os

WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
RED = (255, 50, 50)
GRAY = (100, 100, 100)
ORANGE = (255, 140, 0)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750

# 🔊 SOUND MANAGER (Akıllı Ses Sistemi)
# Dosyalar klasörde yoksa çökmek yerine oyunu sessiz modda çalıştırır.
class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.enabled = True
        except:
            self.enabled = False
            
        self.sounds = {}
        if self.enabled:
            # Yüklemek istediğimiz seslerin listesi
            sound_files = {
                'select': 'select.wav',
                'landing': 'landing.wav',
                'collision': 'collision.wav',
                'alarm': 'alarm.wav'
            }
            for key, filename in sound_files.items():
                try:
                    if os.path.exists(filename):
                        self.sounds[key] = pygame.mixer.Sound(filename)
                    else:
                        self.sounds[key] = None
                except:
                    self.sounds[key] = None

    def play(self, key):
        if self.enabled and key in self.sounds and self.sounds[key]:
            try:
                # Alarm sesi çalarken zaten çalıyorsa üst üste binmesin diye kontrol
                if key == 'alarm':
                    # Her yarım saniyede bir dıt dıt çalması için kanal meşguliyet kontrolü
                    if not pygame.mixer.Channel(1).get_busy():
                        pygame.mixer.Channel(1).play(self.sounds[key])
                else:
                    self.sounds[key].play()
            except:
                pass

class UIManager:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 14)
        self.large_font = pygame.font.SysFont("Arial", 28)
        self.runway_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 10, 200, 20)

    def draw_radar_rings(self, surface):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        for radius in [150, 300, 450]:
            pygame.draw.circle(surface, (20, 35, 60), (center_x, center_y), radius, 1)

    def draw_runway(self, surface):
        pygame.draw.rect(surface, GRAY, self.runway_rect)
        pygame.draw.line(surface, WHITE, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2), 1)

    def draw_hud(self, surface, score, high_score, current_spawn_rate):
        score_lbl = self.large_font.render(f"SCORE: {score}", True, WHITE)
        high_lbl = self.large_font.render(f"HIGH SCORE: {high_score}", True, YELLOW)
        rate_lbl = self.font.render(f"TRAFFIC LEVEL: {round(4000 / current_spawn_rate, 1)}x", True, ORANGE)
        
        surface.blit(score_lbl, (20, 20))
        surface.blit(high_lbl, (20, 60))
        surface.blit(rate_lbl, (20, 100))

    def draw_game_over(self, surface, reason):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((10, 10, 10))
        surface.blit(overlay, (0, 0))

        over_lbl = self.large_font.render("GAME OVER", True, RED)
        reason_lbl = self.font.render(reason, True, WHITE)
        restart_lbl = self.large_font.render("Press 'R' to Restart", True, YELLOW)
        
        surface.blit(over_lbl, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 60))
        surface.blit(reason_lbl, (SCREEN_WIDTH // 2 - len(reason)*3.5, SCREEN_HEIGHT // 2 - 10))
        surface.blit(restart_lbl, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 30))