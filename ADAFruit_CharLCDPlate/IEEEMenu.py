from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from time import sleep
import os
lcd = Adafruit_CharLCDPlate()
RIGHT = 1
LEFT  = 2
UP    = 3
DOWN  = 4
SELECT= 5

#This class will be used to represent a single screen on the LCD menu
#All screens that will appear on the menu will be represented by a Screen or one of its
#Sub-classes.
class Screen():
    def __init__(self, lcd):
        self.rightScr  = None #have it by default have no external connections
        self.leftScr   = None
        self.upScr     = None
        self.downScr   = None
        self.selectScr = None
        self.lcd = lcd
        
    #Adds a branch to this node
    #newScr = Screen to be attached pos = one of the constants defined above
    def append(self, newScr, pos):
        newScr.selectScr = self.selectScr #have it inherit its parents select screen
        newScr.upScr = self #have it have its parent as its up screen
        if (pos == RIGHT):
            self.rightScr = newScr
        elif (pos == LEFT):
            self.leftScr = newScr
        elif (pos == DOWN):
            self.downScr = newScr

    #use this after a normal append() to connect screens horizontaly
    def sideAppend(self, newScr, pos):
        newScr.upScr = self.upScr
        newScr.selectScr = self.selectScr
        if (pos == RIGHT):
            self.rightScr = newScr
            newScr.leftScr = self
        elif (pos == LEFT):
            self.leftScr = newScr
            newScr.rightScr = self
            
    #Used to display information, in subclasses we may prefer to have it
    #access some cross thread Queue for info on hardware
    
    #0 Battery 1 Field 2 Other 3 Current Task
    def show(self, valueList):
        self.lcd.clear()
        self.lcd.message("B:" + str(valueList[0]) + " F:" +  str(valueList[1]) + " %var:" + str(valueList[2]) + "\n" + str(valueList[3]))
            
    #This will manage the reading of the LCD buttons as well as permit
    #sub-classes to have more costumized behavior through overriding
    def switch(self):
        if lcd.buttonPressed(lcd.RIGHT):
            return RIGHT
        if lcd.buttonPressed(lcd.LEFT):
            return LEFT
        if lcd.buttonPressed(lcd.UP):
            return UP
        if lcd.buttonPressed(lcd.DOWN):
            return DOWN
        if lcd.buttonPressed(lcd.SELECT):
            return SELECT
        else:
            return 0

class shutdownScreen(Screen):
    def __init__(self, lcd):
        Screen.__init__(self, lcd)
        self.offsent = False
    def show(self, valueList):
        if (self.offsent == False):
            self.lcd.clear()
            self.lcd.message("Shutdown")
            os.system("sudo halt")
            self.offsent = True

class ConfirmShutdown(Screen):
    def __init__(self, lcd):
        Screen.__init__(self, lcd)
    def show(self, valueList):
        self.lcd.clear()
        self.lcd.message("Confirm Shutdown\n Dwn to confirm")
            
        #Simply a placeholder for specified sub-classes
class outputScreen(Screen):
    def __init__(self, lcd, text):
        Screen.__init__(self, lcd, text)
    #with this class overright the show() method to deal with hardware interaction

#This class will serve as the overall manager of the screen tree
class Menu():
    def __init__(self, firstScreen):
        self.screen = firstScreen
        self.pressed = False
        
    #The overall "do-everything" loop that is in charge of the functions that mus be performed
    #constantly
    def menu(self, valueList):
        self.screen.show(valueList)
        direction = self.screen.switch()
        if(direction != 0):
            self.switch(direction)
            self.pressed = True
        else:
            self.pressed = False
                
    #This reads what the screen switch method has to say and changes the active screen to whatever
    #was decided
    def switch(self, direction):
        if self.pressed == False:
            if (direction == RIGHT):
                if (self.screen.rightScr != None):
                    self.screen = self.screen.rightScr
            if (direction == LEFT):
                if (self.screen.leftScr != None):
                    self.screen = self.screen.leftScr
            if (direction == UP):
                if (self.screen.upScr != None):
                    self.screen = self.screen.upScr
            if (direction == DOWN):
                if (self.screen.downScr != None):
                    self.screen = self.screen.downScr
            if (direction == SELECT):
                if (self.screen.selectScr != None):
                    self.screen = self.screen.selectScr

#select, right, left, up, down
main = Screen(lcd)
main.selectScr = main
confirm = ConfirmShutdown(lcd)
shutdown = shutdownScreen(lcd)
main.append(confirm, DOWN)
confirm.append(shutdown, DOWN)
menu = Menu(main)


def display_menu(valueList):
    menu.menu(valueList)
    
