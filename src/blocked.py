import re
from datetime import datetime
import heapq

my_dict = {}
result = {}

pattern = re.compile('^(.*) - - \[(.*)\] "(.*)" (.*) (.*)$')
timestamp_pattern = re.compile('^(.*) -(.*)$')
timestamp_format = '%d/%b/%Y:%H:%M:%S'
infile = open("log.txt")

requests = []

linecounter = 0

for line in infile:
	request = {}
	lineparts = pattern.match(line).groups()

	request['i'] = lineparts[0]

	timestamp_parts = timestamp_pattern.match(lineparts[1]).groups()
	timestamp = datetime.strptime(timestamp_parts[0], timestamp_format)

	request['t'] = timestamp

	request['s'] = lineparts[3]

	requests.append(request)
	linecounter += 1
	#test(increment the number to suit your data)works well for lines under 10000

	if linecounter >10000000:
		break

print 'Requests loaded successfully'

checkableIps = {}
blockedIps = {}

def getTimeStampsDiffInSec(timestamp1, timestamp2):
	timediff = timestamp2 - timestamp1
	timediff_seconds = (timediff.days*24*60*60) + (timediff.seconds)
	return abs(timediff_seconds)

def getTimeStampsDiffInMinutes(timestamp1, timestamp2):
	timediff = timestamp2 - timestamp1
	timediff_minutes = (timediff.days*24*60) + (timediff.seconds/60)
	return abs(timediff_minutes)

def cleanTimestamps(timestamps, newTimestamp):
	for i in range(0, len(timestamps)):
		if getTimeStampsDiffInSec(timestamps[i], newTimestamp) > 20:
			timestamps.pop(i)

def cleanBlockedIps(blockedips, newTimestamp):
	for ip, timestamp in blockedips.items():
		if getTimeStampsDiffInMinutes(timestamp, newTimestamp) > 5:
			blockedips.pop(ip, None)

for request_index in range(0, len(requests)):
	req = requests[request_index]
	#status = "401"
	cleanBlockedIps(blockedIps, req['t'])

	if req['i'] in blockedIps:
		print 'Blocked: ' + req['i'] + ' ' + str(req['t']) + ' ' + req['s']
		continue

	if int(req['s']) == 401:
		if req['i'] not in checkableIps:
			checkableIps[req['i']] = [req['t']]
		else:
			cleanTimestamps(checkableIps[req['i']], req['t'])
			checkableIps[req['i']].append(req['t'])
			if len(checkableIps[req['i']]) == 3:
				if req['i'] not in blockedIps:
					blockedIps[req['i']] = req['t']
					checkableIps[req['i']] = []






