# Dave Russell

import numpy as np
import newton

SCREEN_H = 1024
SCREEN_V = 1024

MASS_REF = 1988500e24

MASS_SCALE = 1e8
LENGTH_SCALE = 1e9


class PlanetGFX (newton.Planet):

    def mass_to_px (self, mass):
        return np.ceil(np.log(mass * MASS_SCALE / MASS_REF))

    def coord_to_px (self, position):
        scale = lambda x: int(x/LENGTH_SCALE)
        x = scale(position[0]) + SCREEN_H//2
        y = SCREEN_V//2 - scale(position[1])
        if(x < 0 or x >= SCREEN_H):
            self.enabled = 0
        elif (y < 0 or y >= SCREEN_V):
            self.enabled = 0
        else:
            self.enabled = 1
        return (x,y)

    def get_tail_px (self):
        x = np.ceil(self.px_size * np.cos(self.velocity_pl[1] + np.pi))
        y = np.ceil(self.px_size * np.sin(self.velocity_pl[1] + np.pi))
        # note: y-axis is inverted from the remapping inside coord_to_px
        self.px_offset = ((x,-y))
        return (self.px_position[0] + x, self.px_position[1] - y)

    def save_tail_px (self):
        px = self.get_tail_px()
        self.position_queue.insert(0, px)
        self.valid_queue += 1
        if(self.pop_enable):
            self.position_queue.pop()
            self.valid_queue -= 1

    def save_coord_angle (self):
        self.coord_angle = np.arctan2(self.position_xy[1], self.position_xy[0])
        if(self.coord_angle < 0):
            self.coord_angle = self.coord_angle + 2*np.pi
        self.coord_angle = self.coord_angle * 180 / np.pi
        if(self.coord_angle_prev > 360*0.95 and self.coord_angle < 360*0.05):
            self.pop_enable = self._pop_enable
            self._pop_enable = 1
        if(self.coord_angle_prev < 360*0.05 and self.coord_angle > 360*0.95):
            self.pop_enable = self._pop_enable
            self._pop_enable = 1

    def __init__ (self, name = "planet", mass = 1, x = 0, y = 0, speed = 0, angle = 0, color = (255,255,255)):
        super().__init__(name, mass, x, y, speed, angle)
        self.px_size = self.mass_to_px(mass)
        self.px_color = color
        self.px_position = self.coord_to_px((x,y))
        self.px_previous = self.px_position
        self.reinit()

    def reinit (self):
        self.coord_angle = np.arctan2(self.position_xy[1], self.position_xy[0])
        self.coord_angle_prev = self.coord_angle
        self.position_queue = []
        self.was_enabled = self.enabled
        self.enabled = 0
        self.valid_queue = 0
        self.pop_enable = 0
        self._pop_enable = 0

    def update_gravity (self, planet):
        super().update_gravity(planet)

    def update_position (self):
        self.px_size = self.mass_to_px(self.mass)
        self.px_previous = self.px_position
        super().update_position()
        self.was_enabled = self.enabled
        self.px_position = self.coord_to_px(self.position_xy)
        self.coord_angle_prev = self.coord_angle
        self.save_coord_angle()
        if(self.enabled):
            self.save_tail_px()

class SolarGFX(newton.Solar):

    def __init__ (self):
        super().__init__()

    # dir == 1 UP, dir == 0 DOWN
    def scale_size (self, dir = 0):
        global MASS_SCALE, LENGTH_SCALE
        if(dir):
            LENGTH_SCALE *= 0.5
            MASS_SCALE *= 2.0
        else:
            LENGTH_SCALE *= 2.0
            MASS_SCALE *= 0.5
        self.reinit()

    # dir == 1 UP, dir == 0 DOWN
    def scale_time (self, dir = 0):
#        global newton.TIME_SCALE
        if(dir):
            newton.TIME_SCALE *= 2.0
        else:
            newton.TIME_SCALE /= 2.0
        self.reinit()

    def reinit (self):
        for planet in self.planets:
            planet.reinit()




