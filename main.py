
#!/usr/bin/python
import telebot
import openai
from datetime import datetime
from sys import platform
from botapiconfig import openaiapi, telegrambotapi

bot = telebot.TeleBot(telegrambotapi)
openai.api_key = openaiapi

@bot.message_handler(commands=['start','help'])
def start_message(message):
	bot.send_message(message.chat.id, 'Просто напиши текстом свой запрос, я отвечу')

@bot.message_handler(content_types=['text'])
def chat_handler(message):
	command = message.text
	bot_base_message = bot.send_message(message.chat.id, '♻️[GPT] Loading...')
	try:
		gpt_reply = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': command}],)
	except Exception as e:
		bot.reply_to(message, text='⚠Heavy load on OpenAI servers! Try again')
	bot.edit_message_text('✅[GPT] Done!', chat_id=message.chat.id, message_id=bot_base_message.message_id)
	if 'gpt_reply' in locals():
		bot.reply_to(message, text=gpt_reply['choices'][0]['message']['content'])
		f = open("/home/kotk/nginx_files/log.txt","a")
		f.writelines('\n')
		f.writelines('userID: ')
		f.writelines(str(message.from_user.id))
		f.writelines(' Username: ')
		f.writelines(str(message.from_user.username))
		f.writelines(' Date: ')
		f.writelines(str(datetime.fromtimestamp(message.date)))
		f.writelines('\n')
		f.writelines('Prompt: ')
		f.writelines(str(command))
		f.writelines('\n')
		f.writelines('AI reply: ')
		f.writelines(str(gpt_reply['choices'][0]['message']['content']))
		f.writelines('\n')
		f.writelines('---------------------------------------------------------------------------')
		f.close
	else:
		pass
bot.infinity_polling()
