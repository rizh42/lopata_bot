import time


def listener(messages):
    with open('.\\log.txt', 'a+') as f:
        for m in messages:
            if m.content_type == 'text' or m.content_type == 'sticker':
                f.write(str(m.from_user.username) + "||" + time.strftime("%m/%d/%Y, %H:%M:%S", time.gmtime(m.date))
                        + "||" + " [" + str(m.chat.id) + "] || " + m.content_type + "||" + m.chat.type + '\n')


def check_timeout(bot, sent_sticker, message, username):
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


def greet(usr):
    return(f'''
        Привет, {usr}!
        Заходи, устраивайся
        Читай закреп, залетай в форсы и кидай свои любимые мемы
    ''')
