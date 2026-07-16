import pygame
import random
import math

CYAN = (0, 238, 238)

class WeatherSystem:
    def __init__(self):
        self.wind_angle = random.randint(0, 359)
        self.wind_speed = random.uniform(0.1, 0.4)

    def update_wind(self):
        self.wind_angle = random.randint(0, 359)
        self.wind_speed = random.uniform(0.15, 0.5)

    def draw_wind_indicator(self, surface, x, y, font):
        # Pusula arka planı
        pygame.draw.circle(surface, (20, 35, 60), (x, y), 30, 0)
        pygame.draw.circle(surface, CYAN, (x, y), 30, 1)
        
        # Rüzgar oku çizimi
        rad = math.radians(self.wind_angle)
        arrow_end_x = x + 23 * math.cos(rad)
        arrow_end_y = y + 23 * math.sin(rad)
        pygame.draw.line(surface, CYAN, (x, y), (arrow_end_x, arrow_end_y), 2)
        pygame.draw.circle(surface, CYAN, (int(arrow_end_x), int(arrow_end_y)), 3)
        
        # Yazı göstergeleri
        title_lbl = font.render("WIND", True, CYAN)
        info_lbl = font.render(f"{int(self.wind_speed * 10)} KTS", True, CYAN)
        surface.blit(title_lbl, (x - 15, y + 33))
        surface.blit(info_lbl, (x - 18, y + 48))