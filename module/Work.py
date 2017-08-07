# -*- coding: utf-8 -*-

import enum
import uuid

from .Field import Field


class Core:
	uuid = None
	__fields = []
	
	def __init__(self, prevLight = None):
		self.__fields = []

		self.__fields.append(Field.Field('Name', '이름이 어떻게 되나요?', str, 200)) # Currently should not filled.

		if prevLight != None:
			self.uuid = prevLight.uuid
			for field in prevLight.__fields:
				if field.getValue() != None:
					self.setField(['Light', field.name, field.getValue()])

		else:
			self.uuid = uuid.uuid4()
			
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
		status = ''
		for field in self.__fields:
			status += field.getStatus() + '\n'

		return status

	def printStatus(self):
		print('UUID : ' + str(self.uuid))
		print(self.getStatus())