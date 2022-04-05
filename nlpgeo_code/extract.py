import os
import xml.etree.ElementTree as ET
from aclXML.processXML import readVolumeMeta, readPapersInVolume
from utils.gMapsQuery import initGeo
from utils.pdfExtract import initPDF

aclXMLdir = '/PATH/TO/acl-anthology/data/xml/'
outDir='./'
cachePath='./'
initGeo(cachePath)
initPDF(cachePath)

# Harvesting
domains = {}
fileCounter = 1
allPapers=[]
allVolumes=[]
for fileName in os.listdir(aclXMLdir):
    print(
        '============= ' + fileName + ' ===== ' + str(fileCounter) + '/' + str(len(os.listdir(aclXMLdir))) + ' =============')
    fileCounter = fileCounter + 1
    if not fileName.endswith('.xml'):
        continue
    tree = ET.parse(aclXMLdir + fileName)
    root = tree.getroot()
    for volume in root.findall('volume'):
        volumeData = readVolumeMeta(volume,fileName)
        paperData = readPapersInVolume(volume, fileName)
        allVolumes.append(volumeData)
        for datum in paperData:
            allPapers.append((volumeData[0],)+datum)
    #break

# Output
output=open(outDir+'volumes.tsv','w')
for volumeData in allVolumes:
    output.write('\t'.join([str(d).replace('\n',' ').replace('\t',' ') for d in volumeData])+'\n')
output.close()
output=open(outDir+'papers.tsv','w')
for paperData in allPapers:
    output.write('\t'.join([str(d).replace('\n',' ') .replace('\t',' ') for d in paperData])+'\n')
output.close()
