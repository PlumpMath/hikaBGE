#Classes and functions for input in the bge

import bge
KEYCODES={"ACCENTGRAVE":bge.events.ACCENTGRAVEKEY, "A":bge.events.AKEY,
            "BACKSLASH":bge.events.BACKSLASHKEY, "BACKSPACE":bge.events.BACKSPACEKEY,
            "B":bge.events.BKEY, "CAPSLOCK":bge.events.CAPSLOCKKEY, "C":bge.events.CKEY,
            "COMMA":bge.events.COMMAKEY, "DEL":bge.events.DELKEY, "D":bge.events.DKEY,
            "DOWNARROW":bge.events.DOWNARROWKEY, "EIGHT":bge.events.EIGHTKEY,
            "E":bge.events.EKEY, "END":bge.events.ENDKEY, "ENTER":bge.events.ENTERKEY,
            "EQUAL":bge.events.EQUALKEY, "ESC":bge.events.ESCKEY, "F10":bge.events.F10KEY,
            "F11":bge.events.F11KEY, "F12":bge.events.F12KEY, "F13":bge.events.F13KEY,
            "F14":bge.events.F14KEY, "F15":bge.events.F15KEY, "F16":bge.events.F16KEY,
            "F17":bge.events.F17KEY, "F18":bge.events.F18KEY, "F19":bge.events.F19KEY,
            "F1":bge.events.F1KEY, "F2":bge.events.F2KEY, "F3":bge.events.F3KEY,
            "F4":bge.events.F4KEY, "F5":bge.events.F5KEY, "F6":bge.events.F6KEY,
            "F7":bge.events.F7KEY, "F8":bge.events.F8KEY, "F9":bge.events.F9KEY,
            "FIVE":bge.events.FIVEKEY, "F":bge.events.FKEY, "FOUR":bge.events.FOURKEY,
            "G":bge.events.GKEY, "H":bge.events.HKEY, "HOME":bge.events.HOMEKEY,
            "I":bge.events.IKEY, "INSERT":bge.events.INSERTKEY, "J":bge.events.JKEY,
            "K":bge.events.KKEY, "LEFTALT":bge.events.LEFTALTKEY,
            "LEFTARROW":bge.events.LEFTARROWKEY, "LEFTBRACKET":bge.events.LEFTBRACKETKEY,
            "LEFTCTRL":bge.events.LEFTCTRLKEY, "LEFTSHIFT":bge.events.LEFTSHIFTKEY,
            "LINEFEED":bge.events.LINEFEEDKEY, "L":bge.events.LKEY, "MINUS":bge.events.MINUSKEY,
            "M":bge.events.MKEY, "NINE":bge.events.NINEKEY, "N":bge.events.NKEY,
            "O":bge.events.OKEY, "ONE":bge.events.ONEKEY, "PADASTER":bge.events.PADASTERKEY,
            "PADPLUS":bge.events.PADPLUSKEY, "PADSLASH":bge.events.PADSLASHKEY,
            "PAGEDOWN":bge.events.PAGEDOWNKEY, "PAGEUP":bge.events.PAGEUPKEY,
            "PAUSE":bge.events.PAUSEKEY, "PERIOD":bge.events.PERIODKEY, "P":bge.events.PKEY,
            "Q":bge.events.QKEY, "QUOTE":bge.events.QUOTEKEY, "RET":bge.events.RETKEY,
            "RIGHTALT":bge.events.RIGHTALTKEY, "RIGHTARROW":bge.events.RIGHTARROWKEY,
            "RIGHTBRACKET":bge.events.RIGHTBRACKETKEY, "RIGHTCTRL":bge.events.RIGHTCTRLKEY,
            "RIGHTSHIFT":bge.events.RIGHTSHIFTKEY, "R":bge.events.RKEY,
            "SEMICOLON":bge.events.SEMICOLONKEY, "SEVEN":bge.events.SEVENKEY,
            "SIX":bge.events.SIXKEY, "S":bge.events.SKEY, "SLASH":bge.events.SLASHKEY,
            "SPACE":bge.events.SPACEKEY, "TAB":bge.events.TABKEY, "THREE":bge.events.THREEKEY,
            "T":bge.events.TKEY, "TWO":bge.events.TWOKEY, "U":bge.events.UKEY,
            "UPARROW":bge.events.UPARROWKEY, "V":bge.events.VKEY, "W":bge.events.WKEY,
            "X":bge.events.XKEY, "Y":bge.events.YKEY,
            "ZERO":bge.events.ZEROKEY, "Z":bge.events.ZKEY}
MOUSECODES={"LEFT":bge.events.LEFTMOUSE, "MIDDLE":bge.events.MIDDLEMOUSE,
            "X":bge.events.MOUSEX, "Y":bge.events.MOUSEY,
            "RIGHT":bge.events.RIGHTMOUSE, "WHEELDOWN":bge.events.WHEELDOWNMOUSE,
            "WHEELUP":bge.events.WHEELUPMOUSE}

