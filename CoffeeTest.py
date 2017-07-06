import Coffee

cursor = -1
stack = []

while True:
    if cursor != -1:
        print('> Recommend to fill - ', end = '')
        stack[cursor].getHighestPriorityField().printQuestion()

    msg = input('INPUT : ')
    if msg.lower().find('service_start') != -1:
        stack.append(Coffee.Coffee())
        cursor += 1
        # Start
    elif msg.lower().find('set_field') != -1:
        if cursor == -1:
            print('Coffee not started')
        else:
            current_coffee = Coffee.Coffee(stack[cursor])
            current_coffee.applyValue()
            stack.append(current_coffee)
            cursor += 1
    elif msg.lower().find('recommend') != -1:
        if cursor == -1:
            print('Coffee not started - Recommend')
        else:
            print('Recommend about...')
            stack[cursor].getHighestPriorityField().printQuestion()
    elif msg.lower().find('print') != -1:
        if cursor == -1:
            print('Coffee not started')
        else:
            stack[cursor].printStatus()
    elif msg.lower().find('stack') != -1:
        i = 0
        print('Cursor on #', cursor, sep = '')
        for coffee in stack:
            print('Coffee #', i, 'Status')
            coffee.printStatus()
            i += 1
    elif msg.lower().find('back') != -1:
        if cursor == -1:
            print('Coffee not started')
        elif cursor == 0:
            print('Cursor on bottom')
        else:
             cursor -= 1
    elif msg.lower().find('front') != -1:
        if cursor == -1:
            print('Coffee not started')
        elif cursor == len(stack) - 1:
            print('Cursor on top')
        else:
             cursor += 1
    
