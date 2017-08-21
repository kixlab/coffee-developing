# -*- coding: utf-8 -*-

# Use through import

import enum

##### Common functions

# Check whether text is on string.

def msgFind(msg, keyword):
    return msg.lower().find(keyword) != -1

##### Temporary common constants storage

# Deprecated : Hot/Cold List

hot = ['뜨러운', '뜨거운', 'hot', '데운 것', '데운', '미지근한', '뜨거운것', '뜨거워', '따뜻한', '얼음넣지마세요']
cold = ['시원한', '시원한것', '시원한거', '차가운것', '차가운', '차가워', '찬것', '찬거', '찬걸로', '차디찬', '아이스', '차갑게']

# Commands in Stack

commands = ['start', 'coffee_service', 'set_field', 'recommend', 'print', 'stack', 'back', 'front']

# Initializing concept setting. Should be properly inserted.

initialConceptName = 'Coffee'

# Thresholds for Intents(Currently not using) and Entity

intentThreshold = 0.1
entityThreshold = 0.1

# Options for Field.py

types = [enum.Enum, int, bool, str] # Allowed types
OPTIONS = ["QuestionKR", "ReplyExample", "Type", "Min", "Max", "Priority"]

# True-False decision storage

goTrue = [True, 'True', 'Hot', 'To_Go', 'Positive', 'On', 'High']
goFalse = [False, 'False', 'Cold', 'In_House', 'Negative', 'Off', 'Low']

# Number code. Call by coord
goNum = ['Zero', 'One', 'Two', 'Three']