class Button(object):
    """Base class for input events for Pads"""
    def __init__(self):
        self.keyEvents=dict()
        self.mouseEvents=dict()
        self.sensorsEvents=dict()
    def addKey(self,key):
        """key:str() eg:A,B,LEFTARROW"""
        key=key.upper()
        if key in KEYCODES:
            self.keyEvents[key]=KEYCODES[key]
        else:
            raise ValueError("Key must be a supported BGE.events")
    def addMouse(self,mouse):
        """mouse:str() eg:LEFT, MIDDLE, X, Y"""
        mouse=mouse.upper()
        if mouse in MOUSECODES:
            self.mouseEvents[mouse]=MOUSECODES[mouse]
        else:
            raise ValueError("Mouse must be a supported bge.events")
    def addSensor(self,sensor):
        """sensor:str() the name of a connected sensor"""
        s=bge.logic.getCurrentController().sensors
        if sensor in s:
            self.sensorsEvents[sensor]=s[sensor]
        else:
            raise ValueError("Sensor must be a sensor's name connected to the current controller")
    def addJoystickButton(self,number):
        pass
    def status(self):
        mayor=0
        keyboard=bge.logic.keyboard
        mouse=bge.logic.mouse
        for k in self.keyEvents:
            if keyboard.events[self.keyEvents[k]]>mayor:
                mayor=keyboard.events[self.keyEvents[k]]
            else:
                pass
        for m in self.mouseEvents:
            if mouse.events[self.mouseEvents[m]]>mayor:
                mayor=mouse.events[self.mouseEvents[m]]
            else:
                pass
        for s in self.sensorsEvents:
            if str(self.sensorsEvents[s].__class__)=="<class 'SCA_JoystickSensor'>":
                if self.sensorsEvents[s].connected==False:
                    break
            if self.sensorsEvents[s].status>mayor:
                mayor=self.sensorsEvents[s].status
            else:
                pass
        return(mayor)
    def __repr__(self):
        return("Event()")
    def __str__(self):
        return("Event")
    def __nonzero__(self):
        if self.status()>0:
            return(True)
        else:
            return(False)

class Pad(object):
    """Base class for Pad objects,
        pad is a control objects, is a collection of Button object
        that allow easy and fast managament of mutltiple input events"""
    def __init__(self):
        self.len=0
        self.state=True
    def on(self):
        self.state=True
    def off(self):
        self.state=False
    def addButton(self,name,button):
        if "str" in str(name.__class__):
            if "Button" in str(button.__class__):
                self.__dict__[name]=button
                self.len+=1
            else:
                raise TypeError("Button must be a Button object")
        else:
            raise TypeError("Name must be a string")
    def buttons(self):
        l=list()
        for i in self.__dict__:
            if "Button" in (self.__dict__[i].__class__):
                l.append(i)
            else:
                pass
        return(l)
    ####GET button status
    def get(self,buttonName):
        """buttonName: Button name: str"""
        return(self.__dict__[buttonName].status())
    ######################3
    def __str__(self):
        return ("Pad")
    def __repr(self):
        return("Pad()")
    def __len__(self):
        return(self.len)
    def __getitem__(self,item):
        l=list()
        for i in self.__dict__:
            if "Button" in (self.__dict__[i].__class__):
                l.append(self.__dict__[i])
            else:
                pass
        return(l[item])
#################################3
###### 3 buttons pads

class Pad3Buttons(Pad):
    """Custom and easy 3 buttons pad
        UP, DOWN, LEFT, RIGHT, X,Y,Z with event a keyboard support
        key arguments are STR and Event arguments are Sensor's names:str"""
    def __init__(self,UpSensor,UpKey,DownSensor,DownKey,LeftSensor,LeftKey,RightSensor,RightKey,XSensor,XKey,YSensor=None,YKey=None,ZSensor=None,ZKey=None):
        self.len=0
        self.state=True
        self.UpBoton=Button()
        self.UpBoton.addSensor(UpSensor)
        self.UpBoton.addKey(UpKey)
        self.DownBoton= Button()
        self.DownBoton.addSensor(DownSensor)
        self.DownBoton.addKey(DownKey)
        self.LeftBoton= Button()
        self.LeftBoton.addSensor(LeftSensor)
        self.LeftBoton.addKey(LeftKey)
        self.RightBoton= Button()
        self.RightBoton.addSensor(RightSensor)
        self.RightBoton.addKey(RightKey)
        self.XBoton= Button()
        self.XBoton.addSensor(XSensor)
        self.XBoton.addKey(XKey)
        if YSensor != None or YKey != None:
            self.YBoton= Button()
            self.YBoton.addSensor(YSensor)
            self.YBoton.addKey(YKey)
        if ZSensor != None or ZKey != None:
            self.ZBoton= Button()
            self.ZBoton.addSensor(ZSensor)
            self.ZBoton.addKey(ZKey)
        ######Agregar botones al Pad####
        self.addButton("Up",self.UpBoton)
        self.addButton("Down",self.DownBoton)
        self.addButton("Left",self.LeftBoton)
        self.addButton("Right",self.RightBoton)
        self.addButton("X",self.XBoton)
        self.addButton("Y",self.YBoton)
        self.addButton("Z",self.ZBoton)
    def __str__(self):
        return("Pad with 3 buttons")