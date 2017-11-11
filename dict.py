import re

pattern = "([A-Z][0-9]{6}[A-Z][A-Z])"

def extractRoll(filename):
    fout = open("./dict.txt",'a')
    with open(filename) as fin:
        for line in fin:
            roll = re.search(pattern,line)
            if(roll is not None and roll.group(0) is not None):
                fout.write(roll.group(0) + "\n")

extractRoll("btech_hostel_due_10.txt")
extractRoll("PG.txt")
extractRoll("PhD.txt")
