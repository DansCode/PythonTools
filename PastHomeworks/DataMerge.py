
from tkinter import *
import urllib.request
import re
import csv


class HW8:
    def __init__(self, master):
        ###VARS:
        self.taxDir = StringVar()
        self.unmatchDir = StringVar()

        self.taxNum = StringVar()
        self.unmatchNum = StringVar()
        
        self.directions = ('n','s','e','w','nw','ne','sw','se','north','south','east','west','northeast','northwest','southeast','southwest','n.','s.','e.','w.','nw.','ne.','sw.','se.')
        self.roads = ('ave','ave.','avenue','blvd','boulevard','ct','ct.','court','ln','ln.','lane','rd','rd.','road','st','st.','street','way')

        self.north = ('n','n.','north')
        self.south = ('s','s.','south')
        self.east = ('e','e.','east')
        self.west = ('w','w.','west')
        self.nw = ('nw','nw.','northwest')
        self.ne = ('ne','ne.','northeast')
        self.sw = ('sw','sw.','southwest')
        self.se = ('se','se.','southeast')

        self.ave = ('ave','ave.','avenue')
        self.blvd = ('blvd','boulevard')
        self.ct = ('ct','ct.','court')
        self.ln = ('ln','ln.','lane')
        self.rd = ('rd','rd.','road')
        self.st = ('st','st.','street')
        self.way = ('way')
        
        
        self.testFlag = False #a debugging tool of mine. You can safely ignore this.
        #notes:
        #self.propertiesData is defined in a method below. It's a list of lists
        #                    containing data from the input csv.
        #self.cityData, if the site is successfully scraped, will be the list of
        #               lists containing the rows from the city's properties table.
        #self.cityDataFormatted is cityData formatted like propertiesData. Defined in convertCityToMortgageFormat.
        #
        #self.unmatched    A list of unmatched records. Contains records from either propertiesData or cityDataFormatted.
        #
        #self.versionNum   The version number of the input csv file.
        #self.path         path our program works in. Same directory as the input file.
        ########
        
        #Master window: accessible throughout the object
        self.master = master
        
        #Button:
        self.loadButton = Button(self.master, text='Load Properties File', command=self.clicked)
        self.loadButton.grid(row=0,column=0,columnspan=3, sticky=W+E)

        #Labels:
        Label(self.master, text='Tax Data').grid(row=2, column=0)
        Label(self.master, text='Unmatched').grid(row=3, column=0)

        Label(self.master, text='Output Filename').grid(row=1,column=1)
        Label(self.master, text='# of Records').grid(row=1, column=2)

        #Entries:
        self.taxDataEntry = Entry(self.master, textvariable=self.taxDir, width=60)
        self.unmatchDataEntry = Entry(self.master, textvariable=self.unmatchDir, width=60)
        self.taxDataEntry.grid(row=2, column=1)
        self.unmatchDataEntry.grid(row=3, column=1)

        self.taxNumEntry = Entry(self.master, textvariable=self.taxNum, width=15)
        self.unmatchNumEntry = Entry(self.master, textvariable=self.unmatchNum, width=15)
        self.taxNumEntry.grid(row=2, column=2)
        self.unmatchNumEntry.grid(row=3,column=2)

        self.taxDataEntry['state']='readonly'
        self.unmatchDataEntry['state']='readonly'
        self.taxNumEntry['state']='readonly'
        self.unmatchNumEntry['state']='readonly'
        

    def clicked(self):
        filename = filedialog.askopenfilename()

        if self.loadPropertyFile(filename): #the method used here returns a boolean value
            keepGoing = True
            
            try: #scraping...
                self.downloadCityData('http://www.cc.gatech.edu/classes/AY2012/cs2316_spring/hw/hopeulikit-030112.html')
            except: #if the download fails:
                messagebox.showerror(title='Download Failed', message='The scraping of the table on the given page was unsuccessful.')
                keepGoing = False
            
            if keepGoing:    
                try:
                    self.convertCityToMortgageFormat()
                except:
                    messagebox.showerror(title='Data Conversion Failed', message="There was an error in converting the format of the city's data.")
                    keepGoing = False
                    
            if keepGoing:
                try:
                    self.mergeData()
                except:
                    messagebox.showerror(title='Data Merge Failed', message="Unable to Merge Data.")
                    keepGoing = False
                    
            if keepGoing:
                try:
                    self.saveTaxData()
                    self.saveNonMatchedData()
                except:
                    messagebox.showerror(title='Data Save Failed', message="Unable to save Data.")
                
        else:
            messagebox.showerror(title='File Error', message='Invalid filename OR file contains invalid data')
        

    #############HTML PARSER FROM DMSI COURSE NOTES: (All intact/No changes)
    #from http://www.summet.com/dmsi/html/readingTheWeb.html
    def parseTable(self, html):
        #Each "row" of the HTML table will be a list, and the items
        #in that list will be the TD data items.
        ourTable = []

        #We keep these set to NONE when not actively building a
        #row of data or a data item.
        ourTD = None    #Stores one table data item
        ourTR = None    #List to store each of the TD items in.


        #State we keep track of
        inTable = False
        inTR = False
        inTD = False

        #Start looking for a start tag at the beginning!
        tagStart = html.find("<", 0)

        while( tagStart != -1):
            tagEnd = html.find(">", tagStart)

            if tagEnd == -1:    #We are done, return the data!
                return ourTable

            tagText = html[tagStart+1:tagEnd]

            #only look at the text immediately following the <
            tagList = tagText.split()
            tag = tagList[0]
            tag = tag.lower()

            #Watch out for TABLE (start/stop) tags!
            if tag == "table":      #We entered the table!
                inTable = True
            if tag == "/table":     #We exited a table.
                inTable = False

            #Detect/Handle Table Rows (TR's)
            if tag == "tr":
                inTR = True
                ourTR = []      #Started a new Table Row!

            #If we are at the end of a row, add the data we collected
            #so far to the main list of table data.
            if tag == "/tr":
                inTR = False
                ourTable.append(ourTR)
                ourTR = None

            #We are starting a Data item!
            if tag== "td":
                inTD = True
                ourTD = ""      #Start with an empty item!
                
            #We are ending a data item!
            if tag == "/td":
                inTD = False
                if ourTD != None and ourTR != None:
                    cleanedTD = ourTD.strip()   #Remove extra spaces
                    ourTR.append( ourTD.strip() )
                ourTD = None
                

            #Look for the NEXT start tag. Anything between the current
            #end tag and the next Start Tag is potential data!
            tagStart = html.find("<", tagEnd+1)
            
            #If we are in a Table, and in a Row and also in a TD,
            # Save anything that's not a tag! (between tags)
            #
            #Note that this may happen multiple times if the table
            #data has tags inside of it!
            #e.g. <td>some <b>bold</b> text</td>
            #
            #Because of this, we need to be sure to put a space between each
            #item that may have tags separating them. We remove any extra
            #spaces (above) before we append the ourTD data to the ourTR list.
            if inTable and inTR and inTD:
                ourTD = ourTD + html[tagEnd+1:tagStart] + " "
                #print("td:", ourTD)   #for debugging


        #If we end the while loop looking for the next start tag, we
        #are done, return ourTable of data.
        return(ourTable)


    def downloadCityData(self, url):
        #This method uses the table scraper from the DMSI course notes.
        page = urllib.request.urlopen(url)
        html = str(page.read())
        page.close()

        self.cityData = self.parseTable(html)
        #self.cityData is now a list of lists, where each is a row of the table.


    def convertCityToMortgageFormat(self):
        #self.cityData = [ID, Address, Tax Rate]
        #                 (looks like)
        self.cityDataFormatted = []

        #The first list in cityData is literally ['ID','Address','Tax Rate']
        #Not useful, so we start indexing at 1:
        for i in range(1,len(self.cityData)):
            scratch = []
            address = self.cityData[i][1]
            tax = self.cityData[i][2]
            
            #I'll use capture groups to get the info I want:
            pattern = r'(\d{3,4})(.+)\\n\s?([a-zA-Z]*)\s?([A-Z]{2})\s?(\d+)'
            tup1 = re.findall(pattern,address)[0]
            #tup1 looks like: ('1234', 'DIR? Street-Name RD?', 'Hopeulikit', 'GA', '30461')

            street = tup1[1].strip() #stripping whitespace off the sides.
            direction = ''
            road = ''
            
            #checking the front and back of the street for those magic words (N,S, street, blvd, etc...): 
            flagFront = False #this is a flag that indicated we found a magic word in front
            flagBack = False #" "
            
            forwardIdx=None
            for idx in range(len(street)): #the street string is stripped of white spaces on the sides.
                if street[idx] == ' ': #any remaining white space in the string would signal the presence of
                    forwardIdx = idx   #more than one word, which in turn signals the possibility of there being
                    break              #a direction here in the front of the string.
                
            backwardIdx=None
            for idx in range(len(street)-1,-1,-1):
                if street[idx] == ' ': #same idea, except for road types in the back.
                    backwardIdx = idx + 1
                    break

            #if self.testFlag:
                #self.testFlag = False
                #print(backwardIdx)

            if forwardIdx != None: #This being None would mean there's no direction in the address.
                if street[0:forwardIdx].lower() in self.directions:
                    direction = street[0:forwardIdx]
                    flagFront = True

            if backwardIdx != None: #"...^"
                if street[backwardIdx:].lower() in self.roads: 
                    road = street[backwardIdx:]
                    flagBack = True


            #Now we slice and dice the street string accordingly:
            if flagBack:
                street = street[0:backwardIdx-1] #because backwardIdx is the index of the char after the last space.
            #It's important that the back is sliced off first, else funky stuff happens with the indexing.
            
            if flagFront:
                street = street[forwardIdx+1:] #because forwardIdx is the index of the first space.

            #remember tup1 looks like: ('1234', 'DIR? Street-Name RD?', 'Hopeulikit', 'GA', '30461')
            #So we'll append to scratch in a corresponding order:
            scratch.append(tup1[0])
            scratch.append(direction)
            scratch.append(street)
            scratch.append(road)
            scratch.append(tup1[2])
            scratch.append(tup1[3])
            scratch.append(tup1[4])
            scratch.append(tax)

            self.cityDataFormatted.append(scratch)
            #This list is now all the city data -formatted just like the mortgage company's.
            
        
    def loadPropertyFile(self, filename): #Returns False if load is unsuccessful.
        #This, if everything goes well, will have the data from
        #the csv that the company provides.
        self.propertiesData = []
        
        try:
            #A valid file is named 'properties-######.csv'
            #That should be the last 20 characters of whatever
            #string is passed in. If it's not, then we don't have a
            #path to a valid file. I'll use regex to check:
            aSliceOfTheFileName = filename[len(filename)-21:len(filename)]
            #          should   = 'properties-######.csv'

            if not re.match(r'properties-[0-9]{6}\.csv', aSliceOfTheFileName):
                #re.match returns a match object if there is a match.
                #Else, it returns None
                #Match objects have a boolean value of True
                raise ValueError
            
            f = open(filename, 'r')
            csvReader = csv.reader(f)

            for line in csvReader:
                if len(line) != 7:
                    #Each line in a valid file would have 7 items.
                    raise ValueError
                self.propertiesData.append(line)

            f.close()
            
            #Grabbing some data that we will need later:
            self.path = filename[0:len(filename)-21]
            self.versionNum = filename[-10:-4]
            
            return True
        
        except:
            return False


    def mergeData(self):
        self.calculateMatchScore()
        #note: calulateMatchScore defines self.unmatched
        #Inadvertently, calculateMatchScore was made to have some (most) of
        #the functionality that mergeData should have had (explicitly). Oops. Oh well.
        
        ####CONTINUING where calculateMatchScore left off:
        #Again, at this point, the plan is:
        #-append an empty string to all of the company's records that don't have tax data.
        #-using the remaining information in self.cityDic, populate self.unmatched,
        # prepping the data for export to CSV.

        for i in range(len(self.propertiesData)):
            if len(self.propertiesData[i]) != 8:
                self.propertiesData[i].append("")

        for key in self.cityDic.keys():
            for remainingCityData in self.cityDic[key]:
                self.unmatched.append(self.cityDataFormatted[remainingCityData])


    def calculateMatchScore(self):

        
        def makeScore(record, cityRecord): #A local helper function that'll make the code easier to read further down.
            score = 0
            
            #Matching street name:
            if record[2] == cityRecord[2]:
                score += 6
                
            dirScore = 2 #making it easy to adjust these:
            #Matching direction:
            if record[1].lower() in self.north and cityRecord[1].lower() in self.north:
                score += dirScore
            elif record[1].lower() in self.south and cityRecord[1].lower() in self.south:
                score += dirScore
            elif record[1].lower() in self.east and cityRecord[1].lower() in self.east:
                score += dirScore
            elif record[1].lower() in self.west and cityRecord[1].lower() in self.west:
                score += dirScore
            elif record[1].lower() in self.ne and cityRecord[1].lower() in self.ne:
                score += dirScore
            elif record[1].lower() in self.nw and cityRecord[1].lower() in self.nw:
                score += dirScore
            elif record[1].lower() in self.se and cityRecord[1].lower() in self.se:
                score += dirScore
            elif record[1].lower() in self.sw and cityRecord[1].lower() in self.sw:
                score += dirScore
            elif record[1] == '' and cityRecord[1] == '': #"no data is preferable to wrong data"
                score += dirScore
            elif cityRecord[1] == '': #Ambiguity is likeable. Just not as likeable as completely correct data.
                score += dirScore-1
                
            streetScore = 3
            #Matching street types:
            if record[3].lower() in self.ave and cityRecord[3].lower() in self.ave:
                score += streetScore
            elif record[3].lower() in self.blvd and cityRecord[3].lower() in self.blvd:
                score += streetScore
            elif record[3].lower() in self.ct and cityRecord[3].lower() in self.ct:
                score += streetScore
            elif record[3].lower() in self.ln and cityRecord[3].lower() in self.ln:
                score += streetScore
            elif record[3].lower() in self.rd and cityRecord[3].lower() in self.rd:
                score += streetScore
            elif record[3].lower() in self.st and cityRecord[3].lower() in self.st:
                score += streetScore
            elif record[3].lower() in self.way and cityRecord[3].lower() in self.way:
                score += streetScore
            elif record[3] == '' and cityRecord[3] == '':
                score += streetScore
            elif cityRecord[3] == '':
                score += streetScore-1
                
            #Matching everything else:
            if record[4] == cityRecord[4]: #city
                score += 5
            if record[5] == cityRecord[5]: #state
                score += 5
            if record[6] == cityRecord[6]: #zip
                score += 5

            return score
            
        
        self.cityDic = {}
        self.propDic = {}
        self.unmatched = []

        #self.propertiesData
        #self.cityDataFormatted
        #
        ####Don't forget about those ^

        for i in range(len(self.cityDataFormatted)):
            #self.cityDataFormatted[i][0] = ['123','dir','name','road type','city','state','12313','tax']
            self.cityDic[self.cityDataFormatted[i][0]] = [] #giving each key/streetnumber an empty list as a default value.

        for i in range(len(self.cityDataFormatted)):
            self.cityDic[self.cityDataFormatted[i][0]].append(i)
            
        ###The chunk of code above 'initializes' cityDic.
        ###cityDic will have street numbers of city records
        ###as keys. The values will be lists containing the
        ###indices of cityDataFormatted which correspond to
        ###records having corresponding street numbers.

        for i in range(len(self.propertiesData)):
            self.propDic[self.propertiesData[i][0]] = []
        for i in range(len(self.propertiesData)):
            self.propDic[self.propertiesData[i][0]].append(i)

        ###Above, we do the same thing, but for self.propertiesData
        #Now a key-value pair in either dictionary looks like:
        # {index in list: street num of record}

        for streetNumber in self.propDic.keys():
            #Only if the streetNumber is in the city's
            #records do we even start to try matching.
            if streetNumber in self.cityDic.keys():
                
                indexesOfProperties = self.propDic[streetNumber]
                #Above is a list containing indexes of records in
                #self.propertiesData corresponding to
                #each streetNumber.
                indexesOfCityProperties = self.cityDic[streetNumber]
                #^^^^same idea^^^^#

                #Some notes, mostly to myself:
                #Each self.cityDataFormatted[runnerUpIndex] aka cityRecord looks like:
                #['1234', 'DIR', 'Street-Name', 'RD', 'Hopeulikit', 'GA', '30461', 'tax']
                
                for anIndex in indexesOfProperties:
                    bestMatchForProperty = None
                    record = self.propertiesData[anIndex]
                    hiScore = 0
            
                    for anotherIndex in indexesOfCityProperties:
                        cityRecord = self.cityDataFormatted[anotherIndex]

                        score = makeScore(record, cityRecord)
                        
                        if score > 20: #<<<- SCORE THRESHOLD, is right here in this line.
                            if score > hiScore:
                                bestMatchForProperty = cityRecord
                                hiScore = score
                                matchIndex = indexesOfCityProperties.index(anotherIndex)
                                #Right here, I saved the index of anotherIndex in indexesOfCityProperties
                                #Doing so allows for the deletion of the saved anotherIndex out of
                                #the city data structure.
                                #Also, doing so is safe and reliable, because every index of a sequence
                                #is unique. The index method will not find more than one of what we are looking for.
                    
                    if bestMatchForProperty != None:
                        del indexesOfCityProperties[matchIndex]
                        record.append(bestMatchForProperty[7])

                if len(self.cityDic[streetNumber]) == 0: #if the street number has no more corresponding records
                    del self.cityDic[streetNumber]       #left to be compared... delete it out of the dictionary!

                #What all that code just did:
                #found a match for each property and appended tax data to each.
                #on every match, the corresponding reference to the city's record
                #was deleted out of cityDic.

                #What we have left now:
                #-self.cityDic with references to unmatched properties
                #-self.propertiesData with some of the records not having tax data appended to the end.

                #At this point, the plan is:
                #-append an empty string to all of the company's records that don't have tax data.
                #-using the remaining information in self.cityDic, populate self.unmatched,
                # prepping the data for export to CSV.

                #Gonna do all that in self.mergeData        
                

    def saveTaxData(self):
        filename = self.path + 'taxData-{0}.csv'.format(self.versionNum)
        f = open(filename, 'w')
        csvWriter = csv.writer(f)

        for record in self.propertiesData:
            record[7] = record[7].replace(',','') #removing commas
            record[7] = record[7].replace('$','') #removing any dollar sign
        
            csvWriter.writerow(record)
        f.close()

        self.taxDir.set(filename)
        self.taxNum.set(str(len(self.propertiesData)))


    def saveNonMatchedData(self):
        filename = self.path + 'non-matched-city-{0}.csv'.format(self.versionNum)
        f = open(filename, 'w')
        csvWriter = csv.writer(f)

        for record in self.unmatched:
            record[7] = record[7].replace(',','') #removing commas
            record[7] = record[7].replace('$','') #removing any dollar sign

        self.unmatched.sort() #sorting... I love this method. So much. <3... the sorting is textual, btw. As required.
            
        for record in self.unmatched:
            csvWriter.writerow(record)
        f.close()

        self.unmatchDir.set(filename)
        self.unmatchNum.set(str(len(self.unmatched)))


a = Tk()
a.title("Hopeulikit Mortgage Company - Data Merger")
app = HW8(a)
a.mainloop()


