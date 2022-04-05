import os, pickle, googlemaps

# Obtaining location names and coordinates using Google Maps API (you will need a key)
geoCachePath = None
geoCache = {}
gmaps = None
googleMapsAPIkey='INSERT_YOUR_API_KEY_HERE'

def initGeo(cachePath):
    global geoCachePath, geoCache, gmaps
    geoCachePath = cachePath + 'geoCache.bin'
    if os.path.exists(geoCachePath):
        cacheFile = open(geoCachePath, 'rb')
        geoCache = pickle.load(cacheFile)
        cacheFile.close()
        print("Loaded " + str(len(geoCache)) + " cached geographical names.")
    else:
        exit(0)
    gmaps = googlemaps.Client(key=googleMapsAPIkey)


def getCoordsfromName(locationText):
    if 'virtual' in locationText.lower() or 'online' in locationText.lower() or locationText in ['?', '@']:
        return (0, 0)
    location = getLocationfromName(locationText)
    result = (0, 0)
    if len(location) > 0:
        result = (location[0]['geometry']['location']['lat'], location[0]['geometry']['location']['lng'])
    return result


def getLocationfromName(locationText):
    if locationText in geoCache:
        # print("Location for '" + locationText + "' known, retrieving.")
        location = geoCache[locationText]
    else:
        print("Location for '" + locationText + "' unknown, querying.")
        location = gmaps.geocode(locationText)
        #print(location)
        geoCache[locationText] = location
        if len(geoCache) % 10 == 0:
            print("Writing geo cache.")
            cacheFile = open(geoCachePath, 'wb')
            pickle.dump(geoCache, cacheFile)
            cacheFile.close()
    return location
