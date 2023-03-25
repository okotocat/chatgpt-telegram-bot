#!/usr/bin/python
import telebot
import openai
import mysql.connector
from mysql.connector.conversion import MySQLConverter
from telebot import util
from datetime import datetime
from sys import platform
from api_keys import openaiapi, telegrambotapi, user, password, host, database

bot = telebot.TeleBot(telegrambotapi)
openai.api_key = openaiapi

@bot.message_handler(commands=['start','help'])
def start_message(message):
	bot.send_message(message.chat.id, 'Просто напиши текстом свой запрос, я отвечу  /// just type your prompt w/o any commands   /// contact:@tttriot')
@bot.message_handler(content_types=['text'])
def chat_handler(message):
	command = MySQLConverter().escape(message.text)
	bot_base_message = bot.send_message(message.chat.id, '♻️[GPT] Loading...')
	try:
		gpt_reply = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': command}],)
		gpt_for_mysql = MySQLConverter().escape(gpt_reply['choices'][0]['message']['content'])
	except openai.error.OpenAIError as e:				#OpenAI exception bout server load
		print(e)
		bot.reply_to(message, text='⚠Heavy load on OpenAI servers! Try again')
	bot.edit_message_text('✅[GPT] Done!', chat_id=message.chat.id, message_id=bot_base_message.message_id)
	if 'gpt_reply' in locals():
		splitted_text = util.smart_split(gpt_reply['choices'][0]['message']['content'], chars_per_string=2000)
		for text in splitted_text:
			try:
				bot.reply_to(message, text=text)
			except ApiTelegramException as e: 			#cuz reply's start witn \n\n, telegram throw exception about empty message.
				print(e)
				pass
		def push_to_db(message):
			mysqlconnection = mysql.connector.connect(
				user=user,
				password=password,
				host=host,
				database=database
				)
			mycursor = mysqlconnection.cursor()
			sql = "INSERT INTO main_table (user_id, timestamp, prompt, reply, username) VALUES (%s,%s,%s,%s,%s)"
			val = (message.from_user.id, str(datetime.fromtimestamp(message.date)), str(command), str(gpt_for_mysql), str(message.from_user.username))
			mycursor.execute(sql,val)
			mysqlconnection.commit()
			mycursor.close()
			mysqlconnection.close()
		push_to_db(message)
	else:
		pass
bot.infinity_polling()