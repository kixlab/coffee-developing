# -*- coding: utf-8 -*-

import enum
import uuid

from .Field import Field

hot = ['뜨러운', '뜨거운', 'hot', '데운 것', '데운', '미지근한', '뜨거운것', '뜨거워', '따뜻한', '얼음넣지마세요']
cold = ['시원한', '시원한것', '시원한거', '차가운것', '차가운', '차가워', '찬것', '찬거', '찬걸로', '차디찬', '아이스', '차갑게']

class Coffee:
	uuid = None
	__fields = []
	
	def __init__(self, prevCoffee = None):
		self.__fields = []

		#self.__fields.append(Field.Field('Amount', '몇 컵 해드릴까요', int, 200))
		self.__fields.append(Field.Field('Cup_Type', '포장해 드릴까요? 예시 : [먹고갈꺼에요 / 들고갈게요]', str, 200)) # Enum으로 바꿔야함.... True-False 커버가 더 필요할듯...?
		self.__fields.append(Field.Field('Milk', '우유 넣어드릴까요? 예시 : [우유 빼줘 / 우유 넣어]', bool, 200)) # MAX ?
		self.__fields.append(Field.Field('Shot', '샷 추가는 얼마나 해드릴까요? 예시 : [샷 필요없어 / 샷 두번]', int, 200)) # 0-2
		self.__fields.append(Field.Field('Syrup', '시럽 넣어드릴까요? 예시 : [시럽 빼줘 / 시럽 넣어]', bool, 200))
		self.__fields.append(Field.Field('Temp', '아이스로 해드릴까요? 예시 : [뜨거운걸로요 / 차가운걸로요]', bool, 200)) # True는 아이스.
		self.__fields.append(Field.Field('Type', '어떤 커피로 해드릴까요? 예시 : [아메리카노 / 에스프레소]', str, 300))

		if prevCoffee != None:
			self.uuid = prevCoffee.uuid
			for field in prevCoffee.__fields:
				if field.getValue() != None:
					self.setField(['Coffee', field.name, field.getValue()])

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
