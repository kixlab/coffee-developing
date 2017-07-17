import urllib.request
import urllib.parse
import json

linkCoffee = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/b17f3e2d-8222-45c1-a51e-300d12dead2d?subscription-key=99632d6d302c405f8ff27c28ffc7d8d7&staging=true&verbose=true&timezoneOffset=0&q="
'''
query = input("QUERY : ")
print(query)
f = urllib.request.urlopen(link + urllib.parse.quote(query))
myfile = f.read()
resultJson = json.loads(myfile)
print(resultJson)

query = resultJson.get('query')
topScoringIntent = resultJson.get('topScoringIntent')
entities = resultJson.get('entities')

print(query)
print(type(query)) # str
print(topScoringIntent)
print(type(topScoringIntent)) # dict [intent = , score = ]
print(entities)
print(type(entities)) # list
'''

class LUISconnector:
	__link = ''

	def __init__(self, link = linkCoffee):
		self.__link = link

	def getJson(self, query = None):
		if query == None:
			query = input('> QUERY : ')

		print('Query Message : ', query)

		url = urllib.request.urlopen(self.__link + urllib.parse.quote(query))
		resultJson = json.loads(url.read())

		# print(resultJson)

		return resultJson