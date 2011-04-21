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

from helpers       import Sheet

STATUS_ICONS = Sheet("./data/image/menu/status_icons.png")

class Cursor:

    def __init__(self, images, screen):
        """
        Class for custom cursor image.
        Can change its image.
        """
        self.images = images
        self.scr = screen
        self.image = self.images[0]
        self.pos = pygame.mouse.get_pos()
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.hover = False
        self.caller_id = None

    def change_hover(self, object_id, hovering):
        """
        Judging by the object's ID, changes current
        image to other one. ID is needed, so other
        objects don't kill one's request
        """
        if object_id == self.caller_id and not hovering:
            self.hover = hovering

        elif self.caller_id == None and hovering:
            self.hover = hovering
            self.caller_id = object_id

        elif hovering:
            self.hover = hovering
            self.caller_id = object_id

    def update(self):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()
        if self.hover == True:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
        self.scr.blit(self.image, self.rect)

class Master:

    def __init__(self, pos, width, height, screen, cursor, font):
        """
        Controlls and updates widgets
        """
        self.widgets = []
        self.key = None
        self.alive = 1
        self.surface = screen
        self.cursor = cursor
        self.rect = pygame.rect.Rect(0, 0, width, height)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.scr = screen
        self.font = font
        self.state = "default"
        self.top = True

    def die(self):
        """
        Kills object
        """
        self.alive = False

    def switch(self, new_state):
        """
        Switches the state of master
        """
        self.state = new_state

    def update(self):
        """
        Updates widgets if they're updateable
        in current state
        """
        if self.alive:
            for widget in self.widgets:
                if self.state in widget.states:
                    widget.update()

    def add_widget(self, widget):
        """
        Adds widgets.
        """
        self.widgets.append(widget)


class Widget:

    def __init__(self, master, pos, txt_col, bg_col, txt_size, \
                 states=["default"]):
        """
        Base class for other widgets.
        """
        self.master = master
        self.master.add_widget(self)
        self.id = id(self)
        self.cursor = self.master.cursor
        self.pos = [pos[0]+self.master.rect.x, pos[1]+self.master.rect.y]
        self.txt_col = txt_col
        self.txt_size = txt_size
        self.bg_col = bg_col
        self.surf = self.master.surface
        self.font = pygame.font.Font(self.master.font, self.txt_size)
        self.states = states

    def update(self):
        pass


class Label(Widget):

    def __init__(self, master, pos, txt_col, bg_col, txt_size, text, \
                 states=["default"]):
        """
        Blits only one line of text.
        """
        Widget.__init__(self, master, pos, txt_col, bg_col, txt_size, states) 
        self.text = text

        if self.bg_col:
            self.surf = self.font.render(self.text, True, self.txt_col, \
                                         self.bg_col)
        else:
            self.surf = self.font.render(self.text, True, self.txt_col)

        self.rect = self.surf.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def change(self, text):
        """
        Changes data of the label.
        """
        self.text = text

        if self.bg_col:
            self.surf = self.font.render(self.text, True, self.txt_col, \
                                         self.bg_col)
        else:
            self.surf = self.font.render(self.text, True, self.txt_col)

    def update(self):
        self.master.scr.blit(self.surf, self.rect)    


class Textbox(Label):

    def __init__(self, master, pos, txt_col, bg_col, txt_size, text, indent, \
                 states=["default"]):
        """
        Blits multiple lines of text,
        separated by newline.
        """
        Label.__init__(self, master, pos, txt_col, bg_col, txt_size, text, \
                       states)
        self.lines = self.text.split("\n")
        self.surfaces = []
        self.ii = indent # Space between lines

        # Makes new surface for each line
        for i in self.lines:
            tmp = self.font.render(i, True, self.txt_col)
            self.surfaces.append(tmp)

    def update(self):
        for i in range(0, len(self.lines)):
            self.master.scr.blit(self.surfaces[i], (self.pos[0], \
                                (self.pos[1]+self.txt_size*i+i*self.ii)))

    def change(self, text):
        """
        Changes text of the textbox.
        """
        self.lines = text.split("\n")
        self.surfaces = []
        for i in self.lines:
            tmp = self.font.render(i, False, self.txt_col)

            t = tmp.get_width()

            self.surfaces.append(tmp)


