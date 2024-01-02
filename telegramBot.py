import os
import telebot
from telebot import types
import datetime
import configparser

bot = telebot.TeleBot('6479990017:AAEc3cVuUcp-MLzS1SePGYZHg-2L96Xg0wI',parse_mode=None)
ValCommands = 'no_commands'
config = configparser.ConfigParser()

def BlackListCheck(MessageCheck):
    config.read("config.ini")
    BlackList = config['Config']['black_list'].split(',')
    for BlackUser in BlackList:
        if MessageCheck.from_user.username == BlackUser:
            return False
            print(MessageCheck.from_user.username)
            print('False')
        else:
            return True
            print(MessageCheck.from_user.username)
            print('True')

@bot.message_handler(commands=['start'])
def send_start(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("🔄RESTART🔄", callback_data='restart_pc')
    item2 = types.InlineKeyboardButton("📍OFF📍", callback_data='off_pc')
    item3 = types.InlineKeyboardButton("🌐INTERNET🌐", callback_data='open_site') 
    item4 = types.InlineKeyboardButton("💻PROGRAM💻", callback_data='open_program') 

    markup.add(item1, item2)
    markup.add(item3, item4)
    
    bot.send_message(message.chat.id,'Hello, I,m create this is bot, to see the commands write / or tap on the button',reply_markup=markup)

@bot.message_handler(commands=['restart_pc'])
def RestartPc(message):
    if BlackListCheck(message):
        os.system('shutdown /r /t 0')
        dt_now = datetime.datetime.now()
        bot.send_message(message.chat.id,f'''PC RESTART_________
TIME: {dt_now.time()}
DATE: {datetime.date.today()}''')

@bot.message_handler(commands=['off_pc'])
def OffPc(message):
    if BlackListCheck(message):
        os.system('shutdown /s /t 0')
        dt_now = datetime.datetime.now()
        bot.send_message(message.chat.id,f'''PC OFF_________
TIME: {dt_now.time()}
DATE: {datetime.date.today()}''')

@bot.message_handler(commands=['open_program'])
def OpenProgram_and_Mp3(message):
    if BlackListCheck(message):
        global ValCommands,markup

        ValCommands = 'Open_program'

        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("💙Telegram💙", callback_data='Telegram')
        item2 = types.InlineKeyboardButton("💚WhatsApp💚", callback_data='WhatsApp')
        item3 = types.InlineKeyboardButton("💛❤️Yandex Music❤️💛", callback_data='Yandex_Music')
        item4 = types.InlineKeyboardButton("💜Discord💜", callback_data='Discord')
        item5 = types.InlineKeyboardButton("💬CMD💬", callback_data='Cmd')
        back = types.InlineKeyboardButton("⬅Game", callback_data='BackGame')
        next = types.InlineKeyboardButton("Program➡", callback_data='NextProgram')
        

        markup.add(item1, item2)
        markup.add(item3, item4)
        markup.add(item5)

        markup.add(back, next)
        bot.send_message(message.chat.id, 'SEND NAME PROGRAM', reply_markup=markup)

@bot.message_handler(commands=['open_site'])
def OpenSite(message):
    if BlackListCheck(message):
        global ValCommands
        ValCommands = 'OpenSite'

        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("🎷JazzRadio🎷", callback_data='JazzRadio')
        item2 = types.InlineKeyboardButton("👦RickRoll👦", callback_data='RickRoll')
        item3 = types.InlineKeyboardButton("❤️YouTube❤️", callback_data='youtube')
        item4 = types.InlineKeyboardButton("💜Twitch💜", callback_data='Twitch')

        markup.add(item1, item2)
        markup.add(item3, item4)
        bot.send_message(message.chat.id,'SEND NAME SITE', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    global markup
    try:
        if call.message:
            if call.data == 'restart_pc':
                RestartPc(call.message)
            if call.data == 'off_pc':
                OffPc(call.message)
            if call.data == 'open_program':
                OpenProgram_and_Mp3(call.message)
            if call.data == 'open_site':
                OpenSite(call.message)

            if call.data == 'JazzRadio':
                os.system(f'start http://prmstrm.1.fm:8000/ajazz')
            elif call.data == 'RickRoll':
                os.system(f'start https://www.youtube.com/watch?v=dQw4w9WgXcQ')
            elif call.data == 'youtube':
                os.system(f'start https://www.youtube.com/')
            elif call.data == 'Twitch':
                os.system(f'start https://www.twitch.tv/')

            elif call.data == 'Telegram':
                os.system(f'start C:/Users/Евгений/Desktop/Telegram.lnk')
            elif call.data == 'WhatsApp':
                os.system(f'start "" "C:/Users/Евгений/Desktop/WhatsApp.lnk"')
            elif call.data == 'Yandex_Music':
                os.system(f'start "" "C:/Users/Евгений/Desktop/Yandex.Music.lnk"')
            elif call.data == 'Discord':
                os.system(f'start "" "C:/Users/Евгений/Desktop/Discord.lnk"')
            elif call.data == 'Cmd':
                os.system(f'start "" "C:/Users/Евгений/Desktop/Console.lnk"')

            elif call.data == 'Photoshop':
                os.system(f'start "" "C:/Users/Евгений/Desktop/Photoshop.lnk"')
            elif call.data == 'PremierePro':
                os.system(f'start "" "C:/Users/Евгений/Desktop/PremierePro.lnk"')
            elif call.data == 'AfterEffects':
                os.system(f'start "" "C:/Users/Евгений/Desktop/AfterEffects.lnk"')
            elif call.data == 'Illustrator':
                os.system(f'start "" "C:/Users/Евгений/Desktop/Illustrator.lnk"')
            elif call.data == 'VisualStudio':
                os.system(f'start "" "C:/Users/Евгений/Desktop/VisualStudioCode.lnk"')

            elif call.data == 'BackGame':
                markup0 = types.InlineKeyboardMarkup()
                game1 = types.InlineKeyboardButton("💙Fortnite💙", callback_data='Fortnite')
                game2 = types.InlineKeyboardButton("💚🤎Minecraft🤎💚", callback_data='Minecraft')
                gamenext = types.InlineKeyboardButton("Message➡", callback_data='NextMessage')
                
                markup0.add(game1,game2)
                markup0.add(gamenext)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="SEND NAME PROGRAM", reply_markup=markup0)

            elif call.data == 'NextMessage':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="SEND NAME PROGRAM", reply_markup=markup)

            elif call.data == 'NextProgram':
                markup1 = types.InlineKeyboardMarkup()
                program1 = types.InlineKeyboardButton("💙Adobe Photoshop💙", callback_data='Photoshop')
                program2 = types.InlineKeyboardButton("💜Adobe Premiere Pro💜", callback_data='PremierePro')
                program3 = types.InlineKeyboardButton("💜Adobe After Effects💙", callback_data='AfterEffects')
                program4 = types.InlineKeyboardButton("🧡Adobe Illustrator🧡", callback_data='Illustrator')
                program5 = types.InlineKeyboardButton("💙Visual Studio Code💙", callback_data='VisualStudio')
                programback = types.InlineKeyboardButton("⬅Messanger", callback_data='NextMessage')
                

                markup1.add(program1,program2)
                markup1.add(program3,program4)
                markup1.add(program5)

                markup1.add(programback)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="SEND NAME PROGRAM", reply_markup=markup1)

    except Exception as e:
        print(repr(e))
@bot.message_handler(content_types=['text'])
def text_all(message):
    global ValCommands
    if ValCommands == 'Open_program':
        HVal1 = message.text
        os.system(f'start "" "C:/Users/Евгений/Desktop/{HVal1}" ')
        ValCommands = 'no_commands'
        bot.send_message(message.chat.id, f'PROGRAM "{HVal1}" STARTING')

    elif ValCommands == 'OpenSite':
        HVal2 = message.text
        ValCommands= 'no_commands'
        os.system(f'start http://{HVal2}')

        bot.send_message(message.chat.id, f'SITE-"{HVal2}" STARTING')
    else:
        bot.send_message(message.chat.id, 'is not command!')
bot.infinity_polling()
