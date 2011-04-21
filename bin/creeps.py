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

from helpers       import Sheet


class Creep(pygame.sprite.Sprite):

    def __init__(self, creep_id, position, screen, waypoints, cursor):
        pygame.sprite.Sprite.__init__(self)
        self.id = creep_id
        self.position = position
        self.screen = screen
        self.waypoints = waypoints
        self.cursor = cursor
        self.alive = True
        self.animation_index = 0
        self.default_timer_value = 5
        self.health = 100
        self.image_set = {}
        self.image = pygame.surface.Surface((64,64))
        self.old_rotation = None
        self.rotation = None
        self.point = 0
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.speed = 1.5
        self.timer = 0

    def convert_rotation(self, angle):
        """
        Converts the given angles to sides
        of the world
        """
        east = 0
        south = -90
        west = -180
        north = 180

        if angle < north and angle < south:
            return "W"
        elif angle < east and angle > west:
            return "S"
        elif angle < 45 and angle > south:
            return "E"
        elif angle > 45 and angle <= north:
            return "N"  

    def animate(self):
        """
        When delay time has passed, the next
        frame of animation is picked
        """
        # Sets the direction of images and pick the corresponding set of images
        if self.old_rotation != self.rotation:
            self.timer = 5      
            self.animation_index = 0
            self.old_rotation = self.rotation   
            x = self.rect.x
            y = self.rect.y
            self.image = self.image_set[self.rotation][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        else:
            # If the delay time isn't on its maximum, go on
            if self.timer != self.default_timer_value:
                self.timer += 1
            else:
                # When the delay time is on its maximum, go to next image
                self.timer = 0
                # If there's more images left, continue
                if self.animation_index < len(self.image_set[self.rotation])-1:
                    self.animation_index += 1
                else:
                    self.animation_index = 0 # Reset animation   
                x = self.rect.x
                y = self.rect.y
                self.image = self.image_set[self.old_rotation][self.animation_index]
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y


    def update(self):
        if self.alive:
            # Changes the cursor image
            if self.cursor.rect.colliderect(self.rect):
                self.cursor.change_hover(self.id, True)
            else:
                self.cursor.change_hover(self.id, False)

            # When the creep's health is smaller than one, or it has passed the
            # last waypoint, kill it
            if self.health <= 0:
                self.alive = False
                self.kill()
            else:
                # Draw the creep's health bar
                red_bar = pygame.rect.Rect((self.rect.x, self.rect.y-6), \
                                           (self.image.get_width(), 5))
                red_bar.centerx = self.rect.centerx
                unit = (self.image.get_width()*self.health)/100
                green_bar = pygame.rect.Rect((red_bar.x, red_bar.y), \
                                             (unit, 5))
                border = pygame.rect.Rect((self.rect.x-1, self.rect.y-7), \
                                          (self.image.get_width()+1, 6))
                pygame.draw.rect(self.screen, (255, 0, 0), red_bar)
                pygame.draw.rect(self.screen, (0, 255, 0), green_bar)
                pygame.draw.rect(self.screen, (100, 100, 100), border, 1)

            if self.point > len(self.waypoints)-1:
                self.alive = False
                self.kill()

            distance_x = self.waypoints[self.point][0]-self.rect.x
            distance_y = self.waypoints[self.point][1]-self.rect.y

            # If the creep is at the goal and this isn't the last waypoint,
            # go to the next one
            if(abs(distance_x)+abs(distance_y)) < self.speed and not \
            self.point >= len(self.waypoints)-1:
                self.point += 1

            # Compute the angle between the creep and the waypoint
            angle = math.atan2(distance_y, distance_x)

            if self.old_rotation == None:
                self.old_rotation = self.convert_rotation(int(angle*(180/math.pi)))
                self.rotation = self.old_rotation

            # Set the rotation and move in the direction of the current waypoint
            self.rotation = self.convert_rotation(int(angle*(-180/math.pi)))
            self.rect.x += (self.speed*math.cos(angle)) + 0.1
            self.rect.y += (self.speed*math.sin(angle)) + 0.1
            self.animate()


class Wolf(Creep):

    def __init__(self, creep_id, position, screen, waypoints, cursor):
        Creep.__init__(self, creep_id, position, screen, waypoints, cursor)
        self.asset = Sheet("./data/image/creeps/wolf.PNG")
        self.image_set["N"] = [self.asset.get_at((149, 0, 17, 40), True), \
                               self.asset.get_at((149, 41, 17, 40), True)]
        self.image_set["W"] = [self.asset.get_at((17, 55, 43, 26), True), \
        self.asset.get_at((61, 55, 43, 26), True), self.asset.get_at((105,\
                                                        55, 43, 26), True)]
        self.image_set["S"] = [self.asset.get_at((0, 0, 17, 40), True), \
                               self.asset.get_at((0, 41, 17, 40), True)]
        self.image_set["E"] = [self.asset.get_at((17, 0, 43, 26), True), \
        self.asset.get_at((61, 0, 43, 26), True), self.asset.get_at((105, \
                                                        0, 43, 26), True)]
        self.image = self.image_set["S"][0]
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
