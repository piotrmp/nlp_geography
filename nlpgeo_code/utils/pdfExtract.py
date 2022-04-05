import os
import pickle
import re
import requests
import spacy
from fake_useragent import UserAgent
from fitz import fitz

# Getting PDFs from ACL anthology website and parsing to find the name, affiliation and location of the first author

from utils.gMapsQuery import getCoordsfromName

ValidHostnameRegex = "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)+([A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])"
ua = UserAgent()
expr = re.compile('@' + ValidHostnameRegex)
nlp = None
pdfTempPath = None
pdfCache = None
pdfCachePath = None


def initPDF(cachePath):
    global pdfCachePath, pdfTempPath, nlp, pdfCache
    pdfCachePath = cachePath + 'pdfCache.bin'
    pdfTempPath = cachePath + 'paper.pdf'
    nlp = spacy.load("en_core_web_trf")
    pdfCache = {}
    if os.path.exists(pdfCachePath):
        cacheFile = open(pdfCachePath, 'rb')
        pdfCache = pickle.load(cacheFile)
        cacheFile.close()
        print("Loaded " + str(len(pdfCache)) + " cached PDF documents.")
    else:
        exit(0)


def getTextFromWeb(paperId):
    if paperId.startswith("http://") or paperId.startswith("https://"):
        url = paperId
    else:
        url = 'https://www.aclweb.org/anthology/' + paperId + '.pdf'
    headers = {'User-Agent': ua.chrome}
    r = requests.get(url, headers=headers, allow_redirects=True)
    if r.status_code == 404:
        print("Got status: " + str(r.status_code) + " for " + url)
        return '<UNREADABLE>'
    if r.status_code != 200:
        print("Got status: " + str(r.status_code) + " for " + url)
        raise Exception("Unable to reach ACL Anthology.")
    file = open(pdfTempPath, 'wb')
    file.write(r.content)
    file.close()
    try:
        pdf = fitz.open(pdfTempPath)
        text = pdf.loadPage(0).getText()
        pdf.close()
    except RuntimeError as e:
        if e.args[0] in ["unknown encryption handler: 'Adobe.PPKLite'", "no objects found"]:
            text = '<UNREADABLE>'
        else:
            raise
    except ValueError as e:
        if e.args[0] == "page not in document":
            text = '<UNREADABLE>'
        else:
            raise
    return text


def getPaperText(paperId):
    if paperId in pdfCache:
        # print("Text for '" + paperId + "' known, retrieving.")
        text = pdfCache[paperId]
    else:
        # print("Text for '" + paperId + "' unknown, querying...")
        text = getTextFromWeb(paperId)
        pdfCache[paperId] = text
        if len(pdfCache) % 10 == 0:
            print("Writing PDF cache.")
            cacheFile = open(pdfCachePath, 'wb')
            pickle.dump(pdfCache, cacheFile)
            cacheFile.close()
    return text


def getDomain(paperId):
    text = getPaperText(paperId)
    text = text.replace("}", "").replace("{", "")
    match = expr.search(text)
    if match is None:
        return '?'
    domain = match.group(0).lower()
    if domain.startswith("@student."):
        domain = domain.replace("@student.", "@")
    if domain.startswith("@mymail."):
        domain = domain.replace("@mymail.", "@")
    if domain.startswith("@mail."):
        domain = domain.replace("@mail.", "@")
    if domain.startswith("@email."):
        domain = domain.replace("@email.", "@")
    if domain.startswith("@mails."):
        domain = domain.replace("@mails.", "@")
    if domain.startswith("@mail2."):
        domain = domain.replace("@mail2.", "@")
    if domain.startswith("@alumni."):
        domain = domain.replace("@alumni.", "@")
    if domain == '@gmail.com':
        domain = '?'
    return domain


def getLocation(paperId, lastName):
    text = getPaperText(paperId)
    searchStart = -1
    if lastName != '?':
        searchStart = text.find(lastName) + len(lastName)
    # print(paperId)
    # print(text)
    doc = nlp(text)
    locationStart = 0
    locationEnd = 0
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            if ent.start_char > searchStart:
                # print('GPE: '+ent.text)
                if locationStart == 0:
                    locationStart = ent.start_char
                    locationEnd = ent.end_char
                elif ent.start_char - locationEnd < 5:
                    locationEnd = ent.end_char
                else:
                    break
            else:
                # print("Skipping too early entity: " + ent.text)
                pass
    locationText = text[locationStart:locationEnd]
    # print('LOCATION: '+locationText)
    coords = (0, 0)
    if locationText != '':
        coords = getCoordsfromName(locationText)
    # print(locationText + ' ' + str(coords))
    return locationText, coords
