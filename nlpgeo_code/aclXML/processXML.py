from utils.gMapsQuery import getCoordsfromName
from utils.pdfExtract import getDomain, getLocation

# Reading research data from ACL Anthology XML (https://github.com/acl-org/acl-anthology/tree/master/data/xml)
# Tested on version from 17.02.2021

def readPapersInVolume(volume, fileName):
    results = []
    for paper in volume.iter('paper'):
        acceptedAuthor = '?'
        lastName = '?'
        for author in paper.findall('author'):
            firstA = author.find('first')
            lastA = author.find('last')
            acceptedAuthor = ''
            if (firstA is not None) and (firstA.text is not None):
                acceptedAuthor = acceptedAuthor + firstA.text + ' '
            if (lastA is not None) and (lastA.text is not None):
                acceptedAuthor = acceptedAuthor + lastA.text
                lastName = lastA.text
            acceptedAuthor = acceptedAuthor.strip()
            if acceptedAuthor == '':
                acceptedAuthor = '?'
            break
        if paper.find('url') is not None:
            paperId = paper.find('url').text
        else:
            if volume.attrib['id'].isnumeric() and paper.attrib['id'].isnumeric():
                paperId = fileName.split('.')[0] + '-' + str(
                    1000 * int(volume.attrib['id']) + int(paper.attrib['id']))
            else:
                continue
        domain = getDomain(paperId)
        locationText, coords = getLocation(paperId, lastName)
        result = (paperId, acceptedAuthor, domain, locationText, coords[0],coords[1])
        results.append(result)
        print(result)
    return (results)


def readVolumeMeta(volume,fileName):
    confName = ''
    confYear = '?'
    confPlace = '?'
    confCoords = (0, 0)
    volumeId='?'
    if 'id' in volume.attrib:
        volumeId=fileName.replace('.xml','')+'.'+volume.attrib['id']
    for text in volume.find('meta').find('booktitle').itertext():
        confName = confName + text
    if volume.find('meta').find('year') is not None:
        confYear = volume.find('meta').find('year').text
    if volume.find('meta').find('address') is not None:
        confPlace = volume.find('meta').find('address').text
        confCoords = getCoordsfromName(confPlace)
    result = (volumeId,confName, confYear, confPlace, confCoords[0],confCoords[1])
    print(result)
    return (result)
