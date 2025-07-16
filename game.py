import pygame, random, sys
pygame.init()

W, H = 400, 600
FPS, GRAV, FLAP, MAX_FALL = 60, 0.25, -4, 10
GAP, PW, SPACING, SPEED = 130, 100, 450, 2
GROUND, GW, GH = 100, 80, 135
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Doge")
clock = pygame.time.Clock()

try: font = pygame.font.Font("PressStart2P.ttf", 32)
except: font = pygame.font.SysFont("Courier", 32)

bird_img = pygame.transform.scale(pygame.image.load("./Images/Doge.png").convert_alpha(), (40, 40))
grass_img = pygame.transform.scale(pygame.image.load("./Images/grass.png").convert_alpha(), (GW, GH))
pipe_img = pygame.image.load("./Images/pipe.png").convert_alpha()

class Bird:
    def __init__(s): s.x, s.y, s.vel, s.ang, s.dead = 100, H//2, 0, 0, False
    def flap(s): 
        if not s.dead: s.vel, s.ang = FLAP, -30
    def update(s): 
        s.vel = min(s.vel + GRAV, MAX_FALL)
        s.y += s.vel
        s.ang = max(min(s.ang + (3 if s.vel > 0 else -6), 90), -30)
    def draw(s, surf): 
        r = pygame.transform.rotate(bird_img, -s.ang)
        surf.blit(r, r.get_rect(center=(s.x, s.y)).topleft)
    def get_rect(s): return pygame.Rect(s.x - 15, s.y - 15, 30, 30)

class Pipe:
    def __init__(s, x):
        s.x = x
        s.bh = random.randint(50, H - GROUND - GAP - 50)
        s.th = H - GROUND - GAP - s.bh
        s.passed = False
    def update(s): s.x -= SPEED
    def draw(s, surf):
        t = pygame.transform.flip(pygame.transform.scale(pipe_img, (PW, s.th)), False, True)
        b = pygame.transform.scale(pipe_img, (PW, s.bh))
        surf.blit(t, (s.x, 0))
        surf.blit(b, (s.x, s.th + GAP))
    def rects(s):
        return pygame.Rect(s.x, 0, PW, s.th), pygame.Rect(s.x, s.th + GAP, PW, s.bh)

def draw_grass(surf, off):
    y = H - GH
    for i in range(W // GW + 2):
        x = (i * GW) - (off % GW)
        surf.blit(grass_img, (x, y))

def loop():
    bird, pipes = Bird(), [Pipe(W + i * SPACING) for i in range(3)]
    score, scroll, over = 0, 0, False

    while True:
        clock.tick(FPS)
        screen.fill((135, 206, 250))

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if (e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE) or e.type == pygame.MOUSEBUTTONDOWN:
                if over: return
                bird.flap()

        if not over: bird.update(); scroll += SPEED

        if bird.y + 20 >= H - GH:
            bird.y = H - GH - 20
            bird.dead = True
            over = True

        r = bird.get_rect()
        for p in pipes:
            p.update(); p.draw(screen)
            if not p.passed and p.x + PW < bird.x and not over:
                p.passed = True; score += 1
            t, b = p.rects()
            if r.colliderect(t) or r.colliderect(b): over, bird.dead = True, True

        if pipes[0].x + PW < 0:
            pipes.pop(0)
            pipes.append(Pipe(pipes[-1].x + SPACING))

        if bird.y - 20 < 0: bird.y, bird.vel = 0, 0

        draw_grass(screen, scroll)
        bird.draw(screen)
        s_txt = font.render(str(score), 1, (255,255,255))
        screen.blit(s_txt, (W//2 - s_txt.get_width()//2, 20))
        if over:
            m = font.render("Game Over", 1, (0,0,0))
            screen.blit(m, (W//2 - m.get_width()//2, H//2 - 30))
        pygame.display.update()

while True: loop()
