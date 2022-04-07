import numpy as np


dataPath = './'

papers = np.loadtxt(dataPath + 'papers.tsv', delimiter='\t', comments=None, dtype=str)
volumes = np.loadtxt(dataPath + 'volumes.tsv', delimiter='\t', comments=None, dtype=str)

venues = {}
for volume in volumes:
    volumeId=volume[0]
    fileId=volumeId[0:volumeId.rfind('.')]
    if fileId not in venues:
        venues[fileId]=([],[],volume[1])
    year=volume[2]
    location=volume[3]
    if ('online' in location.lower()) or ('virtual' in location.lower()) :
        location='@'
    venues[fileId][0].append(year)
    venues[fileId][1].append(location)

out=open(dataPath+'venues.tsv','w')
for venue in venues:
    out.write(venue)
    years, pos = np.unique(venues[venue][0], return_inverse=True)
    bestPos = np.bincount(pos).argmax()
    out.write('\t' + years[bestPos])
    locations, pos = np.unique(venues[venue][1], return_inverse=True)
    bestPos = np.bincount(pos).argmax()
    out.write('\t' + locations[bestPos])
    out.write('\t' + venues[venue][2])
    out.write('\n')
out.close()
