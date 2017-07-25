#from __future__ import print_function
from Coffee import Coffee
from LUISconnector import LUISconnector

import re

intentThreshold = 0.1
commands = ['coffee_service', 'set_field', 'recommend', 'print', 'stack', 'back', 'front']

class Stack():
	cursor = None
	stack = None
	coffeeLUIS = None
	__msg = '' # Value for save return message

	def __init__(self):
		self.cursor = -1
		self.stack = []
		self.coffeeLUIS = LUISconnector(2)

	def run(self): # For stand-alone
		while True:
			self.react()

	def react(self, msg = None):
		if msg == None: # For console [ MainStack.py ]
			msg = input('> QUERY : ')

		# Command for debugging...
		block = msg.split()

		if block[0] in commands:
			self.run_intent(msg)
			return
		# Commands end

		resultJson = self.coffeeLUIS.getJson(msg)
		entities = resultJson.get('entities')
		self.run_entity(entities)

		if self.__current().isFilled(): # Finished
			self.__addMsg('커피를 다음과 같이 주문합니다.')
			self.__addMsg(self.__current().getStatus())
			return self.__getMsg() # And Return.

		# Moved Recommendation order.
		if not self.__notStarted():
			question = self.__current().getHighestPriorityField().printQuestionKR()
			print(question)
			self.__addMsg(question)

		return self.__getMsg()

	def parseEntity(self, entity):
		# Return as list/tuple form. [Object, FieldName, Value, others...]
		result = entity.get('type').split(':')
		result.append(entity.get('entity'))
		if '' in result:
			result.remove('') # To avoid :: case

		# Temporary coverage for shot
		if result[0] == result[2]: # ['Coffee', 'Shot', 'Coffee', 'Shot', 'Two', '두 번 ']
			result.remove(result[2])
			result.remove(result[2]) # [3] goes to [2]
		return result

	def run_entity(self, entities):
		current = Coffee(self.__current()) # Including starting Coffee when not started

		print('-- ENTITIES LIST --')
		for entity in entities:
			entityPath = self.parseEntity(entity)
			print(entityPath)
			# TODO - If first element is not matching, goto lower part
			if self.getClassName(current) == entityPath[0]:
				current.setField(entityPath)
				pass # entityPath[1]
			else:
				# Go back repeatly
				pass # Currently inimplemented

		print('-- ENTITIES LIST END --')
		self.stack.append(current)
		self.cursor_move(1) # TODO : Change
		print('Current Coffee state :')
		current.printStatus()

	def run_intent(self, msg = None, block = None):
		if msg == None:
			msg = input('INPUT : ')

		if block == None:
			block = msg.split()

		if self.msgFind(msg, 'coffee_service'):
			self.service_start() # Starting service by creating new coffee argument
		elif self.msgFind(msg, 'set_field'):
			self.set_field(block)
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
		elif self.msgFind(msg, 'None'):
			print('Error : Incomprehensible order. [None]')
			return 'Error : Incomprehensible order. [None]'

		else:
			print(msg, 'is not covered order.')
			
	def msgFind(self, msg, keyword):
		return msg.lower().find(keyword) != -1

	def getClassName(self, obj):
		# From "<class 'Coffee.Coffee'>" to Coffee
		return re.split('\'|\.', str(type(obj)))[2]
		# Split Result : ['<class ', 'Coffee', 'Coffee', '>']

	### Functions for each works

	def service_start(self):
		self.stack.append(Coffee())
		self.__addMsg('새 커피를 주문합니다.') # Message for new Coffee
		self.cursor = len(self.stack)-1 # Automatically move to top

	def set_field(self, block = None):
		if self.__notStarted():
			self.service_start()

		if len(block) == 1:
			print('No arguments - set_field')

		else:
			current_coffee = Coffee(self.__current())

			arg = ['Coffee']
			for elem in block[1:]:
				arg.append(elem)
				if len(arg) == 3:
					current_coffee.setField(arg)
					arg = ['Coffee']

			self.stack.append(current_coffee)
			self.cursor_move(1) # TODO : Change
			print('Current Coffee state :')
			current_coffee.printStatus()

	def recommend(self):
		if self.__notStarted():
			print('Coffee not started - Recommend')
		else:
			print('Recommend about...')
			self.__current().getHighestPriorityField().printQuestion()

	def print(self):
		if self.__notStarted():
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
		if self.__notStarted():
			print('Coffee not started')
		elif self.cursor + d < 0 or self.cursor + d >= len(self.stack):
			print('Moved cursor out of range')
		else:
			 self.cursor += d

	def __notStarted(self):
		return self.cursor == -1

	def __current(self):
		if self.__notStarted():
			print('Coffee not started. Create new Coffee')
			self.service_start()
			
		# TODO : Exception should be managed at here?
		return self.stack[self.cursor]

	def __addMsg(self, text):
		self.__msg += str(text) + '\n'

	def __getMsg(self):
		tmp = self.__msg
		self.__msg = ''
		return tmp

	# TODO IDEA : manage cursor == -1 case with other procedure