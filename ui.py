import pygame
import os

WHITE = (255, 255, 255)
GREEN = (0, 255, 100)
RED = (255, 50, 50)
GRAY = (100, 110, 120)
DARK_GRAY = (30, 40, 50)
LIGHT_BLUE = (100, 200, 255)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        
        sound_files = {
            'select': 'select.wav',
            'landing': 'landing.wav',
            'alarm': 'alarm.wav',
            'collision': 'collision.wav'
        }
        
        for name, file in sound_files.annotate_items() if hasattr(sound_files, 'annotate_items') else sound_files.items():
            if os.path.exists(file):
                try:
                    self.sounds[name] = pygame.mixer.Sound(file)
                except Exception as e:
                    print(f"Error loading sound {file}: {e}")
            else:
                print(f"Warning: Sound file {file} not found.")

        self.alarm_playing = False

    def play(self, name):
        if name in self.sounds:
            if name == 'alarm':
                if not self.alarm_playing:
                    self.sounds['alarm'].play(-1)
                    self.alarm_playing = True
            else:
                self.sounds[name].play()

    def stop_alarm(self):
        if 'alarm' in self.sounds and self.alarm_playing:
            self.sounds['alarm'].stop()
            self.alarm_playing = False


class UIManager:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 14)
        self.large_font = pygame.font.SysFont("Arial", 36)
        
        self.runway_width = 160
        self.runway_height = 20
        self.runway_rect = pygame.Rect(
            (SCREEN_WIDTH - self.runway_width) // 2,
            (SCREEN_HEIGHT - self.runway_height) // 2,
            self.runway_width,
            self.runway_height
        )

    def draw_radar_rings(self, surface):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        for radius in [100, 200, 300, 400]:
            pygame.draw.circle(surface, (20, 35, 60), (center_x, center_y), radius, 1)

    def draw_runway(self, surface):
        pygame.draw.rect(surface, DARK_GRAY, self.runway_rect)
        pygame.draw.rect(surface, WHITE, self.runway_rect, 2)
        
        dash_y = self.runway_rect.centery
        start_x = self.runway_rect.left + 10
        end_x = self.runway_rect.right - 10
        
        for x in range(start_x, end_x, 20):
            pygame.draw.line(surface, WHITE, (x, dash_y), (x + 10, dash_y), 2)

    def draw_hud(self, surface, score, high_score, spawn_rate):
        score_lbl = self.font.render(f"SCORE: {score}", True, WHITE)
        high_score_lbl = self.font.render(f"HIGH SCORE: {high_score}", True, GREEN)
        spawn_lbl = self.font.render(f"SPAWN INTERVAL: {spawn_rate / 1000:.1f}s", True, WHITE)
        info_lbl = self.font.render("F: Fullscreen | ESC: Quit | Arrow Keys: Steer selected", True, GRAY)
        
        surface.blit(score_lbl, (20, 20))
        surface.blit(high_score_lbl, (20, 45))
        surface.blit(spawn_lbl, (20, 70))
        surface.blit(info_lbl, (20, SCREEN_HEIGHT - 35))

    def draw_game_over(self, surface, reason):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        go_lbl = self.large_font.render("GAME OVER", True, RED)
        go_rect = go_lbl.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        surface.blit(go_lbl, go_rect)

        reason_lbl = self.font.render(reason, True, WHITE)
        reason_rect = reason_lbl.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        surface.blit(reason_lbl, reason_rect)

        restart_lbl = self.font.render("Press 'R' to restart or 'ESC' to quit", True, LIGHT_BLUE)
        restart_rect = restart_lbl.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        surface.blit(restart_lbl, restart_rect)