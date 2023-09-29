import sqlite3

# импорт нужных файлов и библиотек
import telebot
from wwbd import *
from config import *
from telebot import types
import requests


bot = telebot.TeleBot(key_tg, parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	con = sqlite3.connect(r"db.db", check_same_thread=False)
	cursor = con.cursor()
	registration(con,cursor,message.from_user.id)
	con.close()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Все категории")
	item2 = types.KeyboardButton("Мои подписки")
	item3 = types.KeyboardButton("Отписаться от..")


	markup.add(item1, item2, item3)

	bot.send_message(message.chat.id,"Привет, это новостной бот", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
	if message.chat.type == 'private':
		if message.text == 'Все категории':
			con = sqlite3.connect(r"db.db", check_same_thread=False)
			cursor = con.cursor()
			markup = types.InlineKeyboardMarkup(row_width=2)
			for categ in all_categories(cursor):
				i = str(categ)
				item = types.InlineKeyboardButton(f"{categ}", callback_data=f"про_{categ}")
				markup.add(item)


			bot.send_message(message.chat.id, "Это все категории, на новости которых вы можете подписаться", reply_markup=markup)
		elif message.text == "Мои подписки":
			con = sqlite3.connect(r"db.db", check_same_thread=False)
			cursor = con.cursor()
			markup = types.InlineKeyboardMarkup(row_width=2)
			print(find_category_user(cursor,message.chat.id))
			if find_category_user(cursor,message.chat.id) == None:
				bot.send_message(message.chat.id, "Вы не подписаны ни на одну категорию ")
			else:
				for categ_pod in look_sub(cursor,message.chat.id):
					i = str(categ_pod)
					item = types.InlineKeyboardButton(f"{categ_pod}", callback_data=f"под_{categ_pod}")
					markup.add(item)
				bot.send_message(message.chat.id, "Вы подписаны на: ", reply_markup=markup)
				bot.send_message(message.chat.id, "Для просмотра новости нужно нажать на интересующую вас категорию")

		elif message.text == "Отписаться от..":
			con = sqlite3.connect(r"db.db", check_same_thread=False)
			cursor = con.cursor()
			markup = types.InlineKeyboardMarkup(row_width=3)
			if find_category_user(cursor, message.chat.id) == None:
				bot.send_message(message.chat.id, "Вы не подписаны ни на одну категорию")
			else:
				for categ_otp in look_sub(cursor, message.chat.id):
					i = str(categ_otp)
					item = types.InlineKeyboardButton(f"{categ_otp}", callback_data=f"отп_{categ_otp}")
					markup.add(item)
				bot.send_message(message.chat.id, "Выберите новостную категорию, от которой хотите отписаться:", reply_markup=markup)
		else:
			bot.send_message(message.chat.id, "Я и не знаю что ответить на это")


@bot.callback_query_handler(func= lambda call:True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'про_Спорт':
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				if find_category_in_sub(cursor,call.message.chat.id, "Спорт") == None:
					sub_category(con, cursor, "Спорт", call.message.chat.id)
					bot.send_message(call.message.chat.id, "Вы подписались на спортивные новости")
				else:
					bot.send_message(call.message.chat.id, "Вы уже подписаны на спортивные новости")
			elif call.data == "про_Бизнес":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				if find_category_in_sub(cursor, call.message.chat.id, "Бизнес") == None:
					sub_category(con, cursor, "Бизнес", call.message.chat.id)
					bot.send_message(call.message.chat.id, "Вы подписались на бизнес новости")
				else:
					bot.send_message(call.message.chat.id, "Вы уже подписаны на бизнес новости")
			elif call.data == "про_Здоровье":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				if find_category_in_sub(cursor, call.message.chat.id, "Здоровье") == None:
					sub_category(con, cursor, "Здоровье", call.message.chat.id)
					bot.send_message(call.message.chat.id, "Вы подписались на новости о здоровье")
				else:
					bot.send_message(call.message.chat.id, "Вы уже подписаны на новости о здоровье")
			elif call.data == "про_Развлечение":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				if find_category_in_sub(cursor, call.message.chat.id, "Развлечение") == None:
					sub_category(con, cursor, "Развлечение", call.message.chat.id)
					bot.send_message(call.message.chat.id, "Вы подписались на новости о развлечениях")
				else:
					bot.send_message(call.message.chat.id, "Вы уже подписаны на новости о развлечениях")
			elif call.data == "про_Главное":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				if find_category_in_sub(cursor, call.message.chat.id, "Главное") == None:
					sub_category(con, cursor, "Главное", call.message.chat.id)
					bot.send_message(call.message.chat.id, "Вы подписались на главные новости")
				else:
					bot.send_message(call.message.chat.id, "Вы уже подписаны на главные новости")
			elif call.data == "про_Наука":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				if find_category_in_sub(cursor, call.message.chat.id, "Наука") == None:
					sub_category(con, cursor, "Наука", call.message.chat.id)
					bot.send_message(call.message.chat.id, "Вы подписались на научные новости")
				else:
					bot.send_message(call.message.chat.id, "Вы уже подписаны на научные новости")
			elif call.data == "про_Технология":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				if find_category_in_sub(cursor, call.message.chat.id, "Технология") == None:
					sub_category(con, cursor, "Технология", call.message.chat.id)
					bot.send_message(call.message.chat.id, "Вы подписались на технологические новости")
				else:
					bot.send_message(call.message.chat.id, "Вы уже подписаны на технологические новости")


			elif call.data == "отп_Спорт":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				unsub_category(con, cursor, "Спорт", call.message.chat.id)
				bot.send_message(call.message.chat.id, "Вы отписались от спортивных новостей")
			elif call.data == "отп_Бизнес":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				unsub_category(con, cursor, "Бизнес", call.message.chat.id)
				bot.send_message(call.message.chat.id, "Вы отписались от новостей о бизнесе")
			elif call.data == "отп_Здоровье":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				unsub_category(con, cursor, "Здоровье", call.message.chat.id)
				bot.send_message(call.message.chat.id, "Вы отписались от новостей о здоровье")
			elif call.data == "отп_Развлечение":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				unsub_category(con, cursor, "Развлечение", call.message.chat.id)
				bot.send_message(call.message.chat.id, "Вы отписались от новостей о развлечениях")
			elif call.data == "отп_Главное":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				unsub_category(con, cursor, "Главное", call.message.chat.id)
				bot.send_message(call.message.chat.id, "Вы отписались от главных новостей")
			elif call.data == "отп_Наука":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				unsub_category(con, cursor, "Наука", call.message.chat.id)
				bot.send_message(call.message.chat.id, "Вы отписались от научных новостей")
			elif call.data == "отп_Технология":
				con = sqlite3.connect(r"db.db", check_same_thread=False)
				cursor = con.cursor()
				unsub_category(con, cursor, "Технология", call.message.chat.id)
				bot.send_message(call.message.chat.id, "Вы отписались от новостей о технологиях")




			elif call.data == "под_Спорт":
				url = ('https://newsapi.org/v2/everything?'
					   'q=sports&'
					   'language=ru&'
					   'pageSize=1&'
					   'sortBy=popularity&'
					   f'apiKey={key_news}')

				response = requests.get(url).json()
				titl = response['articles'][0]['title']
				description = response['articles'][0]['description']
				url = response['articles'][0]['url']
				bot.send_message(call.message.chat.id,f"{titl}\n\n{description}\nПодробнее можно прочитать здесь:\n{url}")

			elif call.data == "под_Бизнес":
				url = ('https://newsapi.org/v2/everything?'
					   'q=business&'
					   'language=ru&'
					   'pageSize=1&'
					   'sortBy=popularity&'
					   f'apiKey={key_news}')

				response = requests.get(url).json()
				titl = response['articles'][0]['title']
				description = response['articles'][0]['description']
				url = response['articles'][0]['url']
				bot.send_message(call.message.chat.id,f"{titl}\n\n{description}\nПодробнее можно прочитать здесь:\n{url}")

			elif call.data == "под_Здоровье":
				url = ('https://newsapi.org/v2/everything?'
					   'q=health&'
					   'language=ru&'
					   'pageSize=1&'
					   'sortBy=popularity&'
					   f'apiKey={key_news}')

				response = requests.get(url).json()
				titl = response['articles'][0]['title']
				description = response['articles'][0]['description']
				url = response['articles'][0]['url']
				bot.send_message(call.message.chat.id,f"{titl}\n\n{description}\nПодробнее можно прочитать здесь:\n{url}")

			elif call.data == "под_Развлечение":
				url = ('https://newsapi.org/v2/everything?'
					   'q=entertaiment&'
					   'language=ru&'
					   'pageSize=1&'
					   'sortBy=popularity&'
					   f'apiKey={key_news}')

				response = requests.get(url).json()
				titl = response['articles'][0]['title']
				description = response['articles'][0]['description']
				url = response['articles'][0]['url']
				bot.send_message(call.message.chat.id,f"{titl}\n\n{description}\nПодробнее можно прочитать здесь:\n{url}")

			elif call.data == "под_Главное":
				url = ('https://newsapi.org/v2/everything?'
					   'q=general&'
					   'language=ru&'
					   'pageSize=1&'
					   'sortBy=popularity&'
					   f'apiKey={key_news}')

				response = requests.get(url).json()
				titl = response['articles'][0]['title']
				description = response['articles'][0]['description']
				url = response['articles'][0]['url']
				bot.send_message(call.message.chat.id, f"{titl}\n\n{description}\nПодробнее можно прочитать здесь:\n{url}")

			elif call.data == "под_Наука":
				url = ('https://newsapi.org/v2/everything?'
					   'q=science&'
					   'language=ru&'
					   'pageSize=1&'
					   'sortBy=popularity&'
					   f'apiKey={key_news}')

				response = requests.get(url).json()
				titl = response['articles'][0]['title']
				description = response['articles'][0]['description']
				url = response['articles'][0]['url']
				bot.send_message(call.message.chat.id, f"{titl}\n\n{description}\nПодробнее можно прочитать здесь:\n{url}")

			elif call.data == "под_Технология":
				url = ('https://newsapi.org/v2/everything?'
					   'q=technology&'
					   'language=ru&'
					   'pageSize=1&'
					   'sortBy=popularity&'
					   f'apiKey={key_news}')

				response = requests.get(url).json()
				titl = response['articles'][0]['title']
				description = response['articles'][0]['description']
				url = response['articles'][0]['url']
				bot.send_message(call.message.chat.id, f"{titl}\n\n{description}\nПодробнее можно прочитать здесь:\n{url}")

	except Exception as e:
		print(repr(e))

bot.polling(none_stop=True)