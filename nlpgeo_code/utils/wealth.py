wealthCache = {}



def initWealth(wealthPath):
    for line in open(wealthPath):
        parts=line.strip().split('\t')
        wealthCache[parts[0]]=float(parts[1])

def getWealth(country):
    return wealthCache[country]