import urllib.request
respnse = urllib.request.urlopen('http://python.org')
import urllib.parse
data={
    'a':'传智播客',
    'b':'黑马程序员'
}
result=urllib.parse.urlencode(data)
print(result)