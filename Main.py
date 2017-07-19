from Telegram import TelegramBot

bot = TelegramBot()
bot.ping()
bot.getMessageStack()
#bot.getMessageStack() # Working twice = Buffer cleaning.
#bot.sendMessage(412510630, '아메리카노')