import pygame
from .settings import W, H, GW, GH

def draw_grass(surf, grass_img, scroll):
    y = H - GH
    pygame.draw.rect(surf, (70, 200, 100), (0, y, W, GH))
    for i in range(W // GW + 2):
        surf.blit(grass_img, (i * GW - (scroll % GW), y))
