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
        how_long = lst[1]
        uid_for_ban = message.reply_to_message.from_user.id
        bot.restrict_chat_member(chat_id=message.chat.id, user_id=uid_for_ban, until_date=time.time() + how_long)
        bot.reply_to(message, f'{bot.get_chat_member(message.chat.id, uid_for_ban)} был замучен на {how_long}')


@bot.message_handler(content_types=['new_chat_members'])
def handle_new_member(message):
    usr = message.new_chat_member.username
    bot.reply_to(message, helpers.greet(usr))


@bot.message_handler(content_types=['sticker'])
def handle_stickers(message):
    usr = message.from_user.username
    sticker_timeout_flg = helpers.check_timeout(bot, sent_sticker, message, usr)
    if sticker_timeout_flg:
        bot.delete_message(message.chat.id, message.message_id)


bot.set_update_listener(helpers.listener)
bot.infinity_polling()

