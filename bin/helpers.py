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
import re
import types

from pygame.locals import RLEACCEL, SRCALPHA


def load_image(img, transparency=True, rect=False):
    image = pygame.image.load(img)
    # Picks the transparent color for the image
    if transparency:
       colkey = image.get_at((0, 0))
       image.set_colorkey(colkey)
    if rect:
        rect = image.get_rect()
        return image, rect
    else:
        return image

class Sheet:

    def __init__(self, name):
        """
        Class for loading sprite sheets
        """
        self.sheet = load_image(name)

    def get_at(self, rect, color_key=True):
        """
        Cuts the wanted part of image
        and returns it
        """
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size, SRCALPHA)
        image.blit(self.sheet, (0, 0), rect, 0)

        if color_key:
            color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, RLEACCEL)

        return image


class DictFile:

    def __init__(self, name, dictionary=None):
        """
        Class for saving dictionaries as files and
        exporting dictionaries from those files
        """
        self.file = name
        self.dict = dictionary

    def change(self,  new_dict):
        """
        Set the new dictionary value
        """
        self.dict = new_dict

    def read(self):
        """
        Tries to load a file and extract the
        dictionary from it
        """
        
        try:
            temp_file = open(self.file, "r")
            text = temp_file.read()
            temp_file.close()
            temp_dict = {}
            lines = text.split("\n")
            lines.remove("")        # Some text editors will put this at end of the file
            for line in lines:
                result = line.split(":")
                key = result[0]
                value = result[1]
                variable = self.recognize(value)
                temp_dict[key] = variable
            return temp_dict
        except SystemError:
            print "An error happened while trying to read the file:"
            return SystemError

    def recognize(self, value):
        """
        Recognizes a value as an variable
        and removes marker from it
        """
        temp = None

        if re.search("^i>", value):
            temp = value.replace("i>", "")
            temp = int(temp)

        if re.search("^f>", value):
            temp = value.replace("f>", "")
            temp = float(temp)

        if re.search("^b>", value):
            temp = value.replace("b>", "")
            if temp == "True":
                temp = True
            elif temp == "False":
                temp = False

        if re.search("^s>", value):
            temp = value.replace("s>", "")
        
        if re.search("^l>", value):
            temp = []
            value = re.sub("^l>", "", value)
            value = re.sub("^\[", "", value)
            value = re.sub("]\Z", "", value)
            if re.search("\],", value):
                value = re.sub("],", "];", value)
                value = value.split(";")
            else:
                value = value.split(",")

            for i in value:
                i = self.recognize(i)
                temp.append(i)

        return temp

    def type_recogn(self, value):
        """
        Converts the variable to a string and
        puts a marker on it
        """
        if type(value) == types.StringType:
            value = "s>"+value
        elif type(value) == types.IntType:
            value = "i>"+str(value)
        elif type(value) == types.FloatType:
            value = "f>"+str(value)
        elif type(value) == types.BooleanType:
            value = "b>"+str(value)
        elif type(value) == types.ListType:
            temp_list = []
            for i in value:
                temp_list.append(self.type_recogn(i))
        return value

    def write(self):    
        """
        Saves the given dictionary as an
        ASCII text file
        """
        try:
            temp = ""
            for key, value in self.dict.items():
                value = self.type_recogn(value)
                temp += key+":"+value+"\n"
            temp_file = open(self.file, "w")
            temp_file.write(temp)
            temp_file.close()
            return True
        except:
            return None
