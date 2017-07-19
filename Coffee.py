# -*- coding: utf-8 -*-

import enum
import uuid

import Field

class Coffee:
	uuid = None
	__fields = []
	
	def __init__(self, prevCoffee = None):
		self.__fields = []
		self.__fields.append(Field.Field('Coffee_Fields::Coffee_Kind', '커피 종류', str, 200))
		self.__fields.append(Field.Field('Syrup', '시럽', bool, 200)) # MAX ?
		self.__fields.append(Field.Field('Shot', '샷 추가', int, 200)) # MAX 3?
		self.__fields.append(Field.Field('Ice', '얼음', bool, 200))
		self.__fields.append(Field.Field('Takeout', '테이크아웃', bool, 200))

		if prevCoffee != None:
			self.uuid = prevCoffee.uuid
			for field in prevCoffee.__fields:
				self.applyValue(field.getStatus())

		else:
			self.uuid = uuid.uuid4()
	
	def process(self):
		highestPriorityField = self.getHighestPriorityField()
		while highestPriorityField != None:
			highestPriorityField.printQuestion()
			self.applyValue()
			self.printStatus()
			highestPriorityField = self.getHighestPriorityField()
			
	def getHighestPriorityField(self):
		highestPriority = -1
		highestPriorityField = None
		for field in self.__fields:
			if field.isFilled(): # Skip filled fields
				pass
			else:
				if highestPriority < field.getPriority():
					highestPriority = field.getPriority()
					highestPriorityField = field
		return highestPriorityField

	def isFilled(self):
		return self.getHighestPriorityField() == None

	# get "field + val, divided with one space"
	def applyValue(self, msg = None):
		if msg == None or msg == '':
			#msg = input('VALUE INPUT : ')
			print('No arguments to set :(')
			return

		msg = msg.split()
		if len(msg) < 2:
			print("Not enough parameters :", len(msg))
			# TODO - Divide specifically - len-0, len-1, len-2+
		else:
			if msg[1] == 'None':
				return
			for field in self.__fields:
				if field.name == msg[0]:
					try:
						field.setValue(field.getType()(''.join(msg[1:])))
					except Exception as ex:
						print("WrongTypeException : Expected", field.getType(), "| Input", type(msg[1]))

	def printStatus(self):
		print('UUID :', self.uuid)
		for field in self.__fields:
			field.printStatus()
		print()
