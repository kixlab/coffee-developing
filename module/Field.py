# -*- coding: utf-8 -*-

import enum

types = [enum.Enum, int, bool, str] # Allowed types
OPTIONS = ["QuestionKR", "ReplyExample", "Type", "Limit", "Priority"]
# Dict elements
# - QuestionKR
# - ReplyExample (Optional)
# - Type (Limited - only elements in list [types] is available)
# - Limit (Optional, Type limitation)
# - Priority (Optional, Default = 0)

# TODO : Implement as Bounded Integer, String

class Field:
	name = ''
	__option = dict()
	__value = None
	
	# name = Field name
	# fieldConfig = dict about options
	def __init__(self, name, fieldConfig):
		self.name = name
		self.__option = dict()
		self.value = None
		for option in OPTIONS:
			self.__option[option] = fieldConfig.get(option)
			# Put even None, and all OPTIONS slots are alive.

	def __str__(self):
		if self.name == "":
			return "Invalid Field\n"
		else:
			text = "Field Info <" + self.name + ">\n"

			text += "Field options ---\n"
			for option in OPTIONS:
				setting = self.__option.get(option)
				if setting != None:
					text += option + " : " + str(setting) + "\n"

			return text

	def setValue(self, val):
		if val == None:
			self.__value == None
		elif type(val) == self.__type:
			self.__value = val
		else:
			print('TypeMismatchError : Expected', self.__type, '/ Input', type(val))

	def __getOption(self, code):
		if self.name == '':
			print('Empty Field Error - tried to access', code)
		elif code in OPTIONS:
			return self.__option.get(code)
		else:
			print('Improper option code on Field -', code)

	def getValue(self):
		return self.__value
	
	def getPriority(self):
		return self.__getOption("Priority")

	def getType(self):
		return self.__getOption("Type")
	
	def isFilled(self):
		return self.__value != None

	def getStatus(self):
		return [self.name, str(self.__value)]
		
	def getStatusStr(self):
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
