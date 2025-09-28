
from telebot import types
import  telebot
from telebot.apihelper import ApiTelegramException
from db import *
import time

# Для следующих создателей: Вставьте сюда ВАШ токен
TOKEN = '7962985337:AAEvmgi07WgkkbRz9CgMB0P2suk5-Uh2UOc'
bot = telebot.TeleBot(TOKEN)

# и ваш IP
admin = 6728754836

def is_admin(uid): return uid == admin

# Функция для постов
@bot.message_handler(commands=['broad'])
def broad(m):
    print(m.chat.id, admin, is_admin(m.chat.id))
    if not is_admin(m.chat.id):
        return bot.reply_to(m, 'Только для админа')

    parts = m.text.split(maxsplit=1)
    if len(parts) > 1:
        text = parts[1]
        return send_to_all(lambda cid: bot.send_message(cid, text), m)

    if m.reply_to_message:
        orig = m.reply_to_message

        def send_copy(cid):
            if orig.text:      return bot.send_message(cid, orig.text)
            if orig.photo:     return bot.send_photo(cid, orig.photo[-1].file_id, caption=orig.caption)
            if orig.video:     return bot.send_video(cid, orig.video.file_id, caption=orig.caption)
            if orig.document:  return bot.send_document(cid, orig.document.file_id, caption=orig.caption)
            if orig.audio:     return bot.send_audio(cid, orig.audio.file_id, caption=orig.caption)
            if orig.voice:     return bot.send_voice(cid, orig.voice.file_id)
            if orig.animation: return bot.send_animation(cid, orig.animation.file_id, caption=orig.caption)
            if orig.sticker:   return bot.send_sticker(cid, orig.sticker.file_id)
            return bot.forward_message(cid, orig.chat.id, orig.message_id)

        return send_to_all(send_copy, m)


def send_to_all(send_fn, m):
    ids = all_sub()
    ok = bad = 0
    for cid in ids:
        try:
            send_fn(cid);
            ok += 1
        except ApiTelegramException as e:
            if "blocked" in str(e).lower() or "chat not found" in str(e).lower():
                del_sub(cid)
            else:
                bad += 1
        except Exception:
            bad += 1
        time.sleep(0.03)
    bot.reply_to(m, f"Разослано {ok}, ошибок {bad}, всего {count_subs()}")

# Приветствие
@bot.message_handler(commands=['start'])
def start(message):
    add_sub(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Здравствуйте, я бот-переходник", reply_markup=markup)

# Переходник
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '👋 Поздороваться':
        bot.send_message(message.from_user.id, "📢 Я могу подсказать вам пару сайтов")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        about_b = types.KeyboardButton('📰 О потеплении 📰')
        found_b = types.KeyboardButton('💲 Благотворительность 💲')
        more_b  = types.KeyboardButton('🤍 узнать побольше 🤍')

        markup.add(about_b, found_b, more_b)
        bot.send_message(message.from_user.id, '❓ Какой сайт вас интересует?', reply_markup=markup) #ответ бота

    # Ссылки

    elif message.text == '📰 О потеплении 📰':
        bot.send_message(message.from_user.id, 'Новостные сайты:' +'\n\n'+ '[Earth Observatory](https://www.earthobservatory.nasa.gov/features/GlobalWarming)' +'\n\n'+ '[Naked Science](https://naked-science.ru/tags/globalnoe-poteplenie)' +'\n\n'+ '[Пост наука](https://postnauka.org/themes/globalnoe-poteplenie)',parse_mode='Markdown')

    elif message.text == '💲 Благотворительность 💲':
        bot.send_message(message.from_user.id, 'Сайты с благотворительностью' +'\n\n'+ '[РусКлиматФонд](https://rusclimatefund.ru/donation.html)'+'\n\n'+'[Посади лес](https://posadiles.ru/)'+'\n\n'+'[Подари планете жизнь](https://p-p-j.ru/)', parse_mode='Markdown')

    elif message.text == '🤍 узнать побольше 🤍':
        bot.send_message(message.from_user.id, 'Статья о помощи' +'\n\n'+ '[BBC News Русская служба](https://hi-tech.mail.ru/news/40099-pyat_sposobov_vnesti_svoy_vklad_v_borbu_s_globalnym_potepleniem/)', parse_mode='Markdown')

bot.polling(none_stop=True, interval=0)