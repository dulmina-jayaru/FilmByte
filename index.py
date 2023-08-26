import os
from io import BytesIO
import requests
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from movies_scraper import search_movies, get_movie

TOKEN = "6486303828:AAGufErAT2_a6bVgtA0GIPI_87_ccQOKbwM"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, f"Hello {message.from_user.first_name}, Welcome to FilmByte Movies.\n"
                          f"🔥 Download Your Favourite Movies For 💯 Free And 🍿 Enjoy it.")
    bot.send_message(message.chat.id, "👇 Enter Movie Name 👇")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def find_movie(message):
    search_results = bot.reply_to(message, "Processing...")
    query = message.text
    movies_list = search_movies(query)
    if movies_list:
        keyboards = []
        for movie in movies_list:
            keyboard = InlineKeyboardButton(movie["title"], callback_data=movie["id"])
            keyboards.append([keyboard])
        reply_markup = InlineKeyboardMarkup(keyboards)
        bot.edit_message_text(chat_id=message.chat.id, message_id=search_results.message_id,
                              text='Search Results...', reply_markup=reply_markup)
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=search_results.message_id,
                              text='Sorry 🙏, No Result Found!\nCheck If You Have Misspelled The Movie Name.')


@bot.callback_query_handler(func=lambda call: True)
def movie_result(call):
    s = get_movie(call.data)
    response = requests.get(s["img"])
    img = BytesIO(response.content)
    bot.send_photo(call.message.chat.id, photo=img, caption=f"🎥 {s['title']}")
    link = ""
    links = s["links"]
    for i in links:
        link += "🎬" + i + "\n" + links[i] + "\n\n"
    caption = f"⚡ Fast Download Links :-\n\n{link}"
    if len(caption) > 4095:
        for x in range(0, len(caption), 4095):
            bot.send_message(call.message.chat.id, text=caption[x:x+4095])
    else:
        bot.send_message(call.message.chat.id, text=caption)
bot.delete_webhook()

bot.infinity_polling()

