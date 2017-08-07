from module.Telegram import TelegramBot
import time

bot = TelegramBot()

print('Left messages on buffer :')
bot.clearBuffer()

print('Running bot....')
bot.ping()
# Starting part

while True:
	code = bot.reply()
	if code == 0: # Code for running
		pass
	if code == 1: # Code for '/quit', Exit.
		print('Quit order inserted')
		bot.clearBuffer()
		break
	time.sleep(3)


#bot.getMessageStack() # Working twice = Buffer cleaning.
#bot.sendMessage(412510630, '아메리카노')

# NotEnough
