import os
import string
import requests
import urllib.parse

def getBingResponse(zipCode):
    '''Get's Bing API Response from a Zip Code Location Query'''
    apiKey = os.environ['BING_API_KEY']
    payload = f'http://dev.virtualearth.net/REST/v1/Locations/{zipCode}?maxResults=1&key={apiKey}'
    return requests.get(payload)

def findCoordinates(bingResponse):
    '''Returns the Coordinates of a ZIP code from a Bing Response Object'''
    r = bingResponse.json()
    return r['resourceSets'][0]['resources'][0]['geocodePoints'][0]['coordinates']

def getCoordinates(ZIP):
    '''Convience function to return lat and long from a ZIP Code.'''
    return findCoordinates(getBingResponse(ZIP))

def getCostcoAJAX(coord, maxResponse=10):
    '''Return the Costco AJAX Response for a pair of coordinates.'''
    lat = coord[0]
    lon = coord[1]
    print("Sending Request to Costco AJAX")
    s = requests.Session()
    headers = {'referer': 'http://www.costco.com/warehouse-locations', 'Referrer-Policy': 'no-referrer', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "0","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    payload = f'http://www.costco.com/AjaxWarehouseBrowseLookupView?langId=-1&storeId=10301&numOfWarehouses={maxResponse}&hasGas=false&hasTires=false&hasFood=false&hasHearing=false&hasPharmacy=false&hasOptical=false&hasBusiness=false&hasPhotoCenter=false&tiresCheckout=0&isTransferWarehouse=false&populateWarehouseDetails=true&warehousePickupCheckout=false&latitude={lat}&longitude={lon}&countryCode=US'
    s.get('https://google.com', headers=headers)
    return s.get(payload, headers=headers)

class CostcoLocation:
    def __init__(self, ajax):
        self.locationID = ajax['locationName']
        self.streetAddress = string.capwords(ajax['address1'])
        self.city = string.capwords(ajax['city'])
        self.state = ajax['state']
        zipCode = ajax['zipCode'].split('-')
        self.zip = zipCode[0]
        try:
            self.gasPrices(ajax['gasPrices'])
            self.gasHours(ajax['gasStationHours'])
        except KeyError:
            self.gas = False
        self.formatAddress()

    def gasPrices(self, gasAjax):
        self.gas = True
        self.regular = gasAjax['regular'][:-1]
        self.premium = gasAjax['premium'][:-1]

    def gasHours(self, hoursAjax):
        self.weekdays = self.formatHours(hoursAjax[0]['time'])
        self.saturday = self.formatHours(hoursAjax[1]['time'])
        self.sunday = self.formatHours(hoursAjax[2]['time'])
    
    def formatHours(self, hours):
        time = hours.split('-')
        return (time[0].rstrip(" "), time[1].lstrip(" "))
    
    def formatAddress(self):
        self.address2 = f'{self.city}, {self.state} {self.zip}'
        query = f'{self.streetAddress} {self.address2}'
        urlSafe = urllib.parse.quote(query)
        self.addressLink = "https://www.google.com/maps/search/?api=1&query=Costco+Gasoline+" + urlSafe

def interpretCostcoAJAX(costcoAJAX):
    '''Interprets raw Costco AJAX Response and returns useful classes.'''
    print(f'Response from Costco AJAX: {costcoAJAX}')
    r = costcoAJAX.json()
    del r[0] # Response is always padded with an irrelevant True statement
    locations = []
    for location in r:
        locations.append(CostcoLocation(location))
    return locations

def getCostcoLocations(zip):
    '''Returns list of Costco Location Classes for a Given ZIP Code.'''
    return interpretCostcoAJAX(getCostcoAJAX(getCoordinates(zip)))
