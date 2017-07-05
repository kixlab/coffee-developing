import Coffee
'''
a = Coffee.Coffee()
a.process()
a.printStatus()
'''

stack = []

while True:
    msg = input('INPUT : ')
    if msg.lower().find('service_start') != -1:
        stack.append(Coffee.Coffee())
        # Start
    elif msg.lower().find('set_field') != -1:
        if len(stack) == 0:
            print('Coffee not started')
        else:
            current_coffee = Coffee.Coffee(stack[-1])
            current_coffee.applyValue()
            stack.append(current_coffee)
    elif msg.lower().find('recommend') != -1:
        if len(stack) == 0:
            print('Coffee not started - Recommend')
        else:
            print('Recommend about...')
            stack[-1].getHighestPriorityField().printQuestion()
    elif msg.lower().find('print') != -1:
        if len(stack) == 0:
            print('Coffee not started')
        else:
            stack[-1].printStatus()
    elif msg.lower().find('stack') != -1:
        i = 0
        for coffee in stack:
            print('Coffee #', i, 'Status')
            coffee.printStatus()
            i += 1
    elif msg.lower().find('back') != -1:
        if len(stack) == 0:
            print('Coffee not started')
        else:
            stack.remove(stack[-1])
    
