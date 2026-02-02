import pygame
import random
from constants import *
from circleshape import CircleShape
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            screen, 
            "white", 
            (self.position.x, self.position.y),
            self.radius,
            LINE_WIDTH
        )

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        pos = self.position
        vel = self.velocity
        old_radius = self.radius

        self.kill()

        if old_radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        angle = random.uniform(20, 50)

        v1 = vel.rotate(angle)
        v2 = vel.rotate(-angle)

        new_radius = old_radius - ASTEROID_MIN_RADIUS

        a1 = Asteroid(pos.x, pos.y, new_radius)
        a2 = Asteroid(pos.x, pos.y, new_radius)

        a1.velocity = v1 * 1.2
        a2.velocity = v2 * 1.2