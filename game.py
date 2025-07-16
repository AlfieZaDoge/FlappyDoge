import pygame, random, sys
from classes.settings import *
from classes.bird import Bird
from classes.pipe import Pipe
from classes.utils import draw_grass

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Doge")
clock = pygame.time.Clock()

try:
    font = pygame.font.Font("pixel.ttf", 32)  # Your pixel font file
except:
    font = pygame.font.SysFont("Courier", 32)

bird_img = pygame.transform.scale(pygame.image.load("./Images/Doge.png").convert_alpha(), (76.5, 40))
grass_img = pygame.transform.scale(pygame.image.load("./Images/grass.png").convert_alpha(), (GW, GH))
pipe_img = pygame.image.load("./Images/pipe.png").convert_alpha()

def draw_text_with_outline(surf, text, font, x, y, text_color=(255,255,255), outline_color=(0,0,0), outline_thickness=3):
    base = font.render(text, True, text_color)
    for dx in range(-outline_thickness, outline_thickness + 1):
        for dy in range(-outline_thickness, outline_thickness + 1):
            if dx == 0 and dy == 0:
                continue
            outline = font.render(text, True, outline_color)
            surf.blit(outline, (x + dx, y + dy))
    surf.blit(base, (x, y))

def loop():
    bird = Bird()
    pipes = [Pipe(W + i * SPACING) for i in range(3)]
    score = 0
    scroll = 0
    over = False
    show_hitboxes = False

    while True:
        clock.tick(FPS)
        screen.fill((135, 206, 250))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE) or e.type == pygame.MOUSEBUTTONDOWN:
                if over:
                    return
                bird.flap()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_EQUALS:  # Toggle hitboxes with '='
                    show_hitboxes = not show_hitboxes

        if not over:
            bird.update()
            scroll += SPEED

        if bird.y + 20 >= H - GH:
            bird.y = H - GH - 20
            bird.dead = True
            over = True

        r = bird.get_rect()
        for p in pipes:
            p.update()
            p.draw(screen, pipe_img, show_hitboxes)
            if not p.passed and p.x + PW < bird.x and not over:
                p.passed = True
                score += 1
            t, b = p.rects()
            if r.colliderect(t) or r.colliderect(b):
                over = True
                bird.dead = True

        if pipes[0].x + PW < 0:
            pipes.pop(0)
            pipes.append(Pipe(pipes[-1].x + SPACING))

        if bird.y - 20 < 0:
            bird.y, bird.vel = 0, 0
            over = True  # Die if touching top

        draw_grass(screen, grass_img, scroll)
        bird.draw(screen)

        score_text = str(score)
        x = W // 2 - font.size(score_text)[0] // 2
        y = 20
        draw_text_with_outline(screen, score_text, font, x, y, (255, 255, 255), (0, 0, 0), 3)

        pygame.display.update()

while True:
    loop()

