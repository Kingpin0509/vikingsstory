# -*- coding: utf-8 -*-

############################################################################
#                                                                          #
#   Viking's Story: an open source tower defense game                      #
#   Copyright (C) 2010  Marko Pranjic                                      #
#                                                                          #
#   This program is free software: you can redistribute it and/or modify   #
#   it under the terms of the GNU General Public License as published by   #
#   the Free Software Foundation, either version 3 of the License, or      #
#   (at your option) any later version.                                    #
#                                                                          #
#   This program is distributed in the hope that it will be useful,        #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#   GNU General Public License for more details.                           #
#                                                                          #
#   You should have received a copy of the GNU General Public License      #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                          #
############################################################################

import pygame
import math

class Particle(pygame.sprite.Sprite):

    def __init__(self, pos, speed, size=None, color=None, duration=None, gravity=0):
        pygame.sprite.Sprite.__init__(self)
        self.acclrtn_x = speed[0]
        self.acclrtn_y = speed[1]
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = gravity
        self.pops = []
        # For each duration unit create a copy
        # of the image
        for i in xrange(duration):
            image = pygame.surface.Surface((size, size)).convert()
            image.fill(color)
            self.pops.append(image)
        self.image = self.pops[0]
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.move_ip(self.velocity_x, self.velocity_y)
        self.velocity_x += self.acclrtn_x
        self.velocity_y += self.acclrtn_y
        self.acclrtn_y += self.gravity
        # If no more images are left to choose from,
        # destroy the particle
        if not self.pops:
            self.kill()
        else:
            self.image = self.pops.pop(0)

class Error(Particle):

    def __init__(self, pos, speed, size, color, message, duration):
        Particle.__init__(self, pos, speed, size, color, duration)
        self.font = pygame.font.Font("./data/font/times.ttf", size)
        self.image = self.font.render(message, True, color)
        self.pops = []
        self.alpha = 255
        for i in xrange(duration):
            self.alpha -= 50
            image = self.image.copy()
            image.set_alpha(self.alpha)
            self.image = image
            self.pops.append(image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Bullet(pygame.sprite.Sprite):

    def __init__(self, pos, speed, goal, bastards, image, damage):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.speed = speed
        self.goal = goal
        self.dir = math.atan2(self.goal[1]-pos[1], self.goal[0]-pos[0])
        self.image = pygame.transform.rotate(image, int(self.dir*(-180/math.pi)))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.damage = damage
        self.bastards = bastards
        self.alive = True

    def update(self):
        if self.alive:
            col = pygame.sprite.spritecollide(self, self.bastards, False)
            # If the bullet is off the boundaries, kill him, if he's colliding
            # with the target, remove HP from target and than kill him
            if self.rect.x > 1024 or self.rect.x < 0 or self.rect.y < 0 or \
               self.rect.y > 768 or col:
                if col:
                    for i in col:
                        i.health -= self.damage
                self.alive = False
                self.kill()
            else:
                self.rect.x += self.speed*math.cos(self.dir)
                self.rect.y += self.speed*math.sin(self.dir)
            self.speed += 0.1
