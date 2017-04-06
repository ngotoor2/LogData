import re
from datetime import datetime
import heapq

my_dict = {}
result = {}

pattern = re.compile('^(.*) - - \[(.*)\] "(.*)" (.*) (.*)$')
timestamp_pattern = re.compile('^(.*) -(.*)$')
timestamp_format = '%d/%b/%Y:%H:%M:%S'
infile = open("log.txt")

class Window():
	def __init__(self, beginTimestampIndex, allTimestamps):
		self.beginTime = allTimestamps[beginTimestampIndex]
		self.beginTimestampIndex = beginTimestampIndex
		self.windowExtent = -1
		self.allTimestamps = allTimestamps
		return

	def computeWindowExtent(self):
		remainingTimeStamps = len(self.allTimestamps) - self.beginTimestampIndex - 1
		#print str(remainingTimeStamps) + str(len(self.allTimestamps)) + str(self.beginTimestampIndex)
		if remainingTimeStamps == 0:
			self.windowExtent = 1
		else:
			self.windowExtent = self.getSegmentStopPoint(self.beginTimestampIndex, self.beginTimestampIndex, remainingTimeStamps) - self.beginTimestampIndex
#binary search

	def getSegmentStopPoint(self,windowStartIndex, segmentStartIndex, segmentSize):
		segmentEndIndex = segmentStartIndex + segmentSize - 1
		#print str(segmentStartIndex) + str(windowStartIndex) + str(segmentEndIndex)
		if self.getTimeStampsDiff(windowStartIndex, segmentEndIndex, 2) <= 60:
			return segmentEndIndex
		else:
			newSegmentSize = int(segmentSize/2)
			if newSegmentSize == 1:
				newsegmentStopPoint = segmentStartIndex + 1
			elif self.getTimeStampsDiff(windowStartIndex, segmentStartIndex + newSegmentSize, 2) <= 60:
				newsegmentStopPoint = self.getSegmentStopPoint(windowStartIndex, segmentStartIndex+newSegmentSize, newSegmentSize)
			else:
				newsegmentStopPoint = self.getSegmentStopPoint(windowStartIndex, segmentStartIndex, newSegmentSize)

			return newsegmentStopPoint


	def __cmp__(self, other):
		return cmp(self.windowExtent, other.windowExtent)

	def printWindow(self):
		#f1 =open('./resources','w+')
		#f1.write(' Frequency: ' + str(self.numberOfRequests) +' Begin time: ' + str(self.beginTime) )
		print ' Frequency: ' + str(self.windowExtent) +' Begin time: ' + str(self.beginTime) 

	def getTimeStampsDiff(self,timestampIndex1, timestampIndex2, type):
		timediff = self.allTimestamps[timestampIndex2] - self.allTimestamps[timestampIndex1]
		if type == 1:
			timediff_seconds = (timediff.days*24*60*60) + (timediff.seconds)
			return timediff_seconds
		elif type == 2:
			timediff_minutes = (timediff.days*24*60) + (timediff.seconds/60)
			return timediff_minutes

def getTimeStampsDiffInSec(timestamp1, timestamp2):
	timediff = timestamp2 - timestamp1
	timediff_seconds = (timediff.days*24*60*60) + (timediff.seconds)
	return timediff_seconds


def getTimeStampsDiffInMinutes(timestamp1, timestamp2):
	timediff = timestamp2 - timestamp1
	timediff_minutes = (timediff.days*24*60) + (timediff.seconds/60)
	return timediff_minutes

timestamps = []

linecounter = 0

for line in infile:
	lineparts = pattern.match(line).groups()
	timestamp_parts = timestamp_pattern.match(lineparts[1]).groups()
	timestamp = datetime.strptime(timestamp_parts[0], timestamp_format)
	timestamps.append(timestamp)
	linecounter += 1
	#test(increment the number to suit your data)works well for lines under 10000

	if linecounter >=10000000:
		break

print 'Timestamps loaded successfully'

heap = []
#heapy = heapq.heapify(heap)

prevTimestamp = ''
for request_index in range(0, len(timestamps)):

	beginTime = timestamps[request_index]
	count = 0
	if request_index ==0:
		prevTimestamp = timestamps[request_index]
	else:
		if getTimeStampsDiffInSec(timestamps[request_index], prevTimestamp) == 0:
			continue
		else:
			prevTimestamp = timestamps[request_index]

	window = Window(request_index, timestamps)
	window.computeWindowExtent()
		
	store = True
	for i in range(0, len(heap)):
		if getTimeStampsDiffInMinutes(heap[i].beginTime, window.beginTime) < 60:
			#print  str(window.beginTime) + ' ' + str(heap[i].beginTime) + ' ' + str(getTimeStampsDiffInMinutes(window.beginTime, heap[i].beginTime))
			store = False

	if store:
		heapq.heappush(heap, window)

	if len(heap) > 10:
		heapq.heappop(heap)
		

for window in heap:
	window.printWindow() 




