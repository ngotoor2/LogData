import re

my_dict = {}
result = {}

pattern = re.compile('^(.*) - - \[(.*)\] "(.*)" (.*) (.*)$')

infile = open("log.txt")
for line in infile:
	parts = pattern.match(line).groups()
	httpRequestPath = parts[2].split(' ')
	val = 0
    #print ' L: ' + line + '\n'
    #print ' M: ' + ''.join(parts.groups()) + '\n'
	if len(httpRequestPath) < 2 or not (parts[4].isdigit()):
		#print httpRequestPath
		#print ' L: ' + line + '\n'
		continue
    
	if httpRequestPath[1] not in my_dict:
		try:
			size = parts[4]
			my_dict[httpRequestPath[1]] = {'b': int(size), 'f':1}
		except KeyError:
			print 'L: ' + line + '\n'
		except ValueError:
			print 'L: ' + line + '\n' 
			print parts[4]
	else:
		my_dict[httpRequestPath[1]]['f'] += 1
		my_dict[httpRequestPath[1]]['b'] += int(size)


#sorting based on the product of the bandwidth=bytes*frequency


for key in sorted(my_dict, key=lambda k: my_dict[k]['b']*my_dict[k]['f'], reverse=True)[0:9]:
	#print key + ' ' + str(my_dict[key]) + '\n'
		print key + ' '  
	#f1 = open('./hours.txt','w+')
	#f1.write(key + ' '  + '\n')



