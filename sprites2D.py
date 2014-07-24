import bge

class Animation(object):
    """Base class for animations for Animations for 2D Sprites
    frames=list(str())"""
    def __init__(self,*frames):
        self.frames=list()
        if "list" in str(frames[0].__class__):
            self.frames=frames[0]
        else:
            for i in range(0,len(frames)):
                self.frames.append(frames[i])
    def __getitem__(self,index):
        return(self.frames[index])
    def __str__(self):
        a="Animation:("
        for i in range(len(self.frames)-1):
            a+=self.frames[i]+", "
        a+=self.frames[-1]+")"
        return(a)
    def __repr__(self):
        return(self.__str__())
    def __len__(self):
        return(len(self.frames))    
                
class Sprite2D():
    """Base class for animables 2D Sprites
    mainObject= The object name that owns all actions
    alwaysSensor='Always' sensor attached"""
    ##########      ##########
    # ALWAYS # ---> # PYTHON #
    ##########      ##########

    #Setup:
    #The owner must have a propierty named:"currentFrame"
    #type int, value=0
    #Connect the Python controller to a Always sensors
    
    def __init__(self,mainObject,alwaysSensor): 
        self.main=bge.logic.getCurrentScene().objects[mainObject]
        self.animations=dict()
        self.always=bge.logic.getCurrentController().sensors[alwaysSensor]
        self.always.usePosPulseMode=True
        self.currentAnimation=None
    def addAnimation(self,name,animation):
        self.animations[name]=animation
    def playAnimation(self,animation,frameRate,mode):
        tic=bge.logic.getAverageFrameRate()
        ani=self.animations[animation]
        self.always.frequency=int(tic/frameRate)
        self.currentAnimation=animation
        if mode=="loopStop":
            if self.main["currentFrame"]==(len(ani)-1):
                self.main["currentFrame"]=0
            else:
                self.main["currentFrame"]+=1
                self.main.replaceMesh(ani[self.main["currentFrame"]])
        elif mode=="playOnce":
            if self.main["currentFrame"]==(len(ani)-1):
                self.currentAnimation=None
            else:
                self.main["currentFrame"]+=1
                self.main.replaceMesh(ani[self.main["currentFrame"]])

class Character2D():
    """Base clase for 2D character
    sprite: Sprite()
    collision: Object name to use as physical interactions"""
    def __init__(self,sprite,parent):
        self.sprite=sprite
        self.parent=bge.logic.getCurrentScene().objects[parent]
