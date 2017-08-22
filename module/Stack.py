from .Concept import Concept
from .ConceptStorage import ConceptStorage
from .LUISconnector import LUISconnector
from .JSONexport import JSONexport
from .Commons import *

import re

class Stack():
	cursor = None
	stack = None
	connectLUIS = None
	conceptInit = None
	exportJSON = None
	__hasExported = False
	__msg = '' # Value for save return message

	def __init__(self):
		self.cursor = -1
		self.stack = []
		self.conceptInit = ConceptStorage()
		self.connectLUIS = LUISconnector(2)
		self.exportJSON = JSONexport()
		self.__msg = ''

	def run(self): # For stand-alone
		while True:
			self.react()

	def react(self, msg = None):
		self.__hasExported = False

		if msg == None: # For console [ MainStack.py ]
			msg = input('> QUERY : ')

		# Command for debugging...
		block = msg.split()

		if len(block) == 0:
			self.__errMsg('NoInputMessage')
			self.__getMsg() # Just empty message slot.
			return

		if block[0] in commands:
			self.run_intent(msg)

		# Commands end
		else:
			self.connectLUIS.ask(msg)
			self.set_fields()

		# Moved Recommendation order.

		if not self.__notStarted():
			if self.__current().isFilled(): # Finished
				self.__addMsg('서비스를 다음과 같이 수행합니다.')
				self.__addMsg(self.__current().getStatus())
				self.exportJSON.export(self.__current())
				self.__hasExported = True
				self.clear(self.__current().uuid)
				return self.__getMsg() # And Return.

			question = self.__current().getHighestPriorityField().getQuestionKR()
			print(question)
			self.__addMsg(question)

		return self.__getMsg()

	def clear(self, uuid):
		cursor_tmp = 0
		while cursor_tmp < len(self.stack):
			if self.stack[cursor_tmp].uuid == uuid:
				self.stack.remove(self.stack[cursor_tmp])
				self.cursor -= 1
			else:
				cursor_tmp += 1

	def run_intent(self, msg = None, block = None):
		if msg == None:
			msg = input('INPUT : ')

		if block == None:
			block = msg.split()

		if msgFind(msg, 'start'):
			if len(block) > 1:
				self.service_start(block[1])
			else:
				self.__errMsg('NotEnoughArgument @ Stack : Command \'start\'')

		elif msgFind(msg, 'coffee_service'): # to cover legacy code
			self.service_start('Coffee') # Starting service by creating new coffee argument

		elif msgFind(msg, 'set_field'):
			if len(block) == 4: # ['set_field'] + EntityPath(len=3)
				self.set_fields([block[1:4]])
			else:
				self.__errMsg('NotEnoughArgument @ Stack : Command \'set_field\'')

		elif msgFind(msg, 'recommend'):
			self.recommend()
		elif msgFind(msg, 'print'):
			self.print()
		elif msgFind(msg, 'stack'):
			self.print_stack()
		elif msgFind(msg, 'back'):
			self.__cursorMove(-1)
		elif msgFind(msg, 'front'):
			self.__cursorMove(1)
		elif msgFind(msg, 'None'):
			print('Error : Incomprehensible order. [None]')
			return 'Error : Incomprehensible order. [None]'

		else:
			print(msg, 'is not covered order.')

	### Functions for each works

	# Target = Keyword
	def service_start(self, target = initialConceptName):
		newConcept = self.conceptInit.getConcept(target)
		if newConcept == None:
			self.__errMsg('WrongConceptNameError @ Stack')
		else:
			self.stack.append(Concept(newConcept)) # Clone from storage
			self.__addMsg('새 서비스를 시작합니다.') # Message for new Concept
			self.cursor = len(self.stack)-1 # Automatically move to top

	def set_fields(self, block = None):
		if block == None:
			block = self.connectLUIS.getEntityList()
		storage = [] # Temporary storage

		for entityPath in block:
			# TEMPORARY COVERING PARTS
			# Part 1-1 : Color --> Light.Color, Location --> Light.Location
			if entityPath[0] in ["Color", "Location"] :
				entityPath = ['Light'] + entityPath

			# Part 1-2 : [Light_sat.Light_sat --> Light.Sat]
			if entityPath[0] == "Light_Sat":
				entityPath = ['Light', 'Sat'] + entityPath[2:]

			# Check whether Concept name is proper.
			if self.conceptInit.containConcept(entityPath[0]):
				target = None
				for concept in storage:
					if concept.getName() == entityPath[0]:
						target = concept

				# When there is no proper concept on storage...
				if target == None:
					origin = None # Origin for clone
					cursor_tmp = self.cursor
					while cursor_tmp >= 0:
						if self.stack[cursor_tmp].getName() == entityPath[0]: # When name is matching
							origin = self.stack[cursor_tmp]
							break
						cursor_tmp -= 1

					# When there is no proper concept on both storage and stack...
					if origin == None:
						origin = self.conceptInit.getConcept(entityPath[0])

					target = Concept(origin)
					storage.append(target)

				# Applying entity specs
				target.setEntity(entityPath)

			else:
				print(entityPath)
				self.__errMsg('WrongConceptNameError @ Stack.Entity ' + str(entityPath[0]))

		for concept in storage:
			self.stack.append(concept)
			self.cursor += 1 # TODO : Change
			print('Updated states :')
			concept.printStatus()

	def recommend(self):
		if self.__notStarted():
			print('Service not started - Recommend')
		else:
			print('Recommend about...')
			self.__current().getHighestPriorityField().printQuestion()

	def print(self):
		if self.__notStarted():
			print('Service not started')
		else:
			self.__current().printStatus()

	def print_stack(self):
		i = 0
		print('Cursor on #', self.cursor, sep = '')
		for concept in self.stack:
			print(concept.getName(), '#', i, 'Status')
			concept.printStatus()
			i += 1

	def __cursorMove(self, d):
		if self.__notStarted():
			print('Service not started')
		elif self.cursor + d < 0 or self.cursor + d >= len(self.stack):
			print('Moved cursor out of range')
		else:
			 self.cursor += d

	def __notStarted(self):
		return self.cursor == -1

	def __current(self):
		if self.__notStarted():
			print('Service not started. You need to start service.')
			return None
			
		# TODO : Exception should be managed at here?
		return self.stack[self.cursor]

	def __addMsg(self, text):
		self.__msg += str(text) + '\n'

	def __errMsg(self, text = ""):
		self.__msg += '에러 발생! ' + str(text) + '\n'
		print(text)

	def __getMsg(self):
		tmp = self.__msg
		self.__msg = ''
		return tmp

	def __str__(self):
		result = 'Stack information'
		for elem in self.stack:
			result += '\n' + str(elem)
		return result

	def needExport(self):
		return self.__hasExported

	# TODO IDEA : manage cursor == -1 case with other procedure
