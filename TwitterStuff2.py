import pandas as pd
import matplotlib.pyplot as plt


def InitBins( df, bins, interval ):
	days = []
	for tweet in df.itertuples():
		day = int(tweet.Time.split(",")[0])
		if day not in days:
			days.append(day)

	days.sort()
	for i in range(len(days)-1):
		diff = abs(days[i]-days[i+1])
		if diff != 1:
			print(days[i], days[i+1])
			for j in range(days[i]+1, days[i+1]):
				days.insert(i+(j-days[i]), j)
	#days.sort()

	for day in days:
		for i in range(0,24):
			for j in range(0, 60, interval):
				bins[(day, i, j)] = 0


def CalculateTimeHist( df, bins, interval ):
	for tweet in df.itertuples():
		time = tweet.Time.split(",")[1].split(":")
		day = int(tweet.Time.split(",")[0])
		hour = int(time[0])
		minutes  = (int(time[1])//interval)*interval
		bins[(day, hour, minutes)] += 1
	
	'''
	binsToDelete = []
	for key in bins:
		if bins[key] == 0:
			binsToDelete.append(key)
	for key in binsToDelete:
		del bins[key]
	'''

def Gradient( bins ):
	grad = []
	values = list(bins.values())
	for i in range(len(values)-1):
		grad.append(values[i+1]-values[i])
	return grad

	
if __name__ == '__main__':
	file = "TechBreakup.csv"
	df = pd.read_csv(file)
	bins = {}
	interval = 10

	print(df.head(10))

	InitBins( df, bins, interval )
	CalculateTimeHist( df, bins, interval )
	grad = Gradient( bins )

	keys = [ str(i) for i in bins.keys()]
	ax = plt.axes()
	ax.xaxis.set_major_locator(plt.MaxNLocator(10))
	ax.bar(keys, bins.values())
	plt.show()