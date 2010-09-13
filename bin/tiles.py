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

from helpers       import Sheet


TREES = Sheet("./data/image/environment/environment.PNG")
TILES = Sheet("./data/image/environment/tiles.PNG")

class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, image, size="small"):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.size = size
   
    def update(self):
        pass

def tiles_dictionary():

    dictionary = {}
    dictionary["x"] = TILES.get_at((33, 66, 32, 32), False)
    dictionary["0"] = TILES.get_at((0, 33, 32, 32), False)
    dictionary["1"] = TILES.get_at((33, 0, 32, 32), False)
    dictionary["2"] = TILES.get_at((0, 0, 32, 32), False)
    dictionary["3"] = TILES.get_at((0, 66, 32, 32), False)
    dictionary["4"] = TILES.get_at((66, 66, 32, 32), False)
    dictionary["5"] = TILES.get_at((66, 0, 32, 32), False)
    dictionary["+"] = TILES.get_at((33, 33, 32, 32), False)
    dictionary["P"] = TREES.get_at((47, 0, 31, 56), True)
    dictionary["S"] = TREES.get_at((78, 0, 14, 22), True)
    dictionary["s"] = TREES.get_at((79, 24, 14, 22), True)
    dictionary["R"] = TREES.get_at((93, 0, 16, 12), True)
    dictionary["r"] = TREES.get_at((130, 19, 18, 13), True)
    dictionary["F"] = TILES.get_at((66, 33, 32, 32), False)
    path_tiles = ["0", "1", "2", "3", "4", "5", "+"]
    return (dictionary, path_tiles)
