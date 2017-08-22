from flask import Flask, request
import requests
import json

from .module.Stack import Stack

app = Flask(__name__)

userStack = dict() # [UserID - Stack]

@app.route("/", methods=['GET', 'POST'])
def response():
	msgJson = request.get_json(silent=True)
	if msgJson == None:
		return "Error : Unreceived message."

	userID = msgJson.get('rid')
	text = msgJson.get('message')

	if userID == None:
		return "Error : User ID is not defined."

	stack = userStack.get(userID)
	# If not ID is registered in "userStack"
	if stack == None:
		stack = Stack()
		userStack[userID] = stack

	if text == None:
		text = ''
	response = stack.react(text)

	result = None
	if stack.needExport():
		f = open("result/export.json", 'r', encoding = 'utf-8')
		result = json.loads(f.read())

	resp = requests.post('http://143.248.96.24/message/telebot', json=createResponse(response, userID, 0, 0))
	
	print('Response message :', response)

	return str(result)

@app.route("/ping")
def ping():
	return "Connection Test : Succeeded"

def createResponse(msg, rid, mmstep, mmstep_qna):
	response = dict()
	response['message'] = msg
	response['rid'] = rid
	response['mmstep'] = mmstep
	response['mmstep_qna'] = mmstep_qna
	return response