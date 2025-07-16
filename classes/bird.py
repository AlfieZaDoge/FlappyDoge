import pygame
from .settings import H, FLAP, GRAV, MAX_FALL

class Bird:
    def __init__(self):
        self.x, self.y = 100, H // 2
        self.vel, self.ang = 0, 0
        self.dead = False

    def flap(self):
        if not self.dead:
            self.vel = FLAP
            self.ang = -30

    def update(self):
        self.vel = min(self.vel + GRAV, MAX_FALL)
        self.y += self.vel
        self.ang = max(min(self.ang + (3 if self.vel > 0 else -6), 90), -30)

    def draw(self, surf, img):
        r = pygame.transform.rotate(img, -self.ang)
        surf.blit(r, r.get_rect(center=(self.x, self.y)).topleft)

    def rect(self):
        return pygame.Rect(self.x - 15, self.y - 15, 30, 30)
    