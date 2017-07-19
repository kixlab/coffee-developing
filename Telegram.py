from Stack import Stack

import urllib.request
import urllib.parse
import json

token = 'bot393231664:AAE8oWmuhNM6zp_jmQXMcf2wJpxFuwPeRD8'
botID = 393231664
name = 'FlagshipTestBot'
apiLink = "https://api.telegram.org/" + token + "/" # Attach other arguments at back

class TelegramBot:
	prevOffset = None
	msgStack = []
	memory = Stack()

	def __init__(self):
		pass

	def order(self, order, args = []):
		link = apiLink + str(order)
		for arg in args:
			link = link + str(arg) # arg should include divisor.
		return link

	def react(self, order, args = []):
		url = urllib.request.urlopen(self.order(order, args))
		resultJson = json.loads(url.read())

		if (bool)(resultJson.get('ok')):
			print('SUCCESS :', order)
			pass
		else:
			print('ERROR :', order, '- Bot is not okay')

		return resultJson

	def ping(self):
		resultJson = self.react('getMe')

		result = resultJson.get('result')
		if result.get('id') == botID and result.get('first_name') == name and result.get('username') == name:
			print('SUCCESS for PING : Working correctly.')
			return
		print('ERROR : bot is not okay')

	def getMessageStack(self):
		args = []
		if self.prevOffset != None:
			args = ['?offset=', (self.prevOffset+1)]

		resultJson = self.react('getUpdates', args)

		result = resultJson.get('result')
		for msg in result:
			senderID = msg.get('message').get('from').get('id')
			senderNameFirst = msg.get('message').get('from').get('first_name')
			senderNameLast = msg.get('message').get('from').get('last_name')
			text = msg.get('message').get('text')
			print("Message info :", senderID, senderNameFirst, senderNameLast, text)
			self.msgStack.append(msg)
			self.prevOffset = msg.get('update_id')
			a = self.memory.react(text)
			self.sendMessage(senderID, self.memory.react(text))

	def sendMessage(self, userID, msg):
		args = ['?chat_id=', userID, '&text=', urllib.parse.quote(msg)]

		resultJson = self.react('sendMessage', args)
		