#!/bin/python

import pygame
import time
import random

import newton
import gfx
from gfx import PlanetGFX, SolarGFX

import numpy as np

pygame.init()
screen = pygame.display.set_mode((1024,1024), pygame.RESIZABLE)

venus = PlanetGFX (
    name  = "venus",
    mass  = 4.8675e24,
    x     = -109e9,
    y     = 0,
    speed = 35000,
    angle = -90,
    color = (255, 160, 0)
)

earth = PlanetGFX (
    name  = "earth",
    mass  = 5.9724e24,
    x     = -152e9,
    y     = 0,
    speed = 30000,
    angle = -90,
    color = (0, 255, 0)
)

mars = PlanetGFX (
    name  = "mars",
    mass  = 6.4171e23,
    x     = -249e9,
    y     = 0,
    speed = 24000,
    angle = -90,
    color = (255, 0, 0)
)

jupiter = PlanetGFX (
    name  = "jupiter",
    mass  = 1.8982e27,
    x     = -800e9,
    y     = 0,
    speed = 13000,
    angle = -90,
    color = (100, 20, 80)
)

saturn = PlanetGFX (
    name  = "saturn",
    mass  = 5.6834e26,
    x     = -1500e9,
    y     = 0,
    speed = 9680,
    angle = -90,
    color = (200, 200, 40)
)

neptune = PlanetGFX (
    name  = "neptune",
    mass  = 1.02413e26,
    x     = -4540e9,
    y     = 0,
    speed = 5400,
    angle = -90,
    color = (10, 40, 240)
)

mercury = PlanetGFX (
    name  = "mercury",
    mass  = 3.3011e23,
    x     = -69e9,
    y     = 0,
    speed = 47000,
    angle = -90,
    color = (180, 180, 180)
)

uranus = PlanetGFX (
    name  = "uranus",
    mass  = 8.681e25,
    x     = -3000e9,
    y     = 0,
    speed = 6800,
    angle = -90,
    color = (180, 240, 180)
)

sun = PlanetGFX (
    name = "sun",
    mass = 1988500e24,
    color = (255, 255, 0)
)

solar = SolarGFX()
solar.add_planet(earth)
solar.add_planet(mars)
solar.add_planet(venus)
solar.add_planet(sun)
solar.add_planet(jupiter)
solar.add_planet(saturn)
solar.add_planet(neptune)
solar.add_planet(mercury)
solar.add_planet(uranus)

def get_stars_bg (x, y):
    BG = pygame.Surface((x,y))
    for j in range(0, y):
        for i in range(0, x):
            if(random.random() > 0.999):
                BG.set_at((i,j), (240,240,240))
            else:
                BG.set_at((i,j), (0,0,0))
    return BG

def update_screen (fps):

    fps_text = font.render(f"FPS: {fps: 2.1f}", 1, (255,255,255))
    time_text = font.render(f"TIME_SCALE: {newton.TIME_SCALE} sec", 1, (255,255,255))
    distance_text = font.render(f"DISTANCE_SCALE: {gfx.LENGTH_SCALE/1e9} Gm", 1, (255,255,255))
    screen.blit(bg, (0,0))
    screen.blit(fps_text, (0,0))
    screen.blit(time_text, (0,16))
    screen.blit(distance_text, (0,32))

    solar.update()

    for planet in solar.planets:

        if(planet.enabled or planet.was_enabled):
            pygame.draw.circle(screen, (0,0,0), planet.px_previous, planet.px_size)
        if(planet.enabled):
            pygame.draw.circle(screen, planet.px_color, planet.px_position, planet.px_size)
            for i in range(1, planet.valid_queue):
                pygame.draw.line(screen, planet.px_color, planet.position_queue[i], planet.position_queue[i-1])

    pygame.display.flip()


alive = True
clk = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)
bg = get_stars_bg(1024,1024)

while alive:
    clk.tick(60)
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            alive = False
        if(event.type == pygame.VIDEORESIZE):
            gfx.SCREEN_H, gfx.SCREEN_V = event.size
            bg = get_stars_bg(gfx.SCREEN_H, gfx.SCREEN_V)
            solar.reinit()
        if(event.type == pygame.KEYUP):
            if(event.key == pygame.K_q):
                alive = False
            if(event.key == pygame.K_s):
                update_screen()
            if(event.key == pygame.K_DOWN):
                solar.scale_size(0)
                bg = get_stars_bg(gfx.SCREEN_H, gfx.SCREEN_V)
                update_screen(fps)
            if(event.key == pygame.K_UP):
                solar.scale_size(1)
                bg = get_stars_bg(gfx.SCREEN_H, gfx.SCREEN_V)
                update_screen(fps)
                pygame.display.flip()
            if(event.key == pygame.K_LEFT):
                solar.scale_time(0)
            if(event.key == pygame.K_RIGHT):
                solar.scale_time(1)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        fps = clk.get_fps()
        update_screen(fps)
