import pygame, random, sys, os
pygame.init()

W, H = 400, 600
FPS, GRAV, FLAP, MAX_FALL = 60, 0.25, -4, 10
GAP, PW, SPACING, SPEED = 130, 100, 450, 2
GROUND, GW, GH = 100, 80, 135

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Doge")
clock = pygame.time.Clock()
font = pygame.font.Font("PressStart2P.ttf", 32) if os.path.exists("PressStart2P.ttf") else pygame.font.SysFont("Courier", 32)

def load_img(name, size=None, flip=False):
    img = pygame.image.load(os.path.join("Images", name)).convert_alpha()
    if size: img = pygame.transform.scale(img, size)
    return pygame.transform.flip(img, False, True) if flip else img

bird_img = load_img("Doge.png", (40, 40))
grass_img = load_img("grass.png", (GW, GH))
pipe_img = load_img("pipe.png")

class Bird:
    def __init__(s): s.x, s.y, s.vel, s.ang, s.dead = 100, H//2, 0, 0, False
    def flap(s): s.vel, s.ang = (FLAP, -30) if not s.dead else (s.vel, s.ang)
    def update(s):
        s.vel = min(s.vel + GRAV, MAX_FALL)
        s.y += s.vel
        s.ang = max(min(s.ang + (3 if s.vel > 0 else -6), 90), -30)
    def draw(s, surf):
        r = pygame.transform.rotate(bird_img, -s.ang)
        surf.blit(r, r.get_rect(center=(s.x, s.y)).topleft)
    def rect(s): return pygame.Rect(s.x - 15, s.y - 15, 30, 30)

class Pipe:
    def __init__(s, x):
        s.x = x
        s.bh = random.randint(50, H - GROUND - GAP - 50)
        s.th = H - GROUND - GAP - s.bh
        s.passed = False
    def update(s): s.x -= SPEED
    def draw(s, surf):
        t = pygame.transform.scale(pipe_img, (PW, s.th))
        b = pygame.transform.scale(pipe_img, (PW, s.bh))
        surf.blit(pygame.transform.flip(t, False, True), (s.x, 0))
        surf.blit(b, (s.x, s.th + GAP))
    def rects(s):
        pad_x = 25  # smaller horizontal hitbox for forgiving sides
        pad_y = 5   # taller vertical hitbox for harder top/bottom collision
        top_rect = pygame.Rect(s.x + pad_x, 0, PW - 2 * pad_x, s.th - pad_y)
        bot_rect = pygame.Rect(s.x + pad_x, s.th + GAP + pad_y, PW - 2 * pad_x, s.bh - pad_y)
        return top_rect, bot_rect

def draw_grass(surf, off):
    for i in range(W // GW + 2):
        surf.blit(grass_img, (i * GW - off % GW, H - GH))

def loop():
    bird, pipes = Bird(), [Pipe(W + i * SPACING) for i in range(3)]
    score, scroll, over = 0, 0, False
    can_flap = True

    while True:
        clock.tick(FPS)
        screen.fill((135, 206, 250))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and can_flap:
                    if over:
                        return
                    bird.flap()
                    can_flap = False
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_SPACE:
                    can_flap = True
            if e.type == pygame.MOUSEBUTTONDOWN:
                if over:
                    return
                bird.flap()

        if not over:
            bird.update()
            scroll += SPEED

        if bird.y + 20 >= H - GH or bird.y <= 0:  # die if hits ground or top
            bird.y = min(max(bird.y, 0), H - GH - 20)
            bird.dead, over = True, True

        r = bird.rect()
        for p in pipes:
            p.update()
            p.draw(screen)
            if not p.passed and p.x + PW < bird.x and not over:
                p.passed, score = True, score + 1
            if r.colliderect(p.rects()[0]) or r.colliderect(p.rects()[1]):
                bird.dead, over = True, True

        if pipes[0].x + PW < 0:
            pipes.pop(0)
            pipes.append(Pipe(pipes[-1].x + SPACING))

        draw_grass(screen, scroll)
        bird.draw(screen)
        screen.blit(font.render(str(score), 1, (255, 255, 255)), (W // 2 - 20, 20))
        if over:
            m = font.render("Game Over - Click/Space", 1, (0, 0, 0))
            screen.blit(m, (W // 2 - m.get_width() // 2, H // 2 - 30))

        pygame.display.update()

while True:
    loop()
