# -*- coding: utf-8 -*-

import json

from .Concept import Concept

class ConceptStorage:
	storage = dict()
	
	# This reading part should be covered with try-catch
	def __init__(self):
		f = open("config/Fields.json", 'r', encoding='utf-8')
		settingJson = json.loads(f.read())
		keys = list(settingJson.keys()) # Each key in keys become Concept.name

		for key in keys:
			self.storage[key] = Concept(settingJson.get(key), key)
	
	def __str__(self):
		text = "Concepts stored Info ----------\n"

		for key in list(self.storage.keys()):
			text += str(self.storage.get(key))

		return text

	def containConcept(self, keyword):
		return self.getConcept(keyword) != None

	def getConcept(self, keyword):
		return self.storage.get(keyword)

	def getStatus(self):
		status = ''
		for field in self.__fields:
			status += field.getStatus() + '\n'

		return status

	def printStatus(self):
		print(self.getStatus())