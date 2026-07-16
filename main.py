import pygame
import math
import os
from aircraft import Aircraft, SCREEN_WIDTH, SCREEN_HEIGHT
from weather import WeatherSystem
from ui import UIManager, SoundManager, RED

BG_COLOR = (10, 15, 30)

def get_high_score():
    if not os.path.exists("highscore.txt"):
        return 0
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def main():
    pygame.init()
    
    logical_size = (1000, 750)
    screen = pygame.display.set_mode(logical_size, pygame.SCALED)
    pygame.display.set_caption("Air Traffic Control Simulation V2")
    clock = pygame.time.Clock()

    import aircraft
    import ui
    aircraft.SCREEN_WIDTH = 1000
    aircraft.SCREEN_HEIGHT = 750
    ui.SCREEN_WIDTH = 1000
    ui.SCREEN_HEIGHT = 750

    ui_manager = UIManager()
    weather = WeatherSystem()
    sound = SoundManager()

    aircraft_list = [Aircraft()]
    selected_aircraft = None
    score = 0
    high_score = get_high_score()
    game_over = False
    game_over_reason = ""

    base_spawn_rate = 4000
    current_spawn_rate = base_spawn_rate
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, current_spawn_rate)

    wind_change_event = pygame.USEREVENT + 2
    pygame.time.set_timer(wind_change_event, 10000)

    is_fullscreen = False

    running = True
    while running:
        clock.tick(60)
        
        has_emergency = any(ac.fuel < 50 for ac in aircraft_list)
        if has_emergency and not game_over:
            sound.play('alarm')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == spawn_event and not game_over:
                aircraft_list.append(Aircraft())
                
            elif event.type == wind_change_event and not game_over:
                weather.update_wind()
                
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if event.button == 1:
                    mx, my = event.pos
                    clicked_any = False
                    for ac in aircraft_list:
                        dist = math.hypot(ac.x - mx, ac.y - my)
                        if dist < 15:
                            selected_aircraft = ac
                            clicked_any = True
                            sound.play('select')
                            break
                    if not clicked_any:
                        selected_aircraft = None
                        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode(logical_size, pygame.SCALED | pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode(logical_size, pygame.SCALED)
                
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    
                elif game_over and event.key == pygame.K_r:
                    aircraft_list = [Aircraft()]
                    selected_aircraft = None
                    score = 0
                    high_score = get_high_score()
                    current_spawn_rate = base_spawn_rate
                    pygame.time.set_timer(spawn_event, current_spawn_rate)
                    weather = WeatherSystem()
                    game_over = False
                    game_over_reason = ""

        if not game_over:
            keys = pygame.key.get_pressed()
            if selected_aircraft and selected_aircraft in aircraft_list:
                if keys[pygame.K_LEFT]:
                    selected_aircraft.heading = (selected_aircraft.heading - 2.5) % 360
                elif keys[pygame.K_RIGHT]:
                    selected_aircraft.heading = (selected_aircraft.heading + 2.5) % 360

            cleaned_list = []
            for ac in aircraft_list:
                ac.move(weather.wind_angle, weather.wind_speed)
                
                if ac.fuel <= 0:
                    game_over = True
                    game_over_reason = f"CRASH: {ac.id} ran out of fuel!"
                    sound.play('collision')
                    if score > high_score:
                        save_high_score(score)

                if not ac.is_out_of_bounds():
                    cleaned_list.append(ac)
                else:
                    if ac == selected_aircraft:
                        selected_aircraft = None
            
            aircraft_list = cleaned_list

            landed_aircraft = []
            for ac in aircraft_list:
                if ui_manager.runway_rect.collidepoint(ac.x, ac.y):
                    deg = ac.heading
                    if (0 <= deg <= 15) or (345 <= deg <= 360) or (165 <= deg <= 195):
                        landed_aircraft.append(ac)
                        score += 1
                        sound.play('landing')
                        
                        new_rate = max(1500, base_spawn_rate - (score * 250))
                        if new_rate != current_spawn_rate:
                            current_spawn_rate = new_rate
                            pygame.time.set_timer(spawn_event, current_spawn_rate)
                            
                        if score > high_score:
                            high_score = score
                            save_high_score(high_score)
                            
            for ac in landed_aircraft:
                if ac == selected_aircraft:
                    selected_aircraft = None
                aircraft_list.remove(ac)

        screen.fill(BG_COLOR)
        ui_manager.draw_radar_rings(screen)
        ui_manager.draw_runway(screen)

        if not game_over:
            for i in range(len(aircraft_list)):
                for j in range(i + 1, len(aircraft_list)):
                    ac1 = aircraft_list[i]
                    ac2 = aircraft_list[j]
                    dist = math.hypot(ac1.x - ac2.x, ac1.y - ac2.y)
                    
                    if dist < 45:
                        pygame.draw.circle(screen, RED, (int(ac1.x), int(ac1.y)), 30, 1)
                        pygame.draw.circle(screen, RED, (int(ac2.x), int(ac2.y)), 30, 1)
                        
                    if dist < 12:
                        game_over = True
                        game_over_reason = f"COLLISION between {ac1.id} and {ac2.id}!"
                        sound.play('collision')
                        if score > high_score:
                            save_high_score(score)

        for ac in aircraft_list:
            ac.draw(screen, ac == selected_aircraft, ui_manager.font)

        ui_manager.draw_hud(screen, score, high_score, current_spawn_rate)
        weather.draw_wind_indicator(screen, 1000 - 60, 50, ui_manager.font)

        if game_over:
            ui_manager.draw_game_over(screen, game_over_reason)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()