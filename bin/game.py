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

from creeps        import *
from gui           import *
from helpers       import *
from levels        import *
from tiles         import *
from towers        import *
from spells        import FireArrows
from states        import State

class Game(State):

    def __init__(self,key,manager):
        State.__init__(self,key,manager)	
	self.bullet_group = pygame.sprite.Group()
	self.creeps = pygame.sprite.OrderedUpdates()
        self.cursor = self.manager.cursor
	self.tiles_dict, self.path_tiles = tiles_dictionary()
	self.towers = pygame.sprite.OrderedUpdates()
	self.needed_tiles = pygame.sprite.Group()
	self.banned_tiles = pygame.sprite.OrderedUpdates()
	self.banned_tiles2 = pygame.sprite.OrderedUpdates()
	self.ingame_menu = Master([0,19*32],1024,160,self.screen,self.cursor,"./data/font/viking.ttf")
	self.ingame_menu_bg = load_image("./data/image/menu/ingame_menu.png")
	self.levels = {}
	temp = Level("lv01.mkm")
	self.levels[temp["name"]]=temp
	self.player = self.manager.player
	self.gold_label = Label(self.ingame_menu,[285,10],(255,255,255),None,15,str(self.player["gold"]))
        self.magicka_label = Label(self.ingame_menu,[372,10],(255,255,255),None,15,str(self.player["magicka"]))
	self.particle_emitter = pygame.sprite.Group()
        self.spells = pygame.sprite.Group()

        def spawn():
            if not self.player.buying:
                self.player.buying = True
	        temp = (ArrowTower(len(self.towers),[0,0],80,self.screen, \
                        self.bullet_group,self.creeps,[self.needed_tiles, \
                        self.towers],[self.banned_tiles,self.banned_tiles2], \
                        self.player, self.particle_emitter))
	        self.towers.add(temp)

        def spawn2():
            if not self.player.buying:
                self.player.buying = True
                temp = FireArrows([0, 0], self.player, self.particle_emitter, \
                                  self.screen, self.towers)
                self.spells.add(temp)

        buttons = Sheet("./data/image/menu/buttons.png")       
        ImageButton(self.ingame_menu,[33,47],buttons.get_at((33,0,32,32),False),spawn)
        ImageButton(self.ingame_menu,[806,47],buttons.get_at((66,0,32,32),True),spawn2)

    def event(self,event):
        pass

    def load_level(self,level):
	level = self.levels[level]

	for i in xrange(level["quantity"]):
            x_point = level["start"][0]
	    y_point = level["start"][1]
	    enemy = level["enemies"]
	    if enemy=="wolf":
	        temp = Wolf(len(self.creeps),[x_point,y_point-100*i],self.screen,level["waypoint"],self.cursor)
	        self.creeps.add(temp)

	map = level.map
        for y in xrange(len(map)-1):
            for x in xrange(len(map[y])):
		self.needed_tiles.add(Tile([x*32,y*32],self.tiles_dict["x"]))
        for y in xrange(len(map)):
            for x in xrange(len(map[y])):
		try:
                    temp = map[y][x]
		    if not temp=="x" and not temp in self.path_tiles:
		        self.banned_tiles.add(Tile([x*32,y*32],self.tiles_dict[temp]))
                    elif not temp=="x" and temp in self.path_tiles:
                        self.banned_tiles2.add(Tile([x*32,y*32],self.tiles_dict[temp]))
		except:
		    pass

    def update(self):
	self.gold_label.change(str(self.player["gold"]))
        self.magicka_label.change(str(self.player["magicka"]))
        if len(self.needed_tiles)<=0 and len(self.banned_tiles)<=0:
            self.load_level("Tutorial")
	self.needed_tiles.update()
	self.needed_tiles.draw(self.screen)
        self.banned_tiles2.update()
        self.banned_tiles2.draw(self.screen)
        self.spells.update()
        self.spells.draw(self.screen)
	self.banned_tiles.update()
	self.banned_tiles.draw(self.screen)
	self.bullet_group.update()
	self.bullet_group.draw(self.screen)
	self.creeps.update()
	self.creeps.draw(self.screen)
	self.towers.update()
	self.towers.draw(self.screen)
        self.particle_emitter.update()
        self.particle_emitter.draw(self.screen)
	self.screen.blit(self.ingame_menu_bg,self.ingame_menu.rect)
	self.ingame_menu.update()
	
