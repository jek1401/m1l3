import telebot 
from config import token 

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(func=lambda message: True)
def ban_for_links(message):
    if "https://" in message.text or "http://" in message.text:
        bot.ban_chat_member(message.chat.id, message.from_user.id)
        bot.reply_to(message, "Пользователь забанен за отправку ссылки.")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if len(message.text.split()) == 2:
        user_id = int(message.text.split()[1])
        admin = bot.get_chat_member(message.chat.id, message.from_user.id)
        if admin.status in ['administrator', 'creator']:
            bot.unban_chat_member(message.chat.id, user_id)
            bot.send_message(message.chat.id, f"Пользователь с ID {user_id} разбанен.")
        else:
            bot.send_message(message.chat.id, "У вас нет прав на разбан.")
    else:
        bot.send_message(message.chat.id, "Используйте команду /unban <user_id>")

bot.infinity_polling(none_stop=True)
