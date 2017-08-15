# -*- coding: utf-8 -*-

import enum
import uuid

from .Field import Field
from .Constants import * # For temporary managing for hot/cold

class Concept:
	uuid = None
	name = ""
	__explanation = ""
	__fields = []

	# "arg" should be one of...
	# 1. Elements list Json(= dict type) --> Input key should not None.
	# 2. Cloning target(= Another Concept) --> Input key should be None.
	def __init__(self, arg, key = None):
		self.__fields = []

		if type(arg) == dict:
			if key == None:
				pass # Do not proceed these part. goto end part, and call error.
			
			else:
				# Setting name as key
				self.name = str(key)

				# Setting explanation
				self.__explanation = arg.get('Explanation')
				# Covering blank-explanation case
				if self.__explanation == None:
					self.__explanation = "Currently, explanation about this concept <" + str(name)

				# Setting fields
				fields = arg.get('Fields')
				if fields == None:
					print('CRITICAL ERROR while reading Concept-Field config -', key)
					pass
				else:
					for name in list(fields.keys()):
						fieldConfig = fields.get(name)

						self.__fields.append(Field(name, fieldConfig))
				return
			
		elif type(arg) == Concept:
			if key != None:
				pass # Do not proceed these part. goto end part, and call error.

			else:
				# Cloning
				self.name = arg.name
				self.__explanation = arg.getExplanation()

				if arg.uuid == None:
					# When cloning from initial state = Newly inserted from initial state
					self.uuid = uuid.uuid4()
				else:
					self.uuid = prevElem.uuid
					for field in prevElem.__fields:
						if field.getValue() != None:
							self.setField([self.name, field.name, field.getValue()])
				return
			
		# If setting is properly finished, below part should not be called.

		print('CRITICAL ERROR while initializing Concept - type ', type(arg))
		# Should manage here... but nothing to do currently
		# @TODO

	def __str__(self):
		if self.name == "":
			return "Invalid Concept\n"
		else:
			text = "Concept Info <" + self.name + ">\n"

			if self.uuid != None:
				text += "UUID : " + self.uuid + "\n"

			text += "Explanation : " + self.__explanation + "\n"

			text += "Containing fields ---\n"
			for field in self.__fields:
				text += str(field) + "\n"

			return text

	def getExplanation(self):
		return self.__explanation

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

	def setField(self, entity):
		# Verifying concept type
		if self.name != entity[0]:
			print("WrongConceptException : Expected", self.name, ", but obtained", entity[0])
			return

		# entity = [Classname, FieldName, Value, Option] - Option is optional
		for field in self.__fields:
			if field.name == entity[1]:
				try:
					if field.getType() == bool:
						if (entity[2] == True) or entity[2] == 'Positive' or str(entity[2]).replace(' ','') in cold:
							field.setValue(True)
						elif (entity[2] == False) or entity[2] == 'Negative' or str(entity[2]).replace(' ','') in hot: # Manage explicitly because bool('Negative') = True
							field.setValue(False)
						else:
							print("WrongTypeException : Expected", field.getType(), ", but boolean word.")
					else:
						field.setValue(field.getType()(entity[2]))
						field.printStatus()
					return # Assume same name field is one.
				except Exception as ex:
					if field.getType() == int:
						if entity[2] == 'Zero':
							field.setValue(0)
						elif entity[2] == 'One':
							field.setValue(1)
						elif entity[2] == 'Two':
							field.setValue(2)
						else:
							print("WrongTypeException : Expected", field.getType(), ", but not 0-2.")
					else:
						print("WrongTypeException : Expected", field.getType(), "| Input", type(entity[2]))

		# When no fields are matching
		# TODO : add new field.

	def getStatus(self):
		status = []
		for field in self.__fields:
			status.append(field.getStatus())

		return status

	def getStatusStr(self):
		status = ''
		for field in self.__fields:
			status += field.getStatusStr() + '\n'

		return status

	def printStatus(self):
		print('UUID : ' + str(self.uuid))
		print(self.getStatus())
