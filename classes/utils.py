import pygame
from .settings import W, H, GW, GH

def draw_grass(surf, grass_img, offset):
    y = H - GH
    for i in range(W // GW + 2):
        x = (i * GW) - (offset % GW)
        surf.blit(grass_img, (x, y))
