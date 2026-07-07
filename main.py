import pygame
import random
import sys
import math
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hava Trafik Kontrol (ATC) Simülasyonu")

BACKGROUND_COLOR = (15, 23, 42)       
AIRCRAFT_COLOR = (34, 197, 94)        
SELECTED_COLOR = (234, 179, 8)        
WARNING_COLOR = (239, 68, 68)          
RUNWAY_COLOR = (100, 116, 139)       
TEXT_COLOR = (248, 250, 252)         
RADAR_LINE_COLOR = (30, 41, 59)      

clock = pygame.time.Clock()

HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def save_highscore(new_high):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(new_high))

high_score = load_highscore()
score = 0
game_over = False

class Aircraft:
    def __init__(self):
        side = random.choice(['LEFT', 'RIGHT', 'TOP', 'BOTTOM'])
        if side == 'LEFT':
            self.x = -20
            self.y = random.randint(50, SCREEN_HEIGHT - 50)
            self.heading = random.randint(45, 135)
        elif side == 'RIGHT':
            self.x = SCREEN_WIDTH + 20
            self.y = random.randint(50, SCREEN_HEIGHT - 50)
            self.heading = random.randint(225, 315)
        elif side == 'TOP':
            self.x = random.randint(50, SCREEN_WIDTH - 50)
            self.y = -20
            self.heading = random.randint(135, 225)
        else: 
            self.x = random.randint(50, SCREEN_WIDTH - 50)
            self.y = SCREEN_HEIGHT + 20
            self.heading = random.choice([random.randint(0, 45), random.randint(315, 360)])

        self.speed = random.uniform(1.0, 1.4)           
        self.id = f"{random.choice(['TK', 'PC', 'XQ'])}{random.randint(100, 999)}" 
        self.is_selected = False  
        self.has_warning = False  

    def move(self):
        self.heading = self.heading % 360
        radian = math.radians(self.heading)
        self.x += self.speed * math.sin(radian)
        self.y -= self.speed * math.cos(radian)  

    def draw(self, surface):
        if self.has_warning:
            color = WARNING_COLOR
        elif self.is_selected:
            color = SELECTED_COLOR
        else:
            color = AIRCRAFT_COLOR
        
        if self.has_warning:
            pygame.draw.circle(surface, WARNING_COLOR, (int(self.x), int(self.y)), 30, 1)
        elif self.is_selected:
            pygame.draw.circle(surface, SELECTED_COLOR, (int(self.x), int(self.y)), 18, 1)

        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), 7)
        
        radian = math.radians(self.heading)
        end_x = self.x + math.sin(radian) * 20
        end_y = self.y - math.cos(radian) * 20
        pygame.draw.line(surface, color, (int(self.x), int(self.y)), (int(end_x), int(end_y)), 2)
        
        font = pygame.font.SysFont(None, 16)
        text_surface = font.render(f"{self.id} | HDG:{int(self.heading)}°", True, TEXT_COLOR)
        surface.blit(text_surface, (self.x + 15, self.y - 10))

    def check_click(self, mouse_pos):
        distance = math.hypot(self.x - mouse_pos[0], self.y - mouse_pos[1])
        return distance < 15

def reset_game():
    global score, game_over, selected_aircraft, active_aircrafts
    score = 0
    game_over = False
    selected_aircraft = None
    active_aircrafts = [Aircraft(), Aircraft()]

active_aircrafts = [Aircraft(), Aircraft()]
selected_aircraft = None  

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 4000) 

running = True
while running:
    keys = pygame.key.get_pressed()
    if selected_aircraft and not game_over:
        if keys[pygame.K_LEFT]:     
            selected_aircraft.heading -= 1.5
        if keys[pygame.K_RIGHT]:    
            selected_aircraft.heading += 1.5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == SPAWN_EVENT and not game_over:
            active_aircrafts.append(Aircraft()) 

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                if selected_aircraft:
                    selected_aircraft.is_selected = False
                    selected_aircraft = None
                for aircraft in active_aircrafts:
                    if aircraft.check_click(mouse_pos):
                        aircraft.is_selected = True
                        selected_aircraft = aircraft
                        break

        elif event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset_game()

    if not game_over:
        for i in range(len(active_aircrafts)):
            active_aircrafts[i].has_warning = False 

        for i in range(len(active_aircrafts)):
            for j in range(i + 1, len(active_aircrafts)):
                u1 = active_aircrafts[i]
                u2 = active_aircrafts[j]
                mesafe = math.hypot(u1.x - u2.x, u1.y - u2.y)
                
                if mesafe < 12:  
                    game_over = True
                    if score > high_score:
                        high_score = score
                        save_highscore(high_score)
                elif mesafe < 45: 
                    u1.has_warning = True
                    u2.has_warning = True

        pist_x = SCREEN_WIDTH // 2
        pist_y = SCREEN_HEIGHT // 2
        silinecekler = []

        for aircraft in active_aircrafts:
            aircraft.move()
            
            piste_mesafe = math.hypot(aircraft.x - pist_x, aircraft.y - pist_y)
            if piste_mesafe < 40:
                if (75 < aircraft.heading < 105) or (255 < aircraft.heading < 285):
                    score += 1
                    silinecekler.append(aircraft)
                    if aircraft == selected_aircraft:
                        selected_aircraft = None

        for ucar in silinecekler:
            if ucar in active_aircrafts:
                active_aircrafts.remove(ucar)

    screen.fill(BACKGROUND_COLOR)
    
    pygame.draw.circle(screen, RADAR_LINE_COLOR, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 250, 1)
    pygame.draw.circle(screen, RADAR_LINE_COLOR, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 150, 1)

    runway_rect = pygame.Rect(SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 - 10, 120, 20)
    pygame.draw.rect(screen, RUNWAY_COLOR, runway_rect)
    pygame.draw.line(screen, TEXT_COLOR, (SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2), (SCREEN_WIDTH//2 + 60, SCREEN_HEIGHT//2), 1)

    for aircraft in active_aircrafts:
        aircraft.draw(screen)

    font = pygame.font.SysFont(None, 24)
    skor_yazisi = font.render(f"GÜVENLİ İNİŞ: {score}", True, SELECTED_COLOR)
    rekor_yazisi = font.render(f"REKOR: {high_score}", True, TEXT_COLOR)
    screen.blit(skor_yazisi, (20, 20))
    screen.blit(rekor_yazisi, (20, 45))

    if game_over:
        font_go = pygame.font.SysFont(None, 64)
        go_yazisi = font_go.render("CRASH - GAME OVER", True, WARNING_COLOR)
        screen.blit(go_yazisi, (SCREEN_WIDTH//2 - 220, SCREEN_HEIGHT//2 - 120))
        
        font_sub = pygame.font.SysFont(None, 24)
        sub_yazisi = font_sub.render(f"Bu turda {score} uçağı indirdiniz.", True, TEXT_COLOR)
        screen.blit(sub_yazisi, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))

        font_hint = pygame.font.SysFont(None, 28)
        hint_yazisi = font_hint.render("Yeniden Başlamak İçin 'R' Tuşuna Basın", True, SELECTED_COLOR)
        screen.blit(hint_yazisi, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()