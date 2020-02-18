from tkinter import *
import os
import csv
import copy


class App:
    def __init__(self, master):
        ###VARS:
        self.radioSignal = IntVar()
        self.pathEntryText = StringVar()
        self.truckWidth = StringVar()
        self.truckLength = StringVar()

        self.master = master 
        ########

        
        Label(master, text='Boxes File:').grid(row=0, column=0, sticky=E,padx=2)
        Label(master, text='Width:').grid(row=2, column=0, sticky=E,padx=2)
        Label(master, text='Length:').grid(row=3, column=0, sticky=E,padx=2)
        
        #A named Entry:
        self.pathEntry = Entry(master, width=75,textvariable=self.pathEntryText)
        self.pathEntry.insert(0,'...')
        self.pathEntry['state']='readonly'
        self.pathEntry.grid(row=0,column=1,columnspan=2)

        Button(master, text='Select File',command=self.openFileClicked).grid(row=0,column=3,padx=2)
        
        #Truck Stats:
        Label(master,text='Truck Dimensions').grid(row=1,column=1,sticky=W,padx=27)
        self.widthEntry = Entry(master, textvariable=self.truckWidth)
        self.widthEntry.grid(row=2,column=1,sticky=W)
        
        self.lengthEntry = Entry(master, textvariable=self.truckLength)
        self.lengthEntry.grid(row=3,column=1,sticky=W)

        #Algorithm stuff:
        Label(master,text='Packing Algorithm').grid(row=1,column=2)
        r1 = Radiobutton(master, text='Largest Box First',variable=self.radioSignal,value=10)
        r2 = Radiobutton(master, text='Smallest Box First',variable=self.radioSignal,value=11)
        r3 = Radiobutton(master, text='Downsize each box to 1x1 by crushing each one',variable=self.radioSignal,value=123)
        r1.grid(row=2,column=2); r2.grid(row=3,column=2); r3.grid(row=4,column=2);
        

        #Big Button:
        bigButton = Button(master, text='Pack Boxes & Save Results', command=self.packNSaveClicked)
        bigButton.grid(row=5,column=0,columnspan=4,stick=E+W)


    def initializeTruck(self): #makes an empty truck of specified size
        self.truck = []
        length = int(self.truckLength.get())
        width = int(self.truckWidth.get())

        for y in range(length):
            workingList = []
            for x in range(width):
                workingList.append("")
            self.truck.append(workingList)


    def openFileClicked(self):
        self.filePath = filedialog.askopenfilename()

        if self.filePath != '' and self.filePath != ():
            #for some reason, askopenfilename returns an empty tuple sometimes...
            #anyways...
            self.pathEntryText.set(self.filePath)
        else:
            self.pathEntryText.set('...')


    def readBoxesFile(self):
        self.csvData = []
        
        f = open(self.filePath,'r')
        csvReader = csv.reader(f)
        
        try:
            for line in csvReader:
                if len(line) != 3:
                    raise ValueError
                
                line[1] = int(line[1])
                line[2] = int(line[2])
                self.csvData.append(line)
        except:
            raise ValueError
        f.close()


    def isValidLocation(self, row, column, width, length):
        #Gonna use try and except here to deal with possible index out of range errors
        try:
            for y in range(length):
                for x in range(width):
                    if self.truck[row+y][column+x] != '':
                        return False
            return True
        except:
            return False
        #How this works:
        #row and column are the starting location for the check. (Upper left corner of box)
        #The double for-loop sweeps/scans the area of the truck where
        #the box would be placed. If any cell in the area is occupied,
        #we hit the 'return False.' If we run out of room (index out of range),
        #we hit the 'return False.' 


    def fillTruckLocation(self, row, column, boxData):
        #boxData looks like:
        #[BOX ID, LENGTH, WIDTH]
        length = boxData[1]
        width = boxData[2]
        
        for y in range(length):
            for x in range(width):
                self.truck[row+y][column+x] = boxData[0]
        

    def packBox(self, boxData):
        #boxData looks like:
        #[BOX ID, LENGTH, WIDTH]
        length = boxData[1]
        width = boxData[2]
        
        for y in range(len(self.truck)):
            for x in range(len(self.truck[0])):
                if self.truck[y][x] == '':
                    if self.isValidLocation(y,x,width,length):
                        self.fillTruckLocation(y,x,boxData)
                        return True
        #Well after all that searching and checking... nothing good was found. So:
        return False
                    

    def packTruck(self):
        boxes = copy.deepcopy(self.csvData)
        #A working copy of the csvData ^

        for i in range(len(boxes)):
            boxes[i].append(boxes[i][1]*boxes[i][2])
            #So to each box, I append a number representing their areas.
            #And then I reverse the record so that I can have each one sorted
            #with area being the first element compared.
            boxes[i].reverse()
        
        boxes.sort()
        #Boxes are sorted from small to big.
        #So unless the user hits the radiobutton to pack largest first,
        #The boxes will be packed with the smallest first.

        if self.radioSignal.get() == 10:
            #if the intvar's value is 10, that signals that we wanna pack large boxes first.
            boxes.reverse()
            #boxes is now sorted from big to small.

        #done sorting. Now to make boxes usable by the rest of the program again:
        for i in range(len(boxes)):
            del boxes[i][0] #Getting rid of the entry for area
            boxes[i].reverse()#Now the box's entry is back to normal like:
            #[BOX ID, LENGTH, WIDTH] instead of [AREA, WIDTH, LENGTH, BOX ID]



        #########################################################
        ###EXTRA CREDIT PART:

        if self.radioSignal.get() == 123: #123 is the signal that it's okay to crush the boxes
            if messagebox.askyesno(message='Is it really okay to crush the boxes? If not, they will just be rotated and packed smallest first.'):
                for i in range(len(boxes)):
                    #Each box looks like: [BOX ID, LENGTH, WIDTH], remember?
                    boxes[i][1] = 1 #Just changed length to 1
                    boxes[i][2] = 1 #Just changed width to 1
                
        #The boxes have been crushed down to 1x1 size now! It is easier to fit them onto trucks now!
        #Rotating now: (They are rotated regardless of whether we crush)

            for i in range(len(boxes)):
                length = boxes[i][1]
                width = boxes[i][2]

                boxes[i][1], boxes[i][2] = width, length

        ###END CODE FOR EXTRA CREDIT.
        #########################################################

            

        unpackedBoxes = []

        #packing now:
        for box in boxes:
            if not self.packBox(box):
                unpackedBoxes.append(box)
                
        self.boxes = copy.deepcopy(boxes)
        return unpackedBoxes


    def writeTruckToCSV(self):
        f = open('truckview.csv','w')
        csvWriter = csv.writer(f)

        for row in self.truck:
            csvWriter.writerow(row)
        f.close()


    def packNSaveClicked(self):
        readyToGo = False
        stillGood = False
        
        try:
            int(self.truckWidth.get())
            int(self.truckLength.get())
            if self.radioSignal.get() != 0: #I'm pretty sure 0 is an IntVar's default value...
                readyToGo = True
        except:
            pass
            
        if readyToGo:
            self.initializeTruck()
            try:
                self.readBoxesFile()
                stillGood = True
            except:
                messagebox.showerror(message="Invalid CSV File")
                
            if stillGood:
                leftovers = self.packTruck()
                self.writeTruckToCSV()

                #Getting ready to do some counting for the statistics:       
                truckSize = 0
                filledCells = 0
                
                #Statistics:
                for y in range(len(self.truck)):
                    for x in range(len(self.truck[0])):
                        truckSize+=1
                        if self.truck[y][x] != '':
                            filledCells+=1

                percentTruckFilled = filledCells/truckSize*100
                percentBoxesPacked = ((len(self.boxes)-len(leftovers))/len(self.boxes))*100
                
                #New GUI Elements:
                Label(self.master, text='Packing Statistics').grid(row=6,column=0,columnspan=4)
                bottomFrame = Frame(self.master)
                bottomFrame.grid(row=7,column=0,columnspan=4,sticky=W+E)

                frameLeft = Frame(bottomFrame)
                frameLeft.grid(row=0,column=0,sticky=W,padx=5)
                
                #To put empty space between: (this is the only way I could figure out how to do it lol)
                frameMid = Frame(bottomFrame)
                frameMid.grid(row=0,column=1,padx=190)

                frameRight = Frame(bottomFrame)
                frameRight.grid(row=0,column=2,sticky=E)

                l1 = Label(frameLeft, text='Percent of Boxes Packed: {0:.1f}%'.format(percentBoxesPacked))
                l2 = Label(frameLeft, text='Percent of Truck Filled: {0:.1f}%'.format(percentTruckFilled))
                l1.pack(anchor=E);l2.pack(anchor=E);

                Label(frameRight, text='Boxes not packed:').pack()
                for box in leftovers:
                    Label(frameRight, text=box[0]).pack()
            
        else:
            messagebox.showinfo(message="Ensure that truck dimensions are valid integers and that a packing algorithm is selected")


a = Tk()
anApp = App(a)
a.title("HW6: Box Packer")
a.mainloop()


