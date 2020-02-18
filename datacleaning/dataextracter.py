import csv

f = open("fundamentals.csv","r")
reader = csv.reader(f)
data = []
for line in reader:
    data.append(line)
f.close()

msft = []

for x in data:
    if x[0] == "MSFT":
        msft.append(x)

f = open("msft.csv","w")
writer = csv.writer(f)
for each in msft:
    writer.writerow(each)

f.close()
