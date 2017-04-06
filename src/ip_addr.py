my_dict = {}
result = {}

infile = open("log.txt")
for line in infile:
    #line = line.strip() 
    #parts = [p.strip() for p in line.split("\t")]
    parts = [p for p in line.split("- -")]
    if parts[0] in my_dict:
    	my_dict[parts[0]] += 1
    else:
    	my_dict[parts[0]] = 1
    #print line

for key in sorted(my_dict, key=lambda k: my_dict[k], reverse=True)[0:9]:
	print key + ','+str(my_dict[key]) + '\n'



