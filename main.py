import pygame 
import os
pygame.font.init()
pygame.mixer.init()

width, height = 900, 500
window = pygame.display.set_mode((width, height))

fps = 60
vel = 5
bullet_vel = 7

red_bullets = []
yellow_bullets = []
yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2
health_font = pygame.font.SysFont('comicsans', 40)
winner_font = pygame.font.SysFont('comicsans', 100)

spaceship_width = 55
spaceship_height = 40
border = pygame.Rect(width//2 -5, 0, 10, height)

bullet_hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
bullet_fire_sound = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

yellow_spaceship = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
yellow_spaceship = pygame.transform.rotate(
    pygame.transform.scale(yellow_spaceship, (spaceship_width,spaceship_height)), 90)

red_spaceship = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
red_spaceship = pygame.transform.rotate(
    pygame.transform.scale(red_spaceship, (spaceship_width,spaceship_height)), 270)

space = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')), (width, height))

def draw_winner(winner_text):
    draw_text = winner_font.render(winner_text, 1, (255, 255, 255))
    window.blit(draw_text, (width//2 - draw_text.get_width()//2, height//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

def draw_window(red, yellow, red_bullets, yellow_bullets, yellow_health, red_health):
    #window.fill((135,206,250))
    window.blit(space, (0,0))
    pygame.draw.rect(window, (0,0,0), border)
    
    yellow_health_text = health_font.render('HEALTH: ' + str(yellow_health), 1, (255, 255, 255))
    red_health_text = health_font.render('HEALTH: ' + str(red_health), 1, (255, 255, 255))
    
    window.blit(red_health_text, (width-red_health_text.get_width() - 10, 10))
    window.blit(yellow_health_text, (10, 10))

    window.blit(yellow_spaceship, (yellow.x, yellow.y))
    window.blit(red_spaceship, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(window, (255,0,0), bullet)
        
    for bullet in yellow_bullets:
        pygame.draw.rect(window, (255,255,0), bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    
    if keys_pressed[pygame.K_a] and yellow.x >= 10:
        yellow.x -= vel
    if keys_pressed[pygame.K_d] and yellow.x <= border.x-150:
        yellow.x += vel
    if keys_pressed[pygame.K_w] and yellow.y >= 10:    
        yellow.y -= vel
    if keys_pressed[pygame.K_s] and yellow.y <= 435:    
        yellow.y += vel   

def red_handle_movement(keys_pressed, red):
    
    if keys_pressed[pygame.K_LEFT] and red.x >= border.x+110:
        red.x -= vel
    if keys_pressed[pygame.K_RIGHT] and red.x <= 850:
        red.x += vel
    if keys_pressed[pygame.K_UP] and red.y >= 10:    
        red.y -= vel
    if keys_pressed[pygame.K_DOWN] and red.y <= 435:    
            red.y += vel

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        if bullet.x > width:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        if bullet.x < 0:
            red_bullets.remove(bullet)

def main():
    
    yellow = pygame.Rect(100, 300, spaceship_width, spaceship_height)
    red = pygame.Rect(700, 300, spaceship_width, spaceship_height)    

    clock = pygame.time.Clock()

    red_health = 10
    yellow_health = 10

    winner_text = ''
    

    run = True
    while run:

        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < 5: 
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    bullet_fire_sound.play()
                    
                if event.key == pygame.K_RCTRL and len(red_bullets) < 5: 
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()

            if event.type == yellow_hit:
                yellow_health -= 1
                bullet_hit_sound.play()
            
            if event.type == red_hit:
                red_health -= 1
                bullet_hit_sound.play()
        
        if red_health == 0:
            winner_text = 'Yellow wins'
        
        if yellow_health == 0:
            winner_text = 'Red wins'

        if winner_text:
            draw_winner(winner_text)
            break


        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red) 

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, yellow_health, red_health)


if __name__ == '__main__':
    main()