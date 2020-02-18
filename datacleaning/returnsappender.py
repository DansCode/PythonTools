import csv

f = open("data.csv","r")
reader = csv.reader(f)
data = []
for line in reader:
    data.append(line)
f.close()

data[0].append("Returns")
data[1].append("")

for i in range(len(data)):
    if i > 1:
        closetoday = float(data[i][4])
        closeyesterday = float(data[i-1][4])
        data[i].append(str(
            (closetoday-closeyesterday)/closeyesterday
            ))

    




f = open("projectdata.csv","w")
writer = csv.writer(f)
for each in data:
    writer.writerow(each)
f.close()