class Button(Label):

    def __init__(self, master, pos, txt_col, bg_col, txt_size, text, command, \
                 arguments, states=["default"], holdable=False):
        """
        Button widget - when clicked,
        it will execute the given command.
        """
        Label.__init__(self, master, pos, txt_col, bg_col, txt_size, text, \
                       states)
        self.command = command
        self.args = arguments
        self.holdable = holdable # If true, command will execute when holding 
                                 # button
        self.holding = 0
        self.alpha = 0
        self.line = pygame.surface.Surface((self.surf.get_width(), 1))
        self.line.set_alpha(self.alpha)
        self.line_rect = self.line.get_rect()
        self.line_rect.center = self.rect.center
        self.line_rect.centery += (self.surf.get_height()/2)+1

    def update(self):
        click = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        # If mouse is colliding with the button, and our master is on top,
        # change cursor image and increase alpha, if not, decrease it.
        if self.rect.collidepoint(pos) and self.master.top:
            self.cursor.change_hover(self.id, True)

            if not self.alpha >= 255:
                self.alpha += 15

            elif self.alpha > 255:
                self.alpha = 255

            # If LMB is clicked and button's holdable or the user's not
            # holding the button, execute the command (with or without 
            # arguments, it depends on given values)
            if click[0] == 1:
                if self.holdable or not self.holding>0:
                    if self.args:
                        self.command(self.args)

                    else:
                        self.command()

                    self.holding += 1

            else:
                self.holding = 0

        else:
            self.cursor.change_hover(self.id, False)

            if not self.alpha <= 0:
                self.alpha -= 15

            elif self.alpha < 0:
                self.alpha = 0    

        self.line.set_alpha(self.alpha)
        self.master.scr.blit(self.surf, self.rect)
        self.master.scr.blit(self.line, self.line_rect)

class Image:

    def __init__(self, master, pos, img, states=["default"]):
        """
        Blits an image.
        """
        self.master = master
        self.master.add_widget(self)
        self.cursor = self.master.cursor
        self.id = id(self)
        self.pos = [pos[0]+self.master.rect.x, pos[1]+self.master.rect.y]
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.states = states

    def update(self):
        temp = self.master.scr.blit(self.img, self.rect)


class ImageButton(Image):

    def __init__(self, master, pos, img, command, arguments=None, \
                 states=["default"], holdable=False):
        """
        Image, which when is clicked, will
        execute a command. For more info see Button
        class
        """
        Image.__init__(self, master, pos, img, states)
        self.command = command
        self.args = arguments
        self.holding = 0
        self.holdable = holdable

    def update(self):
        click = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.cursor.change_hover(self.id, True)

            if click[0] == 1 and self.master.top:
                if self.holdable or not self.holding>0:
                    if self.args:
                        self.command(self.args)

                    else:
                        self.command()

                    self.holding+=1

            elif not click[0] == 1:
                self.holding = 0

        else:      
            self.cursor.change_hover(self.id,  False)

        self.master.scr.blit(self.img, self.rect)

