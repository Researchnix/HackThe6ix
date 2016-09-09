from Tkinter import *
import Master



class Painter(Frame):
    total = 1
    mas = Master.Master()
    scaling = 10.0
    intersection_Size = 4




### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### INITIALIZATION ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ##### #


    def __init__(self, master=None):
        self.initializeFrame(master)
        self.initializeMap()
        self.after(10, self.update)


    def initializeFrame(self, master):
        Frame.__init__(self, master)
        Pack.config(self)
        self.createWidgets()

    def initializeMap(self):
        self.mas.printState()
        # Draw the intersections and streets
        for inter in self.mas.m.intersections:
            self.drawIntersection(inter, self.scaling * self.mas.m.intersections[inter][0], self.scaling * self.mas.m.intersections[inter][1])
        for street in self.mas.m.streets:
            self.drawStreet(street)
        for car in self.mas.cars:
            self.drawCar(car)



 ##############################################
 ###            stepping function           ###
 ##############################################

    def update(self, *args):

        # Let the Master class do a time step
        self.mas.run(self.total)
        self.total += 1
        self.mas.printCars()

        for car in self.mas.cars:
            if car.needsUpdate:
                self.updateCar(car)
                car.needsUpdate = False
        self.after(100, self.update)


    def updateCar(self, car):
        dx = self.getDX(car)
        dy = self.getDY(car)
        self.draw.move(car.name, dx, dy)
    
    def drawIntersection(self, label, x, y):
        self.draw.create_rectangle(x-self.intersection_Size, y-self.intersection_Size, x+self.intersection_Size  ,y+self.intersection_Size ,tags=label, fill="blue")

    def drawStreet(self, street):
        x0 = self.mas.m.intersections[street[0]][0] * self.scaling
        y0 = self.mas.m.intersections[street[0]][1] * self.scaling
        x1 = self.mas.m.intersections[street[1]][0] * self.scaling
        y1 = self.mas.m.intersections[street[1]][1] * self.scaling
        #self.draw.create_rectangle(x0-1, y0-1, x1+1, y1)
        self.draw.create_line(x0, y0, x1, y1, fill="red",)

    def drawCar(self, car):
        x = self.getXY(car.curPos)[0]
        y = self.getXY(car.curPos)[1]
        self.draw.create_rectangle(x - 3, y - 3, x + 3, y + 3, tags=car.name, fill="green")


    def getXY(self, carPos):
        streetID = carPos[0]
        street = self.mas.m.streets[streetID]
        length = float(street[2])
        x0 = self.mas.m.intersections[street[0]][0] * self.scaling
        y0 = self.mas.m.intersections[street[0]][1] * self.scaling
        x1 = self.mas.m.intersections[street[1]][0] * self.scaling
        y1 = self.mas.m.intersections[street[1]][1] * self.scaling
        direction = [x1 - x0, y1 - y0]
        progress = float(carPos[1])
        return [x0 + progress/length * direction[0], y0 + progress/length * direction[1]] 

    def getDX(self, car):
        return self.getXY(car.curPos)[0] - self.getXY(car.oldPos)[0]

    def getDY(self, car):
        return self.getXY(car.curPos)[1] - self.getXY(car.oldPos)[1]
        

    def createWidgets(self):
        self.QUIT = Button(self, text='QUIT', foreground='red', command=self.quit)
        self.QUIT.pack(side=BOTTOM, fill=BOTH)
        self.draw = Canvas(self, width="10i", height="10i")
        #self.speed = Scale(self, orient=HORIZONTAL, from_=-100, to=100)
        #self.speed.pack(side=BOTTOM, fill=X)

        # all of these work..
        #self.draw.create_rectangle(0, 0, 10, 10, tags="thing", fill="blue")
        self.draw.pack(side=LEFT)

