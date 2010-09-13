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


import os

from UserDict import UserDict
from helpers  import DictFile

class Level(UserDict):
    def __init__(self,file):
        """
        Class used to as a placeholder
        for level data
        """
        UserDict.__init__(self)
	self.level = DictFile(os.path.join("./data/levels/",file))
	temp = self.level.read()
        for k,v in temp.items():
            self[k] = v
	self.map = self.get_map(self["map"])

    def get_map(self,file):
        """
        Loads a map (which is saved as ASCII text)
        and returns a 2D array
        """
        temp = open(os.path.join("./data/levels/",file),"r")
        map = []
	data = temp.read()
	for y in data.split('\n'):
	    x = []
	    x = y.split('-')
	    map.append(x)
        temp.close()
	return map
