# -*- coding: utf-8 -*-

from .Commons import goTrue, goFalse, goNum, OPTIONS

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
	__config = None # Configuration for help cloning
	
	# name = Field name
	# fieldConfig = dict about options
	def __init__(self, name, fieldConfig):
		self.name = name
		self.__option = dict()
		self.__config = fieldConfig
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
			return

		elif self.getType() == "bool":
			if val in goTrue:
				self.__value = True
			elif val in goFalse:
				self.__value = False
			else:
				print("WrongTypeException @ Field.setValue() : Not boolean")

		elif self.getType() == "int":
			try:
			    val = int(val)
			except ValueError:
				try:
					val = goNum.index(val)
				except ValueError:
					print("WrongTypeException @ Field.setValue() : Not int")
					return

			_min = self.getMin()
			_max = self.getMax()
			if _min != None and _min > val:
				print("WrongRangeException @ Field.setValue() : Smaller than Min")
				return
			if _max != None and _max < val:
				print("WrongRangeException @ Field.setValue() : Larger than Max")
				return
			self.__value = val

		else:
			self.__value = str(val)

	def __getOption(self, code):
		if self.name == '':
			print('Empty Field Error - tried to access', code)
		elif code in OPTIONS:
			return self.__option.get(code)
		else:
			print('Improper option code on Field -', code)

	def getName(self):
		return self.name

	def getConfig(self):
		return self.__config

	def getValue(self):
		return self.__value
	
	def getPriority(self):
		return self.__getOption("Priority")

	def getType(self):
		return self.__getOption("Type")

	def getMin(self):
		return self.__getOption("Min")

	def getMax(self):
		return self.__getOption("Max")

	def getQuestionKR(self):
		return self.__getOption("QuestionKR")
	
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


	def getAttach(self): # Might moved to Util.py
		bottomEmpty = (ord(self.getQuestionKR()[-1]) % 28 == 16)
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
