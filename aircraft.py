import pygame
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750

class Aircraft:
    def __init__(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            self.x = random.randint(50, SCREEN_WIDTH - 50)
            self.y = -20
        elif side == 'bottom':
            self.x = random.randint(50, SCREEN_WIDTH - 50)
            self.y = SCREEN_HEIGHT + 20
        elif side == 'left':
            self.x = -20
            self.y = random.randint(50, SCREEN_HEIGHT - 50)
        else:
            self.x = SCREEN_WIDTH + 20
            self.y = random.randint(50, SCREEN_HEIGHT - 50)

        self.speed = random.uniform(1.2, 2.0)
        target_x = SCREEN_WIDTH // 2
        target_y = SCREEN_HEIGHT // 2
        angle_to_center = math.atan2(target_y - self.y, target_x - self.x)
        self.heading = math.degrees(angle_to_center) % 360

        prefix = random.choice(['TK', 'PC', 'XQ'])
        num = random.randint(100, 999)
        self.id = f"{prefix}-{num}"
        
        # ⛽ DİNAMİK VE GERÇEKÇİ BAŞLANGIÇ YAKITI
        # %30 ihtimalle uçak kritik yakıtla (60-90 arası) doğar ve hızlıca Mayday'e girer.
        # %70 ihtimalle normal depoyla (110-180 arası) doğar.
        if random.random() < 0.30:
            self.fuel = random.randint(60, 90)
        else:
            self.fuel = random.randint(110, 180)
        
        # ☄️ RADAR TRAIL (Radar Kuyruk İzi)
        self.trail = []

    def move(self, wind_angle, wind_speed):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)

        rad = math.radians(self.heading)
        dx = self.speed * math.cos(rad)
        dy = self.speed * math.sin(rad)
        
        wind_rad = math.radians(wind_angle)
        wx = wind_speed * math.cos(wind_rad)
        wy = wind_speed * math.sin(wind_rad)
        
        self.x += dx + wx
        self.y += dy + wy
        
        if self.fuel > 0:
            self.fuel -= 0.05

    def is_out_of_bounds(self):
        margin = 100
        return (self.x < -margin or self.x > SCREEN_WIDTH + margin or
                self.y < -margin or self.y > SCREEN_HEIGHT + margin)

    def draw(self, surface, is_selected, font):
        if is_selected:
            main_color = (255, 215, 0)      # Sarı
            alarm_color = (255, 215, 0)
        elif self.fuel < 50:
            main_color = (255, 50, 50) if pygame.time.get_ticks() % 500 < 250 else (255, 140, 0)
            alarm_color = (255, 50, 50)
        else:
            main_color = (0, 255, 100)     # Yeşil
            alarm_color = (0, 255, 100)

        for i, pos in enumerate(self.trail):
            ratio = (i + 1) / len(self.trail)
            trail_color = (int(main_color[0] * ratio), int(main_color[1] * ratio), int(main_color[2] * ratio))
            size = max(1, int(4 * ratio))
            pygame.draw.circle(surface, trail_color, (int(pos[0]), int(pos[1])), size)

        pygame.draw.circle(surface, main_color, (int(self.x), int(self.y)), 6)
        rad = math.radians(self.heading)
        end_x = self.x + 20 * math.cos(rad)
        end_y = self.y + 20 * math.sin(rad)
        pygame.draw.line(surface, main_color, (self.x, self.y), (end_x, end_y), 2)

        if is_selected or self.fuel < 50:
            pygame.draw.circle(surface, alarm_color, (int(self.x), int(self.y)), 18, 1)

        lbl_text = self.id
        if self.fuel < 50:
            lbl_text += " [MAYDAY]"
            
        lbl = font.render(lbl_text, True, main_color)
        surface.blit(lbl, (self.x + 10, self.y - 15))
        
        fuel_lbl = font.render(f"FUEL: {int(self.fuel)}", True, main_color)
        surface.blit(fuel_lbl, (self.x + 10, self.y))