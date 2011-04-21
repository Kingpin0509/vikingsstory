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

import pygame, urllib,sys

from pygame.locals import *
from gui 	   import *
from helpers       import *
from states        import State

class Menu(State):

    def __init__(self,key,manager):
        State.__init__(self,key,manager)
        self.cursor = self.manager.cursor
        self.menu = Master([0,0],1024,768,self.screen,self.cursor,"./data/font/carolingia.ttf")
        self.menu_background = load_image("./data/image/menu/menu.PNG")
        self.temp = Label(self.menu,[273,638],(0,0,0),None,19,"v. 0.9")
        self.boxes = []
        icons = Sheet("./data/image/menu/status_icons.png")
        try:
            version = float(urllib.urlopen("http://mkm.limun.org/vs/version.txt").read())

            if version==0.9:
                self.boxes.append(MessageBox([300,300],[400,100],self.screen,self.cursor,"You have the most recent version installed.",[self.menu]))
                temp_image = icons.get_at((0,0,19,19),False)
            elif version<0.9:
		self.boxes.append(MessageBox([300,300],[400,100],self.screen,self.cursor,"Damn, you must be Chuck Norris! How did you...?",[self.menu]))
		temp_image = icons.get_at((0,0,19,19),False)
            else:
                self.boxes.append(MessageBox([300,300],[400,100],self.screen,self.cursor,"A new version is available on the official site!",[self.menu]))
                temp_image = icons.get_at((38,0,19,19),False)

        except:
            self.boxes.append(MessageBox([300,300],[400,100],self.screen,self.cursor,"Can't connect! Please check connection and restart.",[self.menu]))
            temp_image = icons.get_at((19,0,19,19),False)

        def x(something):
            print something,"x!"

        self.temp = ImageButton(self.menu,[318,638],temp_image,self.boxes[0].wake)
        self.temp = Button(self.menu,[395,155],(0,0,0),None,62,"New Game",self.manager.set_state,"game")
	self.temp = Button(self.menu,[395,222],(0,0,0),None,62,"Continue",x,"aa")
        self.temp = Button(self.menu,[395,294],(0,0,0),None,62,"Profile",x,"aa")
        self.temp = Button(self.menu,[395,366],(0,0,0),None,62,"Options",self.menu.switch,"options")
        self.temp = Button(self.menu,[395,438],(0,0,0),None,62,"Credits",self.menu.switch,"credits")
        self.temp = Button(self.menu,[395,510],(0,0,0),None,62,"Quit",exit,None)
        self.temp = Button(self.menu,[273,630],(0,0,0),None,20,"Back",self.menu.switch,"default",["credits"])
        self.temp = Button(self.menu,[273,630],(0,0,0),None,20,"Back",self.menu.switch,"default",["options"])
	self.temp = Button(self.menu,[323,630],(0,0,0),None,20,"Apply",x,"aa",["options"])
        self.temp = Textbox(self.menu, [300,155],(0,0,0),None,28,"Created by: Marko Pranjic\nPowered by: PyGame\nBackground music: Celestial Aeon Project\nSound effects: freesounds.org\nSpecial thanks to my friends\nand forumers who supported me!",3,["credits"])
        self.temp = Checkbox(self.menu,[395,154],(0,0,0),None,19,"Fullscreen",(0,1),["options"])
	self.temp = Label(self.menu,[395,179],(0,0,0),None,19,"Background sound:",["options"])
        self.temp = Scroll(self.menu, [560,179],(0,0,0),None,19,["options"])

    def update(self):
        self.screen.blit(self.menu_background,(0,0))
        self.menu.update()
        for i in self.boxes:
            i.update()
