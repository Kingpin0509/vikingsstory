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


class State:

    def __init__(self,key,manager):
        """
        Basic game state
        """
	self.key = key
        self.manager = manager
	self.manager.add_state(key,self)
	self.screen = self.manager.screen
    
    def event(self,event):
	pass

    def update(self):
        pass


class StateManager:

    def __init__(self,player,screen,size,cursor):
        """
        Class for managing game states
        """
	self.player = player
	self.screen = screen
	self.size = size
        self.cursor = cursor
        self.states = {}
	self.current_state = None

    def add_state(self,key,state):
        self.states[key]=state

    def set_state(self,key):
	self.current_state = key

    def event(self,event):
	self.states[self.current_state].event(event)

    def update(self):
        self.states[self.current_state].update() 
