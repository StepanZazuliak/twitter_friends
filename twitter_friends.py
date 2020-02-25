import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
import geopy
import time

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    print('')
    acct = input('Enter Twitter Account:')
    if (len(acct) < 1): break
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '5'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])

    list_friends = []
    for u in js['users']:
        help_list = []
        help_list.append(u['screen_name'])
        loc = u['location']
        
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent = "myGeocoder")
        location1 = geolocator.geocode(loc)
        lat1 = location1.latitude
        lon1 = location1.longitude
        help_list.append(lat1, lon1)
        time.sleep(1)
    
    map = folium.Map(zoom_start=18)

    fg = folium.FeatureGroup(name="Friends")

    for k in list_friends:
        lt = k[1]
        ln = k[2]
        friend = k[0]
        fg_fl.add_child(folium.CircleMarker(location = [lt, ln],
                                            radius = 10,
                                            popup = friend,
                                            color = 'red',
                                            fill_opacity = 0.5))
                                            
    map.add_child(fg)
    map.save('d:/UCU/2semestr/lab3/twiter/friends_map.html')
