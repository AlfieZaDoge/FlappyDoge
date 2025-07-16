import pygame
import random
from classes.settings import PW, GAP, H, GH

class Pipe:
    def __init__(self, x):
        self.x = x
        self.bh = random.randint(80, H - GH - GAP - 80)
        self.th = H - GH - GAP - self.bh
        self.passed = False

    def update(self):
        self.x -= 2

    def draw(self, surf, pipe_img, show_hitbox=False):
        top_pipe = pygame.transform.flip(
            pygame.transform.scale(pipe_img, (PW, self.th)),
            False, True
        )
        bottom_pipe = pygame.transform.scale(pipe_img, (PW, self.bh))

        surf.blit(top_pipe, (self.x, 0))
        surf.blit(bottom_pipe, (self.x, self.th + GAP))

        if show_hitbox:
            for r in self.rects():
                hitbox = r.inflate(-40, -20)
                pygame.draw.rect(surf, (255, 0, 0), hitbox, 2)

    def rects(self):
        top_rect = pygame.Rect(self.x, 0, PW, self.th).inflate(-40, -20)
        bottom_rect = pygame.Rect(self.x, self.th + GAP, PW, self.bh).inflate(-40, -20)
        return top_rect, bottom_rect
