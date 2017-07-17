# -*- coding: utf-8 -*-

import enum

types = [enum.Enum, int, bool, str] # Allowed types

# TODO : Implement as Bounded Integer, String

class Field:
    name = ''
    nameKR = ''
    __priority = 0 # Default is 0. Should not be changed
    __type = None
    __value = None
    
    def __init__(self, name, nameKR, typeDef, priority = 0):
        if not typeDef in types:
            print('WrongTypeError :', typeDef)
        else:
            self.name = name
            self.nameKR = nameKR
            self.__priority = priority
            self.__type = typeDef

    def setValue(self, val):
        if type(val) == self.__type:
            self.__value = val
        else:
            print('TypeMismatchError : Expected', self.__type, '/ Input', type(val))

    def getValue(self):
        return self.__value
    
    def getPriority(self):
        return self.__priority

    def getType(self):
        return self.__type
    
        ''' # OLD CODE
        if self.isFilled():
            return type(__value)
        else:
            return None
        '''
    
    def isFilled(self):
        return self.__value != None

    def getStatus(self):
        return self.name + " " + str(self.__value)
        
    def printStatus(self):
        print(self.name, '=', self.__value)
        
    def printQuestion(self):
        print('(', self.name, '-', self.__type, ')')

    # MAYBE TEMPORARY FUNCTIONS

    def printQuestionKR(self):
        print(self.nameKR + self.getAttach(), self.getQuestion(), '할까요?')

    def getAttach(self): # Might moved to Util.py
        bottomEmpty = (ord(self.nameKR[-1]) % 28 == 16)
        if bottomEmpty:
            return '는'
        else:
            return '은'

    def getQuestion(self):
        if self.__type == enum.Enum:
            return '어떤 걸로'
        elif self.__type == int:
            return '얼마나'
        elif self.__type == bool:
            return '어떻'
        elif self.__type == str:
            return '어떤 걸로'
        else:
            print('TYPE-ERROR on Field.getQuestion()')
            return None # ERROR CASE
