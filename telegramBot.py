import os
import telebot
from telebot import types
import datetime
import configparser
import keyboard
config = configparser.ConfigParser()
ValCommands = 'no_commands'
config_path = 'C:/FESTASHKA/config.ini'
config.read(config_path)
TOKEN = config['Config']['TOKEN_BOT']
src = config['Settings']['default_path']
Error_permission = False

bot = telebot.TeleBot(TOKEN,parse_mode=None)


def BlackListCheck(MessageCheck):
    config.read(config_path)
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
    # markup = types.InlineKeyboardMarkup()
    # item1 = types.InlineKeyboardButton("🔄RESTART🔄", callback_data='restart_pc')
    # item2 = types.InlineKeyboardButton("📍OFF📍", callback_data='off_pc')
    # item3 = types.InlineKeyboardButton("🌐INTERNET🌐", callback_data='open_site') 
    # item4 = types.InlineKeyboardButton("💻PROGRAM💻", callback_data='open_program') 

    markup = types.ReplyKeyboardMarkup()
    item1 = types.KeyboardButton("🔄RESTART🔄")
    item2 = types.KeyboardButton("📍OFF📍")
    item3 = types.KeyboardButton("🌐INTERNET🌐") 
    item4 = types.KeyboardButton("💻PROGRAM💻") 
    item5 = types.KeyboardButton("📦FOLDER_MANAGER📦") 
    item6 = types.KeyboardButton("📔KEYBOARD_SHORTCUP📔") 

    markup.add(item1, item2)
    markup.add(item3, item4)
    markup.add(item6)
    markup.add(item5)

    
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
        # global ValCommands,markup
        # ValCommands = 'Open_program'
        global markup

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
        # global ValCommands
        # ValCommands = 'OpenSite'

        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("🎷JazzRadio🎷", callback_data='JazzRadio')
        item2 = types.InlineKeyboardButton("👦RickRoll👦", callback_data='RickRoll')
        item3 = types.InlineKeyboardButton("❤️YouTube❤️", callback_data='youtube')
        item4 = types.InlineKeyboardButton("💜Twitch💜", callback_data='Twitch')

        markup.add(item1, item2)
        markup.add(item3, item4)
        bot.send_message(message.chat.id,'SEND NAME SITE', reply_markup=markup)

def can_access(path: str) -> bool:
    """Check if we can access folder on network drive"""
    try:
        os.listdir(path)
        return True
    except PermissionError:
        return False

@bot.message_handler(commands=['open_folders_manager'])
def Folders_manager(message):
    global ValCommands,src,Error_permission
    ValCommands = 'folders_manager'

    if src == 'C://':
        src = 'C:/'
    
    # dirt_folders = os.listdir(src)
    folders = os.listdir(src)
    # for iD in range(len(dirt_folders)):
    #     if dirt_folders[iD] in '.':
    #         if can_access(path=src+dirt_folders[iD]):
    #             folders.append(dirt_folders[iD])

    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row_width = 2

    for i in range(0, len(folders)):
        print(folders[i])
        keyboard.add(types.KeyboardButton(folders[i]))
        
    if src == 'C:/':
        keyboard.add(types.KeyboardButton('❌'))
    else:
        keyboard.add(types.KeyboardButton('👈'),types.KeyboardButton('❌'))
    bot.send_message(message.chat.id, f'- {src} -', reply_markup=keyboard)

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
                
            elif call.data == 'win+d':
                keyboard.send("windows+d")
            elif call.data == 'win+l':
                keyboard.send("windows+l")
            elif call.data == 'alt+tab':
                keyboard.send("alt+tab")
            elif call.data == 'alt+F4':
                keyboard.send("alt+F4")
    except Exception as e:
        print(repr(e))

@bot.message_handler(commands=['Keyboard_shortcup'])
def Keyboard_shortcup(message):
    markup = types.InlineKeyboardMarkup()
    item_1 = types.InlineKeyboardButton('WIN + D', callback_data='win+d')
    item_2 = types.InlineKeyboardButton('WIN + L', callback_data='win+l')
    item_3 = types.InlineKeyboardButton('ALT + TAB', callback_data='alt+tab')
    item_4 = types.InlineKeyboardButton('ALT + F4', callback_data='alt+F4')
    markup.add(item_1,item_2)
    markup.add(item_3,item_4)
    bot.send_message(message.chat.id, 'KEYBOARD_SHORTCUP',reply_markup=markup)

@bot.message_handler(content_types=['text'])
def text_all(message):
    global ValCommands,src,Error_permission
    if message.text == "🔄RESTART🔄":
        RestartPc(message)
    elif message.text == "📍OFF📍":
        OffPc(message)
    elif message.text == "🌐INTERNET🌐":
        OpenSite(message)
    elif message.text == "📔KEYBOARD_SHORTCUP📔":
        Keyboard_shortcup(message)
    elif message.text == "💻PROGRAM💻":
        OpenProgram_and_Mp3(message)
    elif message.text == "📦FOLDER_MANAGER📦":
        Folders_manager(message)

    elif ValCommands == 'folders_manager':
        if message.text == '📦FOLDER_MANAGER📦':
            pass
        elif message.text == '❌':
            bot.send_message(message.chat.id, f'- END SRC {src} -')
            ValCommands = 'no_commands'

            config.read(config_path)
            src = config['Settings']['default_path']

            send_start(message)
        elif message.text == '👈':
            src_list = src.split('/')
            src_list.pop()
            src_list.pop()
            print(src_list)
            for i in range(len(src_list)):
                if i == 0:
                    src = ''
                src += src_list[i]  + '/'
            Folders_manager(message)
        elif '.txt' in message.text or '.ini' in message.text or '.md' in message.text:
            print('-----text')
            f = open(f'{src}{message.text}','r', encoding='utf-8')
            bot.send_message(message.chat.id, f'- {message.text} -\n {f.read()}')
        
        elif '.exe' in message.text or '.lnk' in message.text or '.url' in message.text:
            print('-----program')
            os.system(f'start {src}{message.text}')
            bot.send_message(message.chat.id, f'- OPEN {message.text} -')

        elif '.png' in message.text or '.jpg' in message.text or '.webp' in message.text :
            print('-----img')
            bot.send_message(message.chat.id,f'- Идет загрузка файла {message.text} -')
            bot.send_photo(message.chat.id, photo=open(f'{src}{message.text}', 'rb'))
        
        elif '.mp3' in message.text or '.wav' in message.text:
            print('-----music')
            bot.send_message(message.chat.id,f'- Идет загрузка файла {message.text} -')
            bot.send_audio(message.chat.id, open(f'{src}{message.text}', 'rb'))
            
        elif '.js' in message.text or '.htm' in message.text or '.py' in message.text or '.css' in message.text or '.xml' in message.text or '.zip' in message.text or '.rar' in message.text or '.svg' in message.text or '.spec' in message.text or '.blend1' in message.text or '.sys' in message.text or '.DAT' in message.text or '.tmp' in message.text or '.log' in message.text:
            bot.send_message(message.chat.id, f'- Этот формат файлов пока не поддерживается -')
        else:
            print(Error_permission)
            if Error_permission == False:
                print('-----folder')
                src = src + message.text + '/'
                Folders_manager(message)
            else:
                Folders_manager(message)

    elif ValCommands == 'Open_program':
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
