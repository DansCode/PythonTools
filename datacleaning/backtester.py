import csv
import math

f = open("projectdata.csv","r")
reader = csv.reader(f)
data = []
for line in reader:
    data.append(line)
f.close()

def isMonth(month,date):
    if month == "feb" and date[5:7] == "02":
        return 1
    elif month == "mar" and date[5:7] == "03":
        return 1
    elif month == "apr" and date[5:7] == "04":
        return 1
    elif month == "may" and date[5:7] == "05":
        return 1
    elif month == "jun" and date[5:7] == "06":
        return 1
    elif month == "jul" and date[5:7] == "07":
        return 1
    elif month == "aug" and date[5:7] == "08":
        return 1
    elif month == "sep" and date[5:7] == "09":
        return 1
    elif month == "oct" and date[5:7] == "10":
        return 1
    elif month == "nov" and date[5:7] == "11":
        return 1
    elif month == "dec" and date[5:7] == "12":
        return 1
    else:
        return 0
        

def fit(day):
    constant = 2.9047
    close = float(data[day-1][4]) #with delay 1
    avgrangeminusclose = (float(data[day-1][2])+float(data[day-1][3]))/2 - close #with delay 1
    closesquared = close**2
    avgsquared = avgrangeminusclose**2

    february = isMonth("feb",data[day][0])
    march = isMonth("mar",data[day][0])
    april = isMonth("apr",data[day][0])
    may = isMonth("may",data[day][0])
    june = isMonth("jun",data[day][0])
    july = isMonth("jul",data[day][0])
    august = isMonth("aug",data[day][0])
    september = isMonth("sep",data[day][0])
    october = isMonth("oct",data[day][0])
    november = isMonth("nov",data[day][0])
    december = isMonth("dec",data[day][0])


    out = (constant+
           .024284*close+
           .003746*avgrangeminusclose+
           .000073*closesquared+
           .001843*avgsquared+
           -.00052*february+
           -.00395*march+
           .00124*april+
           .00114*may+
           -.00121*june+
           .00369*july+
           .00446*september+
           .00232*october+
           .00135*november+
           -.00452*december)

    return out

rightcount = 0
totalcount = 0
i = 0
flag = False
for each in data:
    
    if each[0] == "2019-01-02":
        flag = True

    if flag:
        est = fit(i)
        close = float(each[4])
        closeyesterday = float(data[i-1][4])

        totalcount += 1

        if est-math.log(closeyesterday) > 0 and math.log(close)-math.log(closeyesterday) > 0:
            rightcount += 1
        elif est-math.log(closeyesterday) < 0 and math.log(close)-math.log(closeyesterday) < 0:
            rightcount += 1
        elif est-math.log(closeyesterday) == math.log(close)-math.log(closeyesterday):
            rightcount += 1

    i += 1


print(rightcount/totalcount)
