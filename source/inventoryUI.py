#!/usr/bin/env python
"""
https://github.com/prompt-toolkit/python-prompt-toolkit/blob/master/examples/full-screen/full-screen-demo.py
"""
from __future__ import unicode_literals

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout.containers import Window, VSplit, HSplit, FloatContainer, Float, WindowAlign, is_container, ConditionalContainer, DynamicContainer
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea, Label, Frame, Box, Checkbox, Dialog, Button, MenuContainer, MenuItem
from source.customBase import RadioList2 
#from pygments.lexers.html import HtmlLexer
from prompt_toolkit.layout.margins import ScrollbarMargin, NumberedMargin
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.formatted_text import FormattedText

from source.lists import getRandomAttackVerb
from source.utils import wait, wrap
import random

class InventoryUI():

    def __init__(self, player):
        self.player = player
        self.playerClans = ' '.join(self.player.clantags)
        if len(self.player.clantags) > 0 : 
            self.playerName = FormattedText([
                ('#ffffff', player.aspect['name']),
                ('', ' '),
                ('#cc00cc', self.playerClans, "utf-8"),
            ]) 
        else: 
            self.playerClans =  self.playerName = FormattedText([
                ('#ffffff', player.aspect['name']),
            ]) 
        self.result = None

        self.mainRadiosRows = []
        self.populateMainRadios() # declares self.mainRadios
        self.currentRadios = self.mainRadios
        self.description = self.mainRadios.description # description is whataver is in the description box on the right
        self.requestingConfirmation = False
        
        self.bindings = KeyBindings()
        self.bindings.add('right' )(focus_next)
        self.bindings.add('tab' )(focus_next)
        self.bindings.add('s-tab')(focus_previous)
        self.bindings.add('left')(focus_previous)
        self.bindings.add('c-m')(self.handleEnter)
        self.bindings.add('escape')(self.handleEscape)

        self.style = Style.from_dict({
            'dialog.body':        'bg:#000000 #ffcccc', #background color, text color
        })

        self.application = Application(
            layout=Layout(
                self.getRootContainer(),
                focused_element=self.mainRadios,
            ),
            key_bindings=self.bindings,
            style=self.style,
            mouse_support=True,
            full_screen=True,
            )

    def handleEscape(self, event):
        self.requestingConfirmation = False
        if self.currentRadios == self.mainRadios:
            self.done()
        else: # return to main page
            self.populateMainRadios()
            self.currentRadios = self.mainRadios
            # self.description = self.mainRadios.description
            self.refresh()

    def handleEnter(self, event):
        if self.requestingConfirmation:
            self.requestingConfirmation = False
            self.player.activateItem(self.listOfItems[self.currentRadios._selected_index])
            self.updateListOfItems()
            # TODO sound music, sound effect of eating a consumable
            return

        if self.currentRadios == self.mainRadios: # if on main page
            self.updateListOfItems()
            self.makeListCurrentRadios(self.listOfItems) 
        elif self.currentRadios == self.selectedRadios: # if not on main page
            if self.listOfItems[self.currentRadios._selected_index].type == "consumable":
                self.requestingConfirmation = True
                self.refresh(setDescription="Eat it?")
                return
            self.player.activateItem(self.listOfItems[self.currentRadios._selected_index]) # can delete items
            self.makeListCurrentRadios(self.listOfItems,self.selectedRadios._selected_index) 

    def updateListOfItems(self):
        if   self.mainRadios._selected_index == 0:
            self.listOfItems = self.player.getAllInventoryItemsAsObjectList(_type='weapon')
        elif self.mainRadios._selected_index == 1:
            self.listOfItems = self.player.getAllInventoryItemsAsObjectList(_type='armour')
        elif self.mainRadios._selected_index == 2:
            self.listOfItems = self.player.getAllInventoryItemsAsObjectList(_type='consumable')
        elif self.mainRadios._selected_index == 3:
            self.listOfItems = self.player.getAllInventoryItemsAsObjectList(_type='quest')
        if len(self.listOfItems) == 0:
            self.populateMainRadios()
            self.currentRadios = self.mainRadios
            self.refresh()



    def makeListCurrentRadios(self, lisp, selectedIndex=0):
        self.listOfItemsTupled = self.tuplify(lisp)
        self.selectedRadios = RadioList2(
            values=self.listOfItemsTupled,
            app = self)    
        self.selectedRadios._selected_index = selectedIndex
        self.currentRadios = self.selectedRadios 
        # self.description = self.currentRadios.values[selectedIndex]
        self.refresh()

    def tuplify(self, listt):
        if len(listt) == 0:
            return [] # should never see this
        newlist=[]
        for i in range(len(listt)):
            l = []
            l.append(self.unicodify(listt[i].description))
            l.append(self.unicodify(listt[i].getName()))
            newlist.append( tuple(l) )
        return newlist

    def refresh(self, setDescription=False):
        #self.populateMainCategories()
        if setDescription:
            self.description = setDescription
        else:
            index = self.currentRadios._selected_index
            self.description = self.currentRadios.values[index][0]
        
        self.application.layout=Layout(
            self.getRootContainer(),
            focused_element=self.currentRadios)
            
        
    def populateMainRadios(self):
        self.mainRadiosRows = []
        self.populateMainRadiosHelper('weapon')
        self.populateMainRadiosHelper('armour')
        self.populateMainRadiosHelper('consumable')
        self.populateMainRadiosHelper('quest')
        self.mainRadios = RadioList2(
            values=self.mainRadiosRows,
            app = self)

    def populateMainRadiosHelper(self, category):
        s = self.unicodify(self.player.getAllInventoryItemsAsString(_type=category, showEquipped=True))
        if not s == '': 
            tup = []
            tup.append(s)
            if category == 'weapon': tup.append('Weapons')
            else: tup.append(category.capitalize())
            self.mainRadiosRows.append( tuple(tup) )

    def makeFormattedText(self, text, color='#ffffff'):
        return FormattedText([
            (color, str(text) )# this shit is shit
        ])

    def unicodify(self, text):
        if isinstance(text, str):
            return str(text)
        else:
            return text

    def getStats(self):
        s = ''
        s += "Health:   " + str(self.player.hp) + " / " + str(self.player.maxhp) + "\n"
        s += "Level:    " + str(self.player.level) + "\n"
        s += "XP:       " + str(self.player.xp) + "\n"
        s += "Money:    $" + str(self.player.money) + "\n"
        s += "Strength: " + str(self.player.strength) 

        return s
        


    # returns new root container (updates text and stuff)
    def getRootContainer(self):
        width = 60
        smallerWidth = 40
        height = 10
        descriptionTitle = FormattedText([('#ffffff', "Description")])# makes it white
        actionsTitle = FormattedText([('#ffffff', "Inventory")])
        desc = wrap(self.description, width-2)
        root_container = VSplit([
            HSplit([
                Dialog(
                    title=actionsTitle,
                    body=HSplit([
                        self.currentRadios,
                    ], )
                ),
            ], padding=0, width = smallerWidth, ),
            HSplit([
                Dialog(
                    title = descriptionTitle,
                    body=Label(desc),
                ),
            ], padding=0, width = width, height= height,),
            HSplit([
                Dialog(
                    title = self.playerName,
                    body=Label(self.getStats()),
                ),
            ], padding=0, width = smallerWidth, height= height,),
        ])
        return root_container 

    def run(self):
        self.application.run()

    def done(self):
        self.result = "hit escape"
        get_app().exit(result="hit escape")
 
# TODO:
# fix escaping after changing equip status inst reflected in main menu
