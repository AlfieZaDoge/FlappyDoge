import pygame, sys
from classes.bird import Bird
from classes.pipe import Pipe
from classes.utils import draw_grass
from classes.settings import *
from classes.pause import Pause

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Doge")
clock = pygame.time.Clock()

try:
    font = pygame.font.Font("./gui/fonts/pixel.ttf", 32)
except:
    font = pygame.font.SysFont("Courier", 32)

bird_img = pygame.transform.scale(pygame.image.load("Images/Doge.png").convert_alpha(), (76.5, 40))
grass_img = pygame.transform.scale(pygame.image.load("Images/grass.png").convert_alpha(), (GW, GH))
pipe_img = pygame.image.load("Images/pipe.png").convert_alpha()
sky_img = pygame.transform.scale(pygame.image.load("Images/sky.png").convert(), (W, H - GH))

def loop():
    bird = Bird()
    pipes = [Pipe(W + i * SPACING) for i in range(3)]
    pause = Pause()
    score, scroll, over, can_flap, show_hitboxes = 0, 0, False, True, False

    while True:
        clock.tick(FPS)
        screen.blit(sky_img, (0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and can_flap and not pause.active:
                    if over:
                        return
                    bird.flap()
                    can_flap = False
                elif e.key == pygame.K_EQUALS:
                    show_hitboxes = not show_hitboxes
                elif e.key == pygame.K_MINUS:
                    pause.toggle()
            if e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
                can_flap = True
            if pause.active:
                pause.handle_event(e)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if over:
                    return
                bird.flap()

        if not over and not pause.active:
            bird.update()
            scroll += SPEED

        if bird.y + 25 >= H - GH or bird.y - 25 <= 0:
            bird.y = min(max(bird.y, 25), H - GH - 25)
            bird.dead = True
            over = True

        r = bird.rect()
        for p in pipes:
            if not over and not pause.active:
                p.update()
            p.draw(screen, pipe_img, show_hitboxes)

            if not p.passed and p.x + PW < bird.x and not over:
                p.passed = True
                score += 1
            if r.colliderect(p.rects()[0]) or r.colliderect(p.rects()[1]):
                bird.dead = True
                over = True

        if pipes[0].x + PW < 0:
            pipes.pop(0)
            pipes.append(Pipe(pipes[-1].x + SPACING))

        draw_grass(screen, grass_img, scroll)
        bird.draw(screen, bird_img)
        score_txt = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_txt, (W // 2 - score_txt.get_width() // 2, 20))

        if pause.active:
            pause.draw(screen)

        pygame.display.update()

while True:
    loop()
