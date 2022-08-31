import telebot
import creds
import helpers
import time

TOKEN = creds.TOKEN

sent_sticker = {}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['mute'])
def handle_mute_cmd(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['administrator', 'creator']:
        lst = message.text.split(' ')
        how_long = float(lst[1])
        if how_long <= 30.0:
            how_long = 31.0
        uid_for_ban = message.reply_to_message.from_user.id
        if bot.get_chat_member(message.chat.id, uid_for_ban).status in ['administrator', 'creator']:
            bot.reply_to(message, 'Админов мутить нельзя, обратись к @rezepinn, @Lil_Danil228 или @rizh42')
        else:
            bot.restrict_chat_member(chat_id=message.chat.id, user_id=uid_for_ban, until_date=time.time() + how_long)
            bot.reply_to(message, f'@{bot.get_chat_member(message.chat.id, uid_for_ban).user.username} был замучен на\
                                        {how_long}')


@bot.message_handler(content_types=['new_chat_members'])
def handle_new_member(message):
    usr = message.new_chat_members[-1].username
    if usr is None:
        usr = message.new_chat_members[-1].first_name
    print(message)
    bot.reply_to(message, helpers.greet(usr))


@bot.message_handler(content_types=['sticker'])
def handle_stickers(message):
    print(message)
    usr = message.from_user.username
    sticker_timeout_flg = helpers.check_timeout(bot, sent_sticker, message, usr)
    if sticker_timeout_flg:
        bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['text'])
def handle_hashtags(message):
    chat_id = message.chat.id
    group_id = '@coliving5'
    if message.text.find("#важно") != -1:
        bot.forward_message(group_id, chat_id, message.message_id)


bot.set_update_listener(helpers.listener)
bot.infinity_polling()

