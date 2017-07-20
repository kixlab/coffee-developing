#from __future__ import print_function
from Coffee import Coffee
from LUISconnector import LUISconnector

intentThreshold = 0.1

class Stack():
	cursor = None
	stack = None
	coffeeLUIS = None

	def __init__(self):
		self.cursor = -1
		self.stack = []
		self.coffeeLUIS = LUISconnector()

	def run(self): # For stand-alone
		while True:
			self.react()

	def react(self, msg = None):
		reply = ''
		
		if msg == None:
			msg = input('> QUERY : ')

		args = None
		# Not applied for mainstream yet
		resultJson = self.coffeeLUIS.getJson(msg)

		query = resultJson.get('query')
		topScoringIntent = resultJson.get('topScoringIntent')

		if topScoringIntent == None:
			print('No topScoringIntent')
			return

		topIntent = topScoringIntent.get('intent')
		topScore = topScoringIntent.get('score')
		if topScore < intentThreshold:
			print("WARNING : Not enough intent score :", topScore * 100) # 0-100 Scale.
			reply = reply + "Cannot understand intent [" + topIntent + ", " + str(topScore * 100) + "]\n"
			return

		entities = resultJson.get('entities')

		msg = topIntent # as next message
		args = ''

		#### TODO - CHANGE HERE ####
		for entity in entities:
			args = args + self.entityAnalysis(entity)
			# Problem - multiple-entity should be concerned later.

		reply = reply + '\n' + msg + '\n' + args
		self.command(msg, args)

		# Moved Recommendation order.
		if not self.__notFilled():
			question = self.__current().getHighestPriorityField().printQuestionKR()
			print('ASK > ' + question)
			reply = reply + 'ASK > ' + question

		return reply

	def command(self, msg = None, args = None):
		if msg == None:
			msg = input('INPUT : ')

		if self.msgFind(msg, 'coffee_service'):
			self.service_start() # Starting service by creating new coffee argument
		elif self.msgFind(msg, 'set_field'):
			self.set_field(args)
		elif self.msgFind(msg, 'recommend'):
			self.recommend()
		elif self.msgFind(msg, 'print'):
			self.print()
		elif self.msgFind(msg, 'stack'):
			self.print_stack()
		elif self.msgFind(msg, 'back'):
			self.cursor_move(-1)
		elif self.msgFind(msg, 'front'):
			self.cursor_move(1)
		else:
			print(msg, 'is not covered order.')
			
	def msgFind(self, msg, keyword):
		return msg.lower().find(keyword) != -1

	def entityAnalysis(self, entityDict):
		entity = entityDict.get('entity')
		entityType = entityDict.get('type')
		score = entityDict.get('score')

		if score < intentThreshold:
			print("WARNING : Not enough intent score :", entity, entitiType, score * 100) # 0-100 Scale.
			return ''
		else:
			return entityType + ' ' + entity + '\n'


		# startIndex and endIndex?


	### Functions for each works

	def service_start(self):
		self.stack.append(Coffee())
		self.cursor = len(self.stack)-1 # Automatically move to top

	def set_field(self, msg = None):
		if self.__notFilled():
			print('Coffee not started - Set_field')
			return # Case : cursor = -1

		current_coffee = Coffee(self.__current())
		current_coffee.applyValue(msg)
		self.stack.append(current_coffee)
		self.cursor_move(1) # TODO : Change
		print('Current Coffee state :')
		current_coffee.printStatus()

	def recommend(self):
		if self.__notFilled():
			print('Coffee not started - Recommend')
		else:
			print('Recommend about...')
			self.__current().getHighestPriorityField().printQuestion()

	def print(self):
		if self.__notFilled():
			print('Coffee not started')
		else:
			self.__current().printStatus()

	def print_stack(self):
		i = 0
		print('Cursor on #', self.cursor, sep = '')
		for coffee in self.stack:
			print('Coffee #', i, 'Status')
			coffee.printStatus()
			i += 1

	def cursor_move(self, d):
		if self.__notFilled():
			print('Coffee not started')
		elif self.cursor + d < 0 or self.cursor + d >= len(self.stack):
			print('Moved cursor out of range')
		else:
			 self.cursor += d

	def __notFilled(self):
		return self.cursor == -1

	def __current(self):
		if self.__notFilled():
			print('Coffee not started')
			return None
		# TODO : Exception should be managed at here?
		return self.stack[self.cursor]

	# TODO IDEA : manage cursor == -1 case with other procedure