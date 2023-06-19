# Dave Russell
# All units are SI

import numpy as np
from collections import namedtuple

def to_polar (cartesian):
    magnitude = np.sqrt(np.sum(np.square(cartesian)))
    angle = np.arctan2(cartesian[1], cartesian[0])
    return np.array([magnitude, angle])

def to_cartesian (polar):
    x = polar[0] * np.cos(polar[1])
    y = polar[0] * np.sin(polar[1])
    return np.array([x,y])

def to_radians (degrees):
    return degrees * np.pi / 180

def to_degrees (radians):
    return radians * 180 / np.pi

TIME_SCALE = 3600*24

class Planet:

    def __init__ (self, name = "planet", mass = 1, x = 0, y = 0, speed = 0, angle = 0):
        # Initialize
        self.name = name
        self.mass = mass
        self.position_xy = np.array([x, y])
        self.velocity_pl = np.array([speed, to_radians(angle % 360)])
        self.gravity_xy = np.array([0.0,0.0])

        # Constants
        self.G = 6.674e-11 # m^3 / (kg*s^2)

    def update_gravity (self, planet):
        # Calculate F = G*m1*m2/(r^2)
        distance_pl = to_polar(planet.position_xy - self.position_xy)
        radius = distance_pl[0]
        angle = distance_pl[1]
        force = self.G * self.mass * planet.mass / np.square(radius)

        self.gravity_xy += to_cartesian(np.array([force,angle]))

    def update_position (self):
        # Calculate delta_P = delta_t * ((delta_t * F/m) + velocity)
        gravity_pl = to_polar(self.gravity_xy)
        acceleration = gravity_pl[0] / self.mass

        velocity_xy = to_cartesian(self.velocity_pl)
        acceleration_xy = to_cartesian(np.array([acceleration, gravity_pl[1]]))

        motion_xy = velocity_xy + (TIME_SCALE * acceleration_xy)
        new_position_xy = self.position_xy + (TIME_SCALE * motion_xy)

        self.gravity_xy = np.array([0.0,0.0])
        self.velocity_pl = to_polar(motion_xy)
        self.position_xy = new_position_xy


class Solar():

    def __init__ (self):
        self.planets = []

    def add_planet (self, planet):
        self.planets.append(planet)

    def update (self):
        for planet in self.planets:
            for ext_planet in self.planets:
                if(planet == ext_planet):
                    continue
                else:
                    planet.update_gravity(ext_planet)
            planet.update_position()

