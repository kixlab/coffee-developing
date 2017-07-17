from Coffee import Coffee
from LUISconnector import LUISconnector

intentThreshold = 0.5

class Main():
	cursor = None
	stack = None
	coffeeLUIS = None

	def __init__(self):
		self.cursor = -1
		self.stack = []
		self.coffeeLUIS = LUISconnector()

	def run(self):
		while True:
			if not self.__notFilled():
				print('ASK > ', end = '')
				self.__current().getHighestPriorityField().printQuestionKR()

			msg = input('INPUT : ')
			if self.msgFind(msg, 'query'):
				# Not applied for mainstream yet
				resultJson = self.coffeeLUIS.getJson()
				query = resultJson.get('query')
				topScoringIntent = resultJson.get('topScoringIntent')
				topIntent = topScoringIntent.get('intent')
				topScore = topScoringIntent.get('score')
				if topScore < intentThreshold:
					print("WARNING : Not enough intent score :", topScore)
					pass

				entities = resultJson.get('entities')

				if topIntent == '':
					pass

				print(query)
				print(topScoringIntent)
				print('Query-Intent', topScoringIntent.get('intent'))
				print('Query-Intent-Type', type(topScoringIntent.get('intent')))
				print('Query-Score', topScoringIntent.get('score'))
				print('Query-Score-Type', type(topScoringIntent.get('score')))
				print(entities)


			if self.msgFind(msg, 'service_start'):
				self.service_start() # Starting service by creating new coffee argument
			elif self.msgFind(msg, 'set_field'):
				self.set_field()
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
			
	def msgFind(self, msg, keyword):
		return msg.lower().find(keyword) != -1

	### Functions for each works

	def service_start(self):
		self.stack.append(Coffee())
		self.cursor = len(self.stack)-1 # Automatically move to top

	def set_field(self):
		if self.__notFilled():
			print('Coffee not started - Set_field')
			return # Case : cursor = -1

		current_coffee = Coffee(self.__current())
		current_coffee.applyValue()
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
				

main = Main()
main.run()
