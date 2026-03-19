#!/usr/bin/env python3

# MIT License

# Copyright (c) 2026 Louis Phoenix (ShRP69) <shrp69@proton.me>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pygame
import random
import math

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

def change_color(key):
    colors = {
        pygame.K_b: (0, 0, 255),
        pygame.K_c: (0, 255, 255),
        pygame.K_d: (110, 75, 38),
        pygame.K_e: (255, 121, 77),
        pygame.K_f: (246, 74, 138),
        pygame.K_g: (0, 255, 0),
        pygame.K_h: (223, 115, 255),
        pygame.K_r: (255, 0, 0),
        pygame.K_w: (255, 255, 255),
        pygame.K_y: (255, 255, 0),
        pygame.K_m: (255, 0, 255),
        pygame.K_o: (128, 128, 0),
        pygame.K_t: (0, 128, 128),
    }
    return colors.get(key)

current_color = (0, 255, 0)

class Star:
    def __init__(self):
        self.reset()

    def reset(self):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, WIDTH // 2)
        self.x = math.cos(angle) * radius
        self.y = math.sin(angle) * radius
        self.z = random.uniform(1, WIDTH)
        self.pz = self.z
        self.speed = random.uniform(3, 10)

    def update(self):
        self.pz = self.z
        self.z -= self.speed
        if self.z <= 1:
            self.reset()

    def draw(self, surface):
        sx = int(CENTER_X + (self.x / self.z) * WIDTH)
        sy = int(CENTER_Y + (self.y / self.z) * HEIGHT)

        px = int(CENTER_X + (self.x / self.pz) * WIDTH)
        py = int(CENTER_Y + (self.y / self.pz) * HEIGHT)

        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
            brightness = int(255 * (1 - self.z / WIDTH))
            brightness = max(100, min(255, brightness))

            color = (
                int(current_color[0] * brightness / 255),
                int(current_color[1] * brightness / 255),
                int(current_color[2] * brightness / 255),
            )

            pygame.draw.line(surface, color, (px, py), (sx, sy), 2)

stars = [Star() for _ in range(1300)]

fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.set_alpha(40)
fade_surface.fill((0, 0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            new_color = change_color(event.key)
            if new_color:
                current_color = new_color

    screen.blit(fade_surface, (0, 0))

    for star in stars:
        star.update()
        star.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
