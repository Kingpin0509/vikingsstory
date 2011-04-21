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
import random

from helpers       import Sheet
from particles     import *


TOWERS = Sheet("./data/image/objects/towers.png")
ARROWS = Sheet("./data/image/objects/arrows.png")

class Tower(pygame.sprite.Sprite):

    def __init__(self, creep_id, pos, range, screen, bullet_group, creeps, \
                 tiles, banned_tiles, player, particle_emitter):
        pygame.sprite.Sprite.__init__(self)
        self.id = creep_id
        self.pos = pos
        self.range = range
        self.screen = screen
        self.bullet_group = bullet_group        
        self.creeps = creeps
        self.player = player
        self.alive = True
        self.available_creeps = []
        self.damage = 1
        self.delay = 10
        self.health = 10
        self.image = pygame.surface.Surface((64,64))
        self.needed = tiles[0]
        self.others = tiles[1]
        self.banned = banned_tiles
        self.particle_emitter = particle_emitter
        self.placed = False
        self.price_gold = 20
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.shooting_timer = 0
        self.arrow = ARROWS.get_at((0, 0, 16, 5), False)
        self.enchanted = False

    def shoot(self, object):
        """
        When the delay time has passed, shoot the
        given object
        """
        if self.shooting_timer == self.delay:
            temp = Bullet(self.rect.center, 6, object.rect.center, \
                          self.creeps, self.arrow, self.damage)
            self.bullet_group.add(temp)
            self.shooting_timer = 0
        else:
            self.shooting_timer += 1

    def search(self):
        """
        Search for a creep, or shoot the existing target
        """
        # If no creep is locked, search for one and add it
        if not len(self.available_creeps) > 0:
            for i in self.creeps:
                distance_x = self.rect.centerx-i.rect.centerx
                distance_y = self.rect.centery-i.rect.centery
                distance = math.sqrt(math.pow(distance_x, 2)+ \
                                     math.pow(distance_y, 2))
                if distance < self.range:
                    self.target = 1                    
                    self.available_creeps.append(i)
                    return
        else:
            # If the creep is locked and alive, shoot!
            for i in self.available_creeps:
                distance_x = self.rect.centerx-i.rect.centerx
                distance_y = self.rect.centery-i.rect.centery
                distance = math.sqrt(math.pow(distance_x, 2)+ \
                                     math.pow(distance_y, 2))
                if i.alive == False:
                    try:
                        self.available_creeps.remove(i)
                    except:
                        print "Something strange happened..."

                # When the creep gets out of the range, remove it from the list
                if distance > self.range: 
                    try:
                        self.available_creeps.remove(i)
                    except:
                        print "Another strange thing happened..."

                # If everything is fine, shoot the creep
                else:
                    self.shoot(i)

    def place(self):
        """
        Place the tower if player has enough money,
        and collision requirements are OK
        """
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        self.rect.center = pos

        # Checks all needed collisions
        col_build_tiles = pygame.sprite.spritecollide(self, self.needed, False)
        col_banned_tiles = False

        for group in self.banned:
            col = pygame.sprite.spritecollide(self, group, False)
            if not col:
                pass
            else:
                col_banned_tiles = True

        col_other_towers = pygame.sprite.spritecollide(self, self.others, False)
        col_other_towers_final = False

        for tower in col_other_towers:
            if not tower.id == self.id:
                if self.rect.centery < tower.rect.centery:
                    col_other_towers = True 

        if click[0] == 1:
            # When all requirements are valid, place the tower
            # and take gold from player
            if col_build_tiles and not col_banned_tiles and not \
               col_other_towers_final and not self.rect.y > \
               (19*32-self.image.get_height()):
                if not self.player["gold"] < self.price_gold:
                    self.placed = True   
                    self.player.buying = False
                    self.player["gold"] -= self.price_gold
                    height = self.image.get_height()
                    for i in xrange(int(self.image.get_width()/5)):
                        speed_x = self.rect.x+5*i
                        self.particle_emitter.add(  
                        Particle([speed_x, self.rect.y+height], [ \
                                 random.uniform(-0.5, 0), -1], \
                                 random.randrange(1, 3), (109, 90, 57), 6, 0.7), 
                        Particle([speed_x+4, self.rect.y+height], [ \
                                 random.uniform(0, 0.5), -1], \
                                 random.randrange(1, 3), (85, 162, 10), 6, 0.7))
                elif self.player["gold"] < self.price_gold and \
                     len(self.particle_emitter) < 1:
                    temp = Error([self.rect.x, self.rect.y-8], [0, -0.5], \
                                  12,(255,0,0), "Insufficient resources!", 25)
                    self.particle_emitter.add(temp)

            # When the tower is off the limits, if there are no existing
            # messages, warn the player
            elif len(self.particle_emitter) < 1 and col_banned_tiles or \
                     col_other_towers_final or self.rect.y > \
                 (19*32-self.image.get_height()):
                temp = Error([self.rect.x, self.rect.y-8], [0, -0.5], 12, \
                             (255, 0, 0), "Can't place the object here!", 25)
                self.particle_emitter.add(temp)
    
        # If player has clicked RMB, cancel the tower
        if click[2] == 1:
            self.player.buying = False
            self.alive = False
            self.kill()

    def update(self):
        if self.alive:
            if not self.placed:
                self.place()
            else:
                self.search()
        else:
            pass


class ArrowTower(Tower):

    def __init__(self, creep_id, pos, range, screen, bullet_group, creeps, \

                 tiles, banned_tiles, player, particle_emitter):
        Tower.__init__(self, creep_id, pos, range, screen, bullet_group, \
                       creeps, tiles, banned_tiles, player, particle_emitter)
        self.damage = 5
        self.delay = 10
        self.health = 100
        self.image = TOWERS.get_at((0, 0, 31, 54), True)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
