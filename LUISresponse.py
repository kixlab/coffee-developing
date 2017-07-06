import urllib.request
import json

link = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/b17f3e2d-8222-45c1-a51e-300d12dead2d?subscription-key=99632d6d302c405f8ff27c28ffc7d8d7&staging=true&verbose=true&timezoneOffset=0&q="
query = input("QUERY : ")
print(query)
f = urllib.request.urlopen(link + query)
myfile = f.read()
resultJson = json.loads(myfile)
print(resultJson)
