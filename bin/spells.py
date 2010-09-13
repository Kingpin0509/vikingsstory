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

from particles import Particle, Error
from helpers   import Sheet

ARROWS = Sheet("./data/image/objects/arrows.png")
SPELLS = Sheet("./data/image/objects/spell.png")

class Spell(pygame.sprite.Sprite):
    
    def __init__(self, pos, player, particle_emitter, screen, target):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.particle_emitter = particle_emitter
        self.screen = screen
        self.target = target
        self.image = pygame.surface.Surface((25,25))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.placed = False
        self.price = 0
        self.targeted = []
        self.effect_time = 30
        self.timer = self.effect_time
        self.enchanted = False

    def buff(self):
        """
        Do some magic crap.
        """
        pass
   
    def undo_buff(self):
        """
        Undo some magic crap.
        """
        pass

    def start_effect(self):
        """
        Particle fun
        """
        pass

    def hide(self):
        """
        Hides spell. It's still active,
        but it doesn't show it
        """
        self.image = pygame.surface.Surface((25, 25))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))

    def place(self):
        """
        Place the spell if player has enough magicka,
        and collision requirements are OK
        """

        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        self.rect.center = pos

        # Checks if colliding with target(s)
        col_1 = pygame.sprite.spritecollide(self, self.target, False)

        if not col_1:
            self.image = SPELLS.get_at((0, 0, 53, 20))
        else:
            self.image = SPELLS.get_at((54, 0, 53, 20))

        if click[0] == 1:
            # When all requirements are valid, place the spell
            # and take magicka from player
            if col_1:
                if not self.player["magicka"] < self.price:
                    self.placed = True   
                    self.player.buying = False
                    self.player["magicka"] -= self.price
                    for target in col_1:
                        if target.enchanted:
                            temp = Error([target.rect.x, target.rect.y-8], \
                                         [0, -0.5], (255, 0, 0), "Already enchanted", \
                                         25)
                            self.particle_emitter.add(temp)
                        else:
                            self.targeted.append(target)
                            break

                    self.start_effect()
                elif self.player["magicka"] < self.price and \
                     len(self.particle_emitter) < 1:
                    temp = Error([self.rect.x, self.rect.y-8], [0, -0.5], \
                                  12, (255, 0, 0), "Insufficient resources!", 25)
                    self.particle_emitter.add(temp)

            # When the spell is not targeted, if there are no existing
            # messages, warn the player
            elif len(self.particle_emitter) < 1 and not col_1 :
                temp = Error([self.rect.x, self.rect.y-8], [0, -0.5], 12, \
                             (255, 0, 0), "Can't find a target here!", 25)
                self.particle_emitter.add(temp)
    
        # If player has clicked RMB, cancel the spell
        if click[2] == 1:
            self.player.buying = False
            self.kill()

    def update(self):
        if not self.placed:
            self.place()
        else:
            if not self.enchanted:
                self.buff()
                self.enchanted = True
            else:
                if not self.timer == 0:
                    self.timer -= 1

                else:
                    self.timer = 0
                    self.undo_buff()

                for tower in self.targeted:
                    # Draw the creep's health bar
                    m_time = pygame.rect.Rect((tower.rect.x, tower.rect.y-6), \
                                              (tower.image.get_width(), 5))
                    m_time.centerx = tower.rect.centerx
                    unit = (tower.image.get_width()*self.timer)/ \
                            self.effect_time
                    time = pygame.rect.Rect((m_time.x, m_time.y), \
                                            (unit+1, 5))
                    pygame.draw.rect(self.screen, (171, 155, 45), m_time)
                    pygame.draw.rect(self.screen, (227, 205, 59), time)
                    pygame.draw.rect(self.screen, (104, 96, 43), m_time, 1)

class FireArrows(Spell):

    def __init__(self, pos, player, particle_emitter, screen, target):
        Spell.__init__(self, pos, player, particle_emitter, screen, target)
        self.image = SPELLS.get_at((0, 0, 53, 20))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.effect_time = 300
        self.timer = self.effect_time
        self.price = 10
        self.previous_val = []

    def buff(self):
        # Changes the values of targeted towers and saves
        # default ones
        for n in xrange(len(self.targeted)):
            tower = self.targeted[n]
            self.previous_val.append([tower.damage, tower.arrow])
            tower.damage += 5
            tower.arrow = ARROWS.get_at((17, 0, 16, 5), False)
            tower.enchanted = True
        self.hide()

    def undo_buff(self):
        # Returns values of targeted towers to default
        # ones, does harakiri
        for n in xrange(len(self.targeted)):
            tower = self.targeted[n]
            tower.damage = self.previous_val[n][0]
            tower.arrow = self.previous_val[n][1]
            tower.enchanted = False

        self.previous_val = self.targeted = []
        self.kill()

    def effect(self):
        pass
