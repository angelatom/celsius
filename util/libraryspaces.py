import json
import requests

key = "1933d3de-38d8-35ba-8880-f77c65b95b1b"
url = 'https://sandbox.api.it.nyu.edu/library-share-space-exp/spaces'
'''
def getSpaceInfo():
    url = 'https://sandbox.api.it.nyu.edu/library-share-space-exp/spaces'
    headers = {'Authorization': 'Bearer 1933d3de-38d8-35ba-8880-f77c65b95b1b'}
    parameters = {'location': 'West', 'floor': 9}
    req = requests.get(url, headers=headers, params=parameters)
    data = json.loads(req.text)
    return data

print(getSpaceInfo())
'''
def querySpaceInfo(floor = None, location = None, space_title = None, status = None, reservable = None, zone_description= None):
    url = 'https://sandbox.api.it.nyu.edu/library-share-space-exp/spaces'
    headers = {'Authorization': 'Bearer 1933d3de-38d8-35ba-8880-f77c65b95b1b'}
    parameters = {}
    if (floor != None):
        parameters['floor'] = floor
    if (location != None):
        parameters['location'] = location
    if (space_title != None):
        parameters['space_title'] = space_title
    if (status != None):
        parameters['status'] = status
    if (reservable != None):
        parameters['reservable'] = reservable
    if (zone_description != None):
        parameters['zone_description'] = zone_description
    req = requests.get(url, headers=headers, params=parameters)
    data = json.loads(req.text)
    return data

'''
return a list of study spot data (each element in the list is a study spot)
return 10 or all possible
'''
def getstudyspots(data):
    spots = []
    counter = 0
    for studyspot in data:
        spots.append(studyspot)
        counter += 1
        if counter > 10:
            break
    return spots

#print(getstudyspots(querySpaceInfo(floor = 9, location='West', reservable='No'))[0]['capacity'])

def getcapacity(studyspot):
    return studyspot['capacity']

def getreservable(studyspot):
    return studyspot['reservable']

def getzone(studyspot):
    return studyspot['zone']

def getspace_title(studyspot):
    return studyspot['space_title']

def getroom_number(studyspot):
    return studyspot['room_number']

def getstatus(studyspot):
    return studyspot['status']

def getfloor(studyspot):
    return studyspot['floor']

def getlocation(studyspot):
    return studyspot['location']

def getzone_description(studyspot):
    return studyspot['zone_description']