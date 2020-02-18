import csv

def parseDate(datestring):
    ymd = datestring.split("-")
    year = int(ymd[0])
    month = int(ymd[1])
    day = int(ymd[2])

    return (year, month, day)

def isLater(firstDate,secondDate):
    yearCheck = firstDate[0] >= secondDate[0]
    monthCheck = firstDate[1] >= secondDate[1]
    dayCheck = firstDate[2] > secondDate[2]

    return yearCheck and monthCheck and dayCheck
    

f = open("MSFTfundamentals.csv","r")
reader = csv.reader(f)
data = []
for line in reader:
    data.append(line)
f.close()


d = {}

for line in data:
    if line[3] not in d.keys():
        d[line[3]] = []
        d[line[3]].append(line[4:])
    else:
        d[line[3]].append(line[4:])


f = open("MSFTpricevolume.csv","r")
reader = csv.reader(f)
data2 = []
for line in reader:
    data2.append(line)
f.close()



for key in d.keys():
    data2[0].append(key)
    values = d[key]

    for line in data2[1:]:
        line.append("")

    point = None
    for line in data2[1:]:
        datepv = parseDate(line[0])

        for each in values:
            datefun = parseDate(each[0])
            if datepv == datefun:
                point = each[1]

        line[-1] = point
            
        
        
f = open("data.csv","w")
writer = csv.writer(f)
for each in data2:
    writer.writerow(each)

f.close()
