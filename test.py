import urllib.request
import json
from pprint import pprint

url = 'https://facebook.com/willy.tru.39'
resp = urllib.request.urlopen(url)
print(resp.data)
data = json.loads(resp.decode('utf-8'))
pprint (data)