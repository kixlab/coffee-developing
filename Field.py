# -*- coding: utf-8 -*-

import enum

types = [enum.Enum, int, bool, str] # Allowed types

# TODO : Implement as Bounded Integer, String

class Field:
	name = ''
	questionKR = ''
	__priority = 0 # Default is 0. Should not be changed
	__type = None
	__value = None
	
	def __init__(self, name, questionKR, typeDef, priority = 0):
		if not typeDef in types:
			print('WrongTypeError :', typeDef)
		else:
			self.name = name
			self.questionKR = questionKR
			self.__priority = priority
			self.__type = typeDef

	def setValue(self, val):
		if val == None:
			self.__value == None
		elif type(val) == self.__type:
			self.__value = val
		else:
			print('TypeMismatchError : Expected', self.__type, '/ Input', type(val))

	def getValue(self):
		return self.__value
	
	def getPriority(self):
		return self.__priority

	def getType(self):
		return self.__type
	
	def isFilled(self):
		return self.__value != None

	def getStatus(self):
		return [self.name, str(self.__value)]
		
	def getStatus(self):
		return self.name + ' = ' + str(self.__value)

	def printStatus(self):
		print(self.getStatus())
		
	def printQuestion(self):
		print('(', self.name, '-', self.__type, ')')

	# MAYBE TEMPORARY FUNCTIONS

	def printQuestionKR(self):
		return self.questionKR

	def getAttach(self): # Might moved to Util.py
		bottomEmpty = (ord(self.questionKR[-1]) % 28 == 16)
		if bottomEmpty:
			return '는'
		else:
			return '은'

	def getQuestion(self):
		if self.__type == enum.Enum:
			return '어떤 걸로 할까요'
		elif self.__type == int:
			return '얼마나 할까요'
		elif self.__type == bool:
			return '넣어 드릴까요'
		elif self.__type == str:
			return '어떤 걸로 할까요'
		else:
			print('TYPE-ERROR on Field.getQuestion()')
			return None # ERROR CASE
