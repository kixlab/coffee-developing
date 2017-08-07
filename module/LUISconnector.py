import urllib.request
import urllib.parse
import json

linkCoffee1 = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/b17f3e2d-8222-45c1-a51e-300d12dead2d?subscription-key=99632d6d302c405f8ff27c28ffc7d8d7&verbose=true&timezoneOffset=0&q="
linkCoffee2 = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/b17f3e2d-8222-45c1-a51e-300d12dead2d?subscription-key=99632d6d302c405f8ff27c28ffc7d8d7&staging=true&timezoneOffset=0&verbose=true&q="

class LUISconnector:
	__link = ''

	def __init__(self, version = 1):
		if version == 2:
			self.__link = linkCoffee2
		else: # version 1 or exceptional cases
			self.__link = linkCoffee1

	def getJson(self, query = None):
		if query == None:
			query = input('> QUERY : ')

		print('Query Message :', query)

		url = urllib.request.urlopen(self.__link + urllib.parse.quote(query))
		resultJson = json.loads(url.read())

		# print(resultJson)

		return resultJson
