from Coffee import Coffee
from LUISconnector import LUISconnector

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
			if self.cursor != -1:
				print('> Recommend to fill - ', end = '')
				self.stack[cursor].getHighestPriorityField().printQuestion()

			msg = input('INPUT : ')
			if msg.lower().find('service_start') != -1:
				self.service_start() # Starting service by creating new coffee argument
			elif msg.lower().find('set_field') != -1:
				self.set_field()
			elif msg.lower().find('recommend') != -1:
				self.recommend()
			elif msg.lower().find('print') != -1:
				self.print()
			elif msg.lower().find('stack') != -1:
				self.print_stack()
			elif msg.lower().find('back') != -1:
				self.cursor_move(-1)
			elif msg.lower().find('front') != -1:
				self.cursor_move(1)
			elif msg.lower().find('query') != -1:
				# Not applied for mainstream yet
				resultJson = coffeeLUIS.getJson()
				query = resultJson.get('query')
				topScoringIntent = resultJson.get('topScoringIntent')
				entities = resultJson.get('entities')
				print(query)
				print(topScoringIntent)
				print(entities)

	def service_start(self):
		self.stack.append(Coffee())
		self.cursor += 1

	def set_field(self):
		if self.__notFilled() == -1:
			print('Coffee not started')
		else:
			current_coffee = Coffee(stack[cursor])
			current_coffee.applyValue()
			self.stack.append(current_coffee)
			cursor += 1
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
		if __notFilled():
			print('Coffee not started')
		elif self.cursor + d < 0 || self.cursor + d >= len(self.stack):
			print('Moved cursor out of range')
		else:
			 self.cursor += d

	def __notFilled(self):
		return self.cursor == -1

	def __current(self):
		# TODO : Exception should be managed at here?
		return self.stack[cursor]

	# TODO IDEA : manage cursor == -1 case with other procedure
				

main = Main()
main.run()
