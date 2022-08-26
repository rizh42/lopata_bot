import telebot
import time

TOKEN = ''

sent_sticker = {}

bot = telebot.TeleBot(TOKEN)

def listener(messages):
    for m in messages:
        if m.content_type == 'text' or m.content_type == 'sticker':
            print(str(m.from_user.username) + "||" + time.strftime("%m/%d/%Y, %H:%M:%S", time.gmtime(m.date)) + "||" +
                  " [" + str(m.chat.id) + "] || " + m.content_type + "||" + m.chat.type)


def check_timeout(message, username):
    #print(username, int(time.time()), message.date, bot.get_chat_member(message.chat.id, message.from_user.id).status)
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['administrator', 'creator']:
        return False
    else:
        if username in sent_sticker:
            if message.date - sent_sticker[username] > 60:
                sent_sticker.pop(username)
                return False
            else:
                return True
        else:
            sent_sticker[username] = message.date
            return False


@bot.message_handler(content_types=['sticker'])
def handle_stickers(message):
    usr = message.from_user.username
    sticker_timeout_flg = check_timeout(message, usr)
    if sticker_timeout_flg:
        bot.delete_message(message.chat.id, message.message_id)


bot.set_update_listener(listener)
bot.infinity_polling()

