# -*- coding: utf-8 -*-

import enum
import uuid

from .Field import Field
from .Commons import * # For temporary managing for hot/cold

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
					self.uuid = arg.uuid

				for field in arg.__fields: # Cloning setting. It should work even value is None.
					self.cloneField(field)

				self.printStatus()
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

	def getName(self):
		return self.name

	def getExplanation(self):
		return self.__explanation

	def getFields(self):
		return self.__fields

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

	def cloneField(self, field): # Clone and input to this Concept.
		newField = Field(field.getName(), field.getConfig())
		if field.isFilled():
			newField.setValue(field.getValue())
		self.__fields.append(newField)

	def setEntity(self, entity):
		# Verifying concept type
		if self.name != entity[0]:
			print("WrongConceptException : Expected", self.name, ", but obtained", entity[0])
			return

		# entity = [Classname, FieldName, Value, Option] - Option is optional
		for field in self.__fields:
			if field.name == entity[1]:
				field.setValue(entity[2])
				return # No duplicated fields

		# When no fields are matching.
		# Currently, error message printed.
		print('WrongFieldException @ Concept.setEntity()', str(entity[1]))
		# TODO(LongTerm) : add new field.

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
