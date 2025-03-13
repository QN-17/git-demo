import urllib.request
response=urllib.request.urlopen('https://bing.com')
html=response.read ().decode('UTF-8')
print(html)