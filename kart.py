##############KART CLASS###########3
import math
from hikaBGE import hikaMath
from mathutils import Vector

####FUNCTIONS####
def getWheels(car):
    """Get named wheels even grandchilds"""
    dic={}
    child=car.children
    lista=list()
    lista=child
    for j in child:
        lista=lista+ j.children
    for i in lista:
        if "FL" in i.name:
            dic["FL"]=i
        elif "FR" in i.name:
            dic["FR"]=i
        elif "BL" in i.name:
            dic["BL"]=i
        elif "BR" in i.name:
            dic["BR"]=i
        else:
            pass
    return(dic)

class GoKart(object):
    """Base class for automoviles, karts, cars and vehicle moBLon
    Cd= dragging coeficient"""
    def __init__(self, mainObject, engineForce,turnForce,brakeForce, wheelRotationAxis=2,frontalAxis=1, lateralAxis=0,upAxis=2, areaY=2, areaX=6,areaZ=10,Cd=0.5,airDensity=1.29,wheelParent=None,wheelFL=None,wheelFR=None,wheelBL=None,wheelBR=None):
        self.mainObject=mainObject
        self.engineForce=engineForce
        self.turnForce=turnForce
        self.brakeForce=brakeForce
        self.wheelRotationAxis=wheelRotationAxis
        self.frontalAxis=frontalAxis
        self.lateralAxis=lateralAxis
        self.upAxis=upAxis
        self.area=[areaX,areaY,areaZ]
        self.Cd=Cd
        self.airDensity=airDensity
        self.wheelParent=wheelParent
        self.wheels={"FL":wheelFL,"FR":wheelFR,"BL":wheelBL,"BR":wheelBR}
        self.dragFactor=-0.5*self.Cd*self.airDensity
        self.wheelAngle=0.1
        self.drags=self.calcDrags()

    def calcDrags(self):
        dragsList=[0,0,0]
        for i in range(3):
            dragsList[i]=self.dragFactor*self.area[i]*(self.mainObject.getLinearVelocity()[i]**2)
        return(dragsList)

    def applyDrag(self):
        self.mainObject.applyForce((self.drags[0],self.drags[1],self.drags[2]),True)
        return(True)

    def __calcTorque__(self, angle, force, distance):
        return(force*math.sin(angle)*distance)

    def calcTireAngle(self):
        """FL=self.wheels["FL"].localOrientation.to_euler("XYZ")[self.wheelRotationAxis]
        FR=self.wheels["FR"].localOrientation.to_euler("XYZ")[self.wheelRotationAxis]
        BL=self.wheels["BL"].localOrientation.to_euler("XYZ")[self.wheelRotationAxis]
        BR=self.wheels["BR"].localOrientation.to_euler("XYZ")[self.wheelRotationAxis]
        pF=(FL+FR)/2
        pB=(BR+BL)/2
        return(abs(pF-pB))"""
        return(abs((self.wheelParent.localOrientation.to_euler()[self.wheelRotationAxis])))

    def _rotateWheels(self,angle):
        if self.wheelRotationAxis==0:
            self.wheelParent.applyRotation((angle,0,0),True)
        elif self.wheelRotationAxis==1:
            self.wheelParent.applyRotation((0,angle,0),True)
        elif self.wheelRotationAxis==2:
            self.wheelParent.applyRotation((0,0,angle),True)
        else:
            print("Wrong whelRotation axis:",self.wheelRotationAxis)

    def turnWheeels(self,direction):
        #Con flecha
        maxAngle= math.radians(50)
        angle=self.wheelParent.localOrientation.to_euler()[self.wheelRotationAxis]
        if direction>0:
            if angle<maxAngle:
                self._rotateWheels(self.wheelAngle)
            else:
                pass
        if direction<0:
            if angle> -maxAngle:
                self._rotateWheels(-self.wheelAngle)
        else:
            pass

    def turn(self, direction):
        """Aply a torque to the mainObject
        direction=-1/1"""
        self.turnWheeels(direction)
        angle=self.calcTireAngle()
        posFW=(self.wheels["FL"].worldPosition+self.wheels["FR"].worldPosition)*0.5
        mainPosition=self.mainObject.worldPosition
        distance=(posFW-mainPosition).length
        torque= self.__calcTorque__(angle, self.turnForce, distance)*direction
        if self.upAxis==0:
            self.mainObject.applyTorque((torque, 0, 0), True)
        elif self.upAxis==1:
            self.mainObject.applyTorque((0, torque, 0), True)
        elif self.upAxis==2:
            self.mainObject.applyTorque((0, 0, torque), True)
        else:
            print("Error applying torque, wrong lateralAxis:", self.upAxis)

    def gas(self, customForce=None):
        if customForce==None:
            if self.frontalAxis==0:
                self.mainObject.applyForce((self.engineForce, 0, 0), True)
            elif self.frontalAxis==1:
                self.mainObject.applyForce((0, self.engineForce, 0), True)
            elif self.frontalAxis==2:
                self.mainObject.applyForce((0, 0, self.engineForce), True)
            else:
                print("Error applying gas, wrong frontalAxis:", self.frontalAxis)
        else:
            if self.frontalAxis==0:
                self.mainObject.applyForce((customForce, 0, 0), True)
            elif self.frontalAxis==1:
                self.mainObject.applyForce((0,customForce, 0), True)
            elif self.frontalAxis==2:
                self.mainObject.applyForce((0, 0,customForce), True)
            else:
                print("Error applying gas, wrong frontalAxis:", self.frontalAxis)

    def brake(self,minV=2,force=None):
        vel=self.mainObject.getLinearVelocity()[self.frontalAxis]
        velX=self.mainObject.getLinearVelocity()[self.lateralAxis]
        if abs(vel)>minV:
            if vel>0:
                self.gas(-self.brakeForce)
                #print("Brake negativo")
            elif vel<0:
                self.gas(self.brakeForce)
                #print("Brake positivo")
            else:
                print("Error inesperado, vel:",vel," brakeForce: ",self.brakeForce)
        """if abs(velX)>minV:
            vec=Vector((0,0,0))
            if self.lateralAxis==0:
                vec.x=self.brakeForce
            elif self.lateralAxis==1:
                vec.y=self.brakeForce
            elif self.lateralAxis==2:
                vec.z=self.brakeForce
            else:
                pass
            if velX>0:
                vec= -vec
            self.mainObject.applyForce(vec,True)
            print(vec)"""

    def wheelRoll(self):
        """Llamar al final de cada frame"""
        rotFact=0.1
        for w in self.wheels:
            self.wheels[w].applyRotation((self.mainObject.getLinearVelocity()[self.frontalAxis]*rotFact,0,0),True)

    def resetWheel(self):
        a=self.wheelParent.localOrientation.to_euler()[self.wheelRotationAxis]
        if a==0:
            dire=1
        else:
            dire=(a/(abs(a)))*-1
        v=Vector((0,0,0))
        factor=0.1
        if a !=0:
            if self.wheelRotationAxis==0:
                v.x=factor*dire
            elif self.wheelRotationAxis==1:
                v.y=factor*dire
            elif self.wheelRotationAxis==2:
                v.z=factor*dire
            else:
                pass
            self.wheelParent.applyRotation(v,True)
        else:
            pass

    def wheelie(self,direction):
        rot=0.05
        maxAngle=math.radians(45)
        vect= Vector((0,0,0))
        if self.lateralAxis==0:
            vect.x=rot
        elif self.lateralAxis==1:
            vect.y=rot
        elif self.lateralAxis==2:
            vect.z=rot
        else:
            pass
        vect=vect*direction
        angle=self.mainObject.localOrientation.to_euler()[self.lateralAxis]
        #print(angle,vect)
        if abs(angle)<maxAngle:
            self.mainObject.applyRotation(vect,True)