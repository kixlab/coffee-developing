import enum
import Field

class Coffee:
    __fields = []
    
    def __init__(self, prevCoffee = None):
        self.__fields = []
        self.__fields.append(Field.Field('Type', str, 200))
        self.__fields.append(Field.Field('Sugar', int, 200))
        self.__fields.append(Field.Field('Prime', int, 200))

        if prevCoffee != None:
            for field in prevCoffee.__fields:
                self.applyValue(field.getStatus())
    
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
        if msg == None:
            msg = input('VALUE INPUT : ')
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
                        field.setValue(field.getType()(msg[1]))
                    except Exception as ex:
                        print("WrongTypeException : Expected", field.getType(), "| Input", type(msg[1]))

    def printStatus(self):
        for field in self.__fields:
            field.printStatus()
