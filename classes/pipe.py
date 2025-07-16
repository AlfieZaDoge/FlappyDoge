import pygame, random
from .settings import H, GROUND, GAP, PW

class Pipe:
    def __init__(self, x):
        self.x = x
        self.bh = random.randint(80, H - GROUND - GAP - 80)
        self.th = H - GROUND - GAP - self.bh
        self.passed = False

    def update(self):
        self.x -= 2

    def draw(self, surf, img):
        top = pygame.transform.scale(pygame.transform.flip(img, False, True), (PW, self.th))
        bottom = pygame.transform.scale(img, (PW, self.bh))
        surf.blit(top, (self.x, 0))
        surf.blit(bottom, (self.x, self.th + GAP))

    def rects(self):
        pad = 15
        return (
            pygame.Rect(self.x + pad, 0, PW - 2 * pad, self.th),
            pygame.Rect(self.x + pad, self.th + GAP, PW - 2 * pad, self.bh)
        )
