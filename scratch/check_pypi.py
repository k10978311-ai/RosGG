import urllib.request
import re

req = urllib.request.Request('https://pypi.org/search/?q=etc1', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
packages = re.findall(r'package-snippet__name">([^<]+)</span>', html)
print('Packages:', packages)
