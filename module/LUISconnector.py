import urllib.request
import urllib.parse
import json

from .Commons import entityThreshold

linkCoffee1 = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/b17f3e2d-8222-45c1-a51e-300d12dead2d?subscription-key=99632d6d302c405f8ff27c28ffc7d8d7&verbose=true&timezoneOffset=0&q="
linkCoffee2 = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/b17f3e2d-8222-45c1-a51e-300d12dead2d?subscription-key=99632d6d302c405f8ff27c28ffc7d8d7&staging=true&timezoneOffset=0&verbose=true&q="

class LUISconnector:
	__link = ''
	resultJson = None

	def __init__(self, version = 1):
		if version == 2:
			self.__link = linkCoffee2
		else: # version 1 or exceptional cases
			self.__link = linkCoffee1

	def ask(self, query = None):
		if query == None:
			query = input('> QUERY : ')

		print('Query Message :', query)

		url = urllib.request.urlopen(self.__link + urllib.parse.quote(query))
		self.resultJson = json.loads(url.read())
		
	def getJson(self):
		return self.resultJson

	# Parse JSON to entities.
	# Return as [Concept, EntityType, EntityValue]		
	def getEntityList(self):
		if self.resultJson == None:
			return []
		else:
			entityList = []
			
			for entityJson in self.resultJson.get('entities'):
				path = entityJson.get('type').split(':')

				# For brute-force like cleaning
				# 1. To avoid :: case
				if '' in path:
					path.remove('')

				# 2. Currently, not managing 'Boolean::Boolean:Positive' cases...
				if path[0] == 'Boolean':
					continue

				# 3. Covering... ['Coffee', 'Shot', 'Coffee', 'Shot', 'Two', '두 번 ']
				if len(path) >= 3:
					if path[0] == path[2]:
						path.remove(path[2])
					if path[1] == path[2]: # [3] goes to [2], so compare with [1] and [2]
						path.remove(path[2])

				# If resolution-values is on, insert it
				if entityJson.get('resolution') != None:
					path.append(entityJson.get('resolution').get('values')[0])

				# When not filled properly, add entity name as entity value
				elif len(path) == 2:
					path.append(entityJson.get('entity'))

				# Finally, add to List UNLESS score is too low.
				# If score slot is not occur, consider as score 1.00
				score = entityJson.get('score')
				if score != None and score < entityThreshold:
					print('TooLowScoreException @ Entity :', path)
				else:
					entityList.append(path)

			return entityList