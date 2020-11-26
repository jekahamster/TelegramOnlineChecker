import plotly.graph_objects as go 
from datetime import datetime as dt 
from datetime import timedelta as td


LOG_PATH = "log"

def strToDate(strDate):
	return dt.strptime(strDate, "%Y-%m-%d %H:%M:%S.%f")

def isBetween(d, d1, d2):
	return (d1 <= d) and (d <= d2)

def readData(path):
	with open(path, "r") as file: 
		data = []
		for row in file:
			data += [row.replace("\n", "")]

	return data


def formatUserData(data):
	out = []
	for row in data:
		separator1 = row.find("|")
		separator2 = row.find("|", separator1+1)
		separator3 = row.find("|", separator2+1)
		separator4 = row.find("|", separator3+1)

		name 	 = row[:separator1]
		status 	 = row[separator1+1:separator2].replace("Status:", "")
		lastSeen = row[separator2+1:separator3].replace("LastSeen:", "")
		until 	 = row[separator3+1:separator4].replace("Until:", "")
		date 	 = strToDate(row[separator4+1:].replace("Now:", ""))

		out += [{
			"name": name,
			"date": date
		}]

	return out

def formatLogData(data):
	out = []
	for row in data:
		separator = row.find("|")
		name = row[:separator]
		date = strToDate(row[separator+1:])

		out += [{
			"name": name,
			"date": date
		}]

	return out

def filterBetween(data, dstart, dstop):
	out = []
	for d in data:
		if isBetween(d["date"], dstart, dstop):
			out += [d]

	return out

def filterByName(data):
	out = {}
	for d in data:
		
		if d["name"] not in out:
			out[d["name"]] = []

		out[d["name"]] += [d["date"]]

	return out

def groupDate(userData):
	out = {}
	userData = userData.copy()

	minDate = None
	maxDate = None
	delta = td(minutes=10)

	for name in userData:
		if minDate is None:
			minDate = min(userData[name])
		if maxDate is None:
			maxDate = max(userData[name])

		tempMin = min(userData[name])
		minDate = min(tempMin, minDate)

		tempMax = max(userData[name])
		maxDate = max(tempMax, maxDate)


	for name in userData:
		currentDate = minDate
		userDate = userData[name]
		tempDate = []

		while userDate and currentDate <= maxDate:
			
			if isBetween(userDate[0], currentDate, currentDate + delta):
				tempDate += [currentDate]
				userDate.pop(0)

			elif (currentDate + delta < userDate[0]):
				currentDate += delta

		date = []
		count = []
		currentDate = minDate
		while currentDate <= maxDate:
			date += [currentDate]
			count += [tempDate.count(currentDate)]

			currentDate += delta

		out[name] = {
			"date": date,
			"count": count
		}

	return out

dateStart = dt(2020, 2, 23, 15, 10, 13, 0)
dateStop  = dt(2020, 2, 27, 7, 10, 13, 0)



strData 	= readData(LOG_PATH)
allData 	= formatLogData(strData)
allData 	= filterBetween(allData, dateStart, dateStop)
usersData 	= filterByName(allData)
usersData 	= groupDate(usersData)


for name in usersData:
	for i in range(len(usersData[name]["date"])):
		print(usersData[name]["date"][i], usersData[name]["count"][i])

fig = go.Figure()

for name in usersData:
	fig.add_trace(
		go.Scatter(name=name, x=[str(d) for d in usersData[name]["date"]], y=[c for c in usersData[name]["count"]])
	)
	
fig.show()