class Checkbox(Widget):

    def __init__(self, master, pos, txt_col, bg_col, txt_size, text, values, \
                 states=["default"]):
        """
        Widget for visually showing Boolean
        value. If box is clicked, and value is true,
        change it to false and vice-versa.
        """
        Widget.__init__(self, master, pos, txt_col, bg_col, txt_size, states)
        self.text = text
        self.current = self.not_checked = values[0] # Sets value to default one
        self.checked = values[1]
        self.images = [STATUS_ICONS.get_at((57, 0, 19, 19), False), \
                       STATUS_ICONS.get_at((0, 0, 19, 19), False)]
        self.button = ImageButton(master, pos, self.images[0], self.switch, \
                                  None, states)
        if self.bg_col:
            self.surf = self.font.render(self.text, True, self.txt_col, \
                                         self.bg_col)
        else:
            self.surf = self.font.render(self.text, True, self.txt_col)

        self.rect = self.surf.get_rect()
        self.rect.x = self.pos[0]+21
        self.rect.y = self.pos[1]

    def get_value(self):
        """
        Returns current value.
        """
        return self.current

    def switch(self):
        """
        Switches the current value.
        """
        if not self.current == self.checked:
            self.current = self.checked
            self.button.img = self.images[1]

        else:
            self.current = self.not_checked
            self.button.img = self.images[0]

    def update(self):
        self.master.scr.blit(self.surf, self.rect)
        self.button.update()   


class Scroll(Label):

    def __init__(self, master, pos, txt_col, bg_col, txt_size, \
                 states=["default"], minv=0, maxv=100, step=1):
        """
        Widget for changeable values.
        """
        Label.__init__(self, master, pos, txt_col, bg_col, txt_size, \
                       str(maxv), states)
        self.text = str(maxv)
        self.minv = minv
        self.maxv = maxv
        self.step = step
        self.value = maxv
        self.lower  = ImageButton(master, pos, STATUS_ICONS.get_at(( \
                                  76, 0, 19, 19), False), self.add, (-1), \
                                  states, True)
        self.higher = ImageButton(master, [pos[0]+100, pos[1]], \
                                  STATUS_ICONS.get_at((95, 0, 19, 19), False), \
                                  self.add, (1), states, True)
        self.rect.x += 19

    def add(self, value=1):
        """
        Adds value to current one.
        """
        if not self.value < self.minv and not self.value > self.maxv:
            self.value += self.step*value

            if self.value > self.maxv:
                self.value = self.maxv

            elif self.value < self.minv:
                self.value = self.minv

            self.text = str(self.value)

    def update(self):
        self.master.scr.blit(self.surf, self.rect)
        self.lower.update()
        self.higher.update()


class MessageBox:

    def __init__(self, pos, size, screen, cursor, text, other_masters, \
                 ok_function=None, arg=None):
        """
        A pop-up window with OK and
        CANCEL options.
        """
        self.pos = pos
        self.screen = screen

        self.text = text
        self.cursor = cursor
        self.size = size
        self.top = False
        if ok_function == None:
            self.ok_function = self.lazy
        else:
            self.ok_function = ok_function
        self.main = Master(self.pos, size[0], size[1], screen, self.cursor, \
                           "./data/font/carolingia.ttf")
        Label(self.main, [8, 8], (0, 0, 0), None, 18, self.text)
        Button(self.main, [(self.size[0]-(self.size[0]/2))-8, 34], \
              (0, 0, 0), None, 18, "OK", self.lazy, "")
        self.alive = False
        self.main.top = self.main.alive = False
        self.arg = arg
        self.other_masters = other_masters

    def switch(self, argument):
        for i in self.other_masters:
            i.top = argument

    def lazy(self):
        self.switch(True)
        self.alive = self.main.alive = self.top = False

        try:
            self.ok_function(self.arg)
        except:
            pass

    def wake(self):
        self.switch(False)
        self.main.top = self.main.alive = self.alive = True

    def update(self):
        if self.alive:
            pygame.draw.rect(self.screen, (46, 16, 14), (self.pos[0], \
                           self.pos[1], self.size[0], self.size[1]), 1)
            pygame.draw.rect(self.screen, (76, 23, 20), (self.pos[0]+1, \
                       self.pos[1]+1, self.size[0]-2, self.size[1]-2), 1)
            pygame.draw.rect(self.screen, (46, 16, 14), (self.pos[0]+2, \

                     self.pos[1]+2, self.size[0]-4, self.size[1]-4), 1)
            pygame.draw.rect(self.screen, (154, 127, 127), (self.pos[0]+3, \
                             self.pos[1]+3, self.size[0]-6, self.size[1]-6))
            self.main.update()
