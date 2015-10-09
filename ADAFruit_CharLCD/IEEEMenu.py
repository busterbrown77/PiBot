import Adafruit_CharLCDPlate
import time
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
    def __init__(self, lcd, text):
        self.rightScr  = None #have it by default have no external connections
        self.leftScr   = None
        self.upScr     = None
        self.downScr   = None
        self.selectScr = None
        self.text = text
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
    def show(self):
        self.lcd.clear()
        self.lcd.message(self.text)
        
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

        
class inputScreen(Screen):
    def __init__(self, lcd, text):
        Screen.__init__(self, lcd, text)

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
    def menu(self):
        while True:
            if (hasattr(self.screen, "input")):
                self.screen.input()
            self.screen.show()
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
main = Screen(lcd, "Main")
main.selectScr = main
outScreen = Screen(lcd, "     Output    ")
main.append(outScreen, DOWN)
inputScreen = Screen(lcd, "     Input    ")
outScreen.sideAppend(inputScreen, LEFT)
shutScreen = Screen(lcd, "     ShutDown")
inputScreen.sideAppend(shutScreen, LEFT)
menu = Menu(main)
last = 0
lcd.clear()
menu.menu()
