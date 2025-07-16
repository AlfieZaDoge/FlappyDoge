import pygame, sys, os
from classes.bird import Bird
from classes.pipe import Pipe
from classes.utils import draw_grass
from classes.settings import *

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Doge")

font = pygame.font.Font("PressStart2P.ttf", 32) if os.path.exists("PressStart2P.ttf") else pygame.font.SysFont("Courier", 32)
bird_img = pygame.transform.scale(pygame.image.load("./Images/Doge.png").convert_alpha(), (40, 40))
grass_img = pygame.transform.scale(pygame.image.load("./Images/grass.png").convert_alpha(), (GW, GH))
pipe_img = pygame.image.load("./Images/pipe.png").convert_alpha()

def loop():
    bird = Bird()
    pipes = [Pipe(W + i * SPACING) for i in range(3)]
    score, scroll, over, can_flap = 0, 0, False, True

    while True:
        clock.tick(FPS)
        screen.fill((135, 206, 250))

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and can_flap:
                if over: return
                bird.flap(); can_flap = False
            if e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
                can_flap = True
            if e.type == pygame.MOUSEBUTTONDOWN:
                if over: return
                bird.flap()

        if not over:
            bird.update()
            scroll += SPEED

        if bird.y + 20 >= H - GH or bird.y <= 0:
            bird.y = min(max(bird.y, 0), H - GH - 20)
            bird.dead = True
            over = True

        r = bird.rect()
        for p in pipes:
            p.update(); p.draw(screen, pipe_img)
            if not p.passed and p.x + PW < bird.x and not over:
                p.passed = True; score += 1
            if r.colliderect(p.rects()[0]) or r.colliderect(p.rects()[1]):
                bird.dead = True; over = True

        if pipes[0].x + PW < 0:
            pipes.pop(0)
            pipes.append(Pipe(pipes[-1].x + SPACING))

        draw_grass(screen, grass_img, scroll)
        bird.draw(screen, bird_img)

        screen.blit(font.render(str(score), 1, (255, 255, 255)), (W // 2 - 20, 20))
        if over:
            m = font.render("Game Over - Click/Space", 1, (0, 0, 0))
            screen.blit(m, (W // 2 - m.get_width() // 2, H // 2 - 30))

        pygame.display.update()

while True:
    loop()
