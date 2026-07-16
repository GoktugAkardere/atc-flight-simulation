import random
import math
import pygame

class WeatherSystem:
    def __init__(self):
        self.wind_angle = random.randint(0, 359)
        self.wind_speed = random.uniform(0.1, 0.4)

    def update_wind(self):
        self.wind_angle = (self.wind_angle + random.randint(-30, 30)) % 360
        self.wind_speed = max(0.05, min(0.6, self.wind_speed + random.uniform(-0.05, 0.05)))

    def draw_wind_indicator(self, surface, x, y, font):
        pygame.draw.circle(surface, (30, 45, 80), (x, y), 25, 2)
        
        rad = math.radians(self.wind_angle)
        end_x = x + 20 * math.cos(rad)
        end_y = y + 20 * math.sin(rad)
        
        pygame.draw.line(surface, (100, 200, 255), (x, y), (end_x, end_y), 3)
        pygame.draw.circle(surface, (100, 200, 255), (int(end_x), int(end_y)), 4)
        
        lbl = font.render(f"WIND: {self.wind_speed * 10:.1f} KT", True, (100, 200, 255))
        surface.blit(lbl, (x - 35, y + 30))