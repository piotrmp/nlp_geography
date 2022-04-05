import numpy as np

# Replace the location with the most popular one for this affiliation
from utils.gMapsQuery import initGeo, getCoordsfromName

dataPath = './'
cachePath = './'
initGeo(cachePath)

papers = np.loadtxt(dataPath + 'papers.tsv', delimiter='\t', comments=None, dtype=str)
volumes = np.loadtxt(dataPath + 'volumes.tsv', delimiter='\t', comments=None, dtype=str)

venues = {}

for line in open(dataPath + 'venues-ref.tsv'):
    parts = line.split('\t')
    venues[parts[0]] = (parts[1], parts[2])

for i in range(volumes.shape[0]):
    fileId = volumes[i, 0][0:volumes[i, 0].rfind('.')]
    year = volumes[i, 2]
    location = volumes[i, 3]
    if year == '?':
        year = venues[fileId][0]
    if ('online' in location.lower()) or ('virtual' in location.lower()):
        location = '@'
    elif venues[fileId][1] == '@':
        location = '@'
    elif location == '?':
        location = venues[fileId][1]
    volumes[i, 2] = year
    volumes[i, 3] = location
np.savetxt(dataPath + 'volumes-ref.tsv',volumes, delimiter='\t', fmt="%s", encoding='utf-8')

affiliations = np.unique(papers[:, 3])
for affiliation in affiliations:
    print(affiliation)
    hereLocations = papers[papers[:, 3] == affiliation, 4]
    hereLocations = hereLocations[hereLocations != '']
    if affiliation != '?' and len(hereLocations) == 0:
        defaultLocation = '?'
        defaultC1, defaultC2 = (0, 0)
    else:
        locations, pos = np.unique(hereLocations, return_inverse=True)
        bestPos = np.bincount(pos).argmax()
        defaultLocation = locations[bestPos]
        defaultC1, defaultC2 = getCoordsfromName(defaultLocation)
    toFill = np.logical_and(papers[:, 3] == affiliation, papers[:, 4] == '')
    papers[toFill, 4] = defaultLocation
    papers[toFill, 5] = defaultC1
    papers[toFill, 6] = defaultC2

np.savetxt(dataPath + 'papers-ref.tsv', papers, delimiter='\t', fmt="%s", encoding='utf-8')
