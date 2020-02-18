import csv
import turtle

f = open("^DJI.csv","r")
reader = csv.reader(f)
data = list(reader); f.close();

print(data[0]);data = data[1:];
print("   0 \t   1 \t   2 \t   3 \t   4 \t      5 \t  6")

Date = []
Open = []
High = []
Low  = []
Close = []

lines = []
boxes = []
points = []


for each in data:
    Date.append(each[0])
    Open.append(float(each[1]))
    High.append(float(each[2]))
    Low.append(float(each[3]))
    Close.append(float(each[4]))

g = turtle.Screen()
g.title("Indicator E")
g.bgcolor("black")
g.setup(width=1000, height=700)
g.screensize(2000,20000)

scalingFactor = .2
yOffset = -5000

pen = turtle.RawPen(g)
pen.color("white")
pen.hideturtle()
pen.speed(0)

pen.up()
pen.goto(-990,340)
pen.down()
pen.goto(-990,-330)
pen.goto(-990,0)
#pen.goto(990,0)

pen.up()

############################################

class Point:
    pen = turtle.RawPen(g)
    pen.color("white")
    pen.hideturtle()
    pen.speed(0)
    
    def __init__(self,x,y, flag = None, date=0):
        self.x = x
        self.y = y
        self.flag = flag
        self.date = date

    def draw(self):
        x = self.x*scalingFactor
        y = self.y*scalingFactor+yOffset

        if self.flag == "close":
            self.pen.color("red")
        elif self.flag == "open":
            self.pen.color("green")

        width = 4
        self.pen.up()
        self.pen.goto(x-width/2,y+width/2)
        self.pen.down()
        self.pen.goto(x+width/2,y+width/2)
        self.pen.goto(x+width/2,y-width/2)
        self.pen.goto(x-width/2,y-width/2)
        self.pen.goto(x-width/2,y+width/2)
        self.pen.up()
        

class Line:
    pen = turtle.RawPen(g)
    pen.color("white")
    pen.hideturtle()
    pen.speed(0)
    
    def __init__(self,begin,end):
        #begin and end should be tuples
        self.begin = begin
        self.end = end

        self.slope = (end[1]-begin[1])/(end[0]-begin[0])
        self.yint = begin[1] - self.slope*begin[0]
        

    def intersect(self,line):
        1

    def draw(self):
        self.pen.up()
        self.pen.goto(scalingFactor*self.begin[0],
                      scalingFactor*self.begin[1]+yOffset)
        self.pen.down()
        self.pen.goto(scalingFactor*self.end[0],
                      scalingFactor*self.end[1]+yOffset)
        self.pen.up()

class BoxLine(Line):
    pen = turtle.RawPen(g)
    pen.color("orange")
    pen.hideturtle()
    pen.speed(0)

class Box:
    pen = turtle.RawPen(g)
    pen.color("orange")
    pen.hideturtle()
    pen.speed(0)
    
    def __init__(self,high,low,leftSide,rightSide):
        self.high = high
        self.low = low
        self.leftSide = leftSide
        self.rightSide = rightSide
        
        self.line = BoxLine(
                (leftSide,low),
                (rightSide,high)
            )

    def draw(self):
        
        high = self.high*scalingFactor+yOffset
        low = self.low*scalingFactor+yOffset
        leftSide = self.leftSide*scalingFactor
        rightSide = self.rightSide*scalingFactor
        
        
        self.pen.up()
        self.pen.goto(leftSide,high)
        self.pen.down()
        self.pen.goto(rightSide,high)
        self.pen.goto(rightSide,low)
        self.pen.goto(leftSide,low)
        self.pen.goto(leftSide,high)
        self.pen.up()

        self.line.draw()
        

############################################


def graphPeriod(n,di,bw): #n = lookback periods; di = start date; bw = box window
    h = 0 - 990/scalingFactor #running horizontal position offset by screen size
    boxLeft = boxRight = h

    for i in range(n):

        openPoint = Point(h,Open[di+i],flag="open",date=di+i)
        points.append(openPoint)

        h += .3*abs(Open[di+i]-Close[di+i])
        
        closePoint = Point(h,Close[di+i],flag="close",date=di+i)
        points.append(closePoint)
        
        h += .3*abs(Open[di+i+1]-Close[di+i])

        
    i = 0
    while i < len(points)-1:
        lines.append(
                Line( (points[i].x,points[i].y),
                      (points[i+1].x,points[i+1].y)
                    )
            )
        i+=1

    
    i = 0
    while i < len(points)-10:

        maxhigh = max(High[points[i].date:points[i+10].date])
        minlow = min(Low[points[i].date:points[i+10].date])

        boxes.append(
                Box(maxhigh,minlow,points[i].x,points[i+9].x)
            )
        
        i += 10


    for each in points:
        each.draw()
    for each in lines:
        each.draw()
    for each in boxes:
        each.draw()
            

    
graphPeriod(170,0,5)


        
