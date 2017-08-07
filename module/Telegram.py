from .Stack import Stack, commands

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

	# Variables of KJ
	rep = None
	lst = ["포장",'우유','샷','시럽','아이스','커피']
	# ----------

	def __init__(self):
		pass

	def order(self, order, args = []):
		link = apiLink + str(order)
		con = '?'
		for arg in args:
			if arg[1] != '':
				link = link + con + str(arg[0]) + '=' + str(arg[1]) # arg should include divisor.
				con = '&'
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

	def reply(self): # Reply is included
		args = []
		if self.prevOffset != None:
			args = [['offset', (self.prevOffset+1)]]

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

			if text == '/start':
				self.memory.service_start() # Forcefully start.

			if text == '/quit':
				self.sendMessage(senderID, '서비스를 종료합니다.')
				return 1 # Code for quit

			# modified by KJ
			if self.rep != None:
				attachArg = True
				for command in commands:
					if text in command:
						attachArg = False
				if attachArg:
					for elm in self.lst:
						if elm in self.rep:
							if elm not in text:
								text = elm + " " + text
								break
			# ----------

			reply = self.memory.react(text)

			# modified by KJ
			self.rep = reply
			# ----------

			self.sendMessage(senderID, reply)

			if reply != None:
				if reply.find('커피를 다음과 같이 주문합니다.') != -1: # 종료일때.
					self.sendMessage(senderID, '커피 주문을 완료하여 서비스를 종료하겠습니다.')
					return 1 # Code for quit. At next modification, remove all same uuid case in stack.

		return 0

	def sendMessage(self, userID, msg):
		args = []
		if msg == None or msg == '':
			print('Tried to send empty message.')
		else:
			args = [['chat_id', userID], ['text', urllib.parse.quote(msg)]]

			resultJson = self.react('sendMessage', args)

	def clearBuffer(self):
		# To clear stack....
		args = []
		if self.prevOffset != None:
			args = [['offset', (self.prevOffset+1)]]

		self.react('getUpdates', args)

		print('Buffer cleared.')
