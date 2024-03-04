import aiogram
from aiogram import Bot, Dispatcher, executor, types
import datetime
import configparser
import os
import subprocess 




config = configparser.ConfigParser()
config_path = 'C:/FESTASHKA/config.ini'
ValCommands = 'no_commands'
config.read(config_path)
TOKEN = config['Config']['TOKEN_BOT']
src = config['Settings']['default_path']
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def BlackListCheck(MessageCheck):
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

@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    item1 = types.KeyboardButton("🔄RESTART🔄")
    item2 = types.KeyboardButton("📍OFF📍")
    item3 = types.KeyboardButton("🌐INTERNET🌐") 
    item4 = types.KeyboardButton("💻PROGRAM💻") 
    item5 = types.KeyboardButton("📦FOLDER_MANAGER📦") 

    markup.add(item1, item2)
    markup.add(item3, item4)
    markup.add(item5)

    await bot.send_message(message.chat.id,'Hello, I,m create this is bot, to see the commands write / or tap on the button',reply_markup=markup)


async def RestartPc(message):
    if await BlackListCheck(message):
        os.system('shutdown /r /t 0')
        dt_now = datetime.datetime.now()
        await bot.send_message(message.chat.id,f'''PC RESTART_________
TIME: {dt_now.time()}
DATE: {datetime.date.today()}''')
        
async def OffPc(message):
    if await BlackListCheck(message):
        os.system('shutdown /s /t 0')
        dt_now = datetime.datetime.now()
        await bot.send_message(message.chat.id,f'''PC OFF_________
TIME: {dt_now.time()}
DATE: {datetime.date.today()}''')
        
async def OpenSite(message):
    global ValCommands
    if await BlackListCheck(message):
        ValCommands = 'OpenSite'
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("🎷JazzRadio🎷", callback_data='JazzRadio')
        item2 = types.InlineKeyboardButton("👦RickRoll👦", callback_data='RickRoll')
        item3 = types.InlineKeyboardButton("❤️YouTube❤️", callback_data='youtube')
        item4 = types.InlineKeyboardButton("💜Twitch💜", callback_data='Twitch')

        markup.add(item1, item2)
        markup.add(item3, item4)
        await bot.send_message(message.chat.id,'SEND NAME SITE', reply_markup=markup)

async def OpenProgram_and_Mp3(message):
    if await BlackListCheck(message):
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
        await bot.send_message(message.chat.id, 'SEND NAME PROGRAM', reply_markup=markup)

@dp.message_handler(commands=['open_folders_manager'])
async def Folders_manager(message):
    if await BlackListCheck(message):
        global ValCommands,src
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
            keyboard.add(types.KeyboardButton('📁'),types.KeyboardButton('❌'))
        else:
            keyboard.add(types.KeyboardButton('👈'),types.KeyboardButton('📁'),types.KeyboardButton('❌'))
        await bot.send_message(message.chat.id, f'- {src} -', reply_markup=keyboard)

@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    global ValCommands,src

    if message.text == '🔄RESTART🔄':
        await RestartPc(message)
    elif message.text == '📍OFF📍':
        await OffPc(message)
    elif message.text == '🌐INTERNET🌐':
        await OpenSite(message)
    elif message.text == '💻PROGRAM💻':
        await OpenProgram_and_Mp3(message)
    elif message.text == '📦FOLDER_MANAGER📦':
        await Folders_manager(message)

    elif ValCommands == 'folders_manager':
        if message.text == '📦FOLDER_MANAGER📦':
            pass
        elif message.text == '❌':
            await bot.send_message(message.chat.id, f'- END SRC {src} -')
            ValCommands = 'no_commands'

            config.read(config_path)
            src = config['Settings']['default_path']
            await send_start(message)

        elif message.text == '📁':
            subprocess.Popen(f'explorer "{src}"') 
        elif message.text == '👈':
            src_list = src.split('/')
            src_list.pop()
            src_list.pop()
            print(src_list)
            for i in range(len(src_list)):
                if i == 0:
                    src = ''
                src += src_list[i]  + '/'
            await Folders_manager(message)
        elif '.txt' in message.text or '.ini' in message.text or '.md' in message.text or '.log' in message.text:
            print('-----text')
            f = open(f'{src}{message.text}','r', encoding='utf-8')
            await bot.send_message(message.chat.id, f'- {message.text} -\n {f.read()}')
        
        elif '.exe' in message.text or '.lnk' in message.text or '.url' in message.text:
            print('-----program')
            os.system(f'start {src}{message.text}')
            await bot.send_message(message.chat.id, f'- OPEN {message.text} -')

        elif '.png' in message.text or '.jpg' in message.text or '.webp' in message.text :
            print('-----img')
            await bot.send_message(message.chat.id,f'- Идет загрузка файла {message.text} -')
            await bot.send_photo(message.chat.id, photo=open(f'{src}{message.text}', 'rb'))
        
        elif '.mp3' in message.text or '.wav' in message.text:
            print('-----music')
            await bot.send_message(message.chat.id,f'- Идет загрузка файла {message.text} -')
            await bot.send_audio(message.chat.id, open(f'{src}{message.text}', 'rb'))
            
        elif '.js' in message.text or '.htm' in message.text or '.py' in message.text or '.css' in message.text or '.xml' in message.text or '.zip' in message.text or '.rar' in message.text or '.svg' in message.text or '.spec' in message.text or '.blend1' in message.text or '.sys' in message.text or '.DAT' in message.text or '.tmp' in message.text or '.log' in message.text:
            await bot.send_message(message.chat.id, f'- Этот формат файлов пока не поддерживается -')
        
        else:
            print('-----folder')
            src = src + message.text + '/'
            await Folders_manager(message)

    elif ValCommands == 'Open_program':
        HVal1 = message.text
        os.system(f'start "" "C:/Users/Евгений/Desktop/{HVal1}" ')
        ValCommands = 'no_commands'
        await bot.send_message(message.chat.id, f'PROGRAM "{HVal1}" STARTING')

    elif ValCommands == 'OpenSite':
        HVal2 = message.text
        ValCommands= 'no_commands'
        os.system(f'start https://{HVal2}')

        await bot.send_message(message.chat.id, f'SITE-"{HVal2}" STARTING')
    else:
        await bot.send_message(message.chat.id, 'is not command!')

@dp.callback_query_handler(lambda c: c.data == 'JazzRadio')
async def JazzRadio(call: types.CallbackQuery, **kwargs):
    os.system(f'start http://prmstrm.1.fm:8000/ajazz')
    
@dp.callback_query_handler(lambda c: c.data == 'RickRoll')
async def RickRoll(call: types.CallbackQuery, **kwargs):
    os.system(f'start https://www.youtube.com/watch?v=dQw4w9WgXcQ')

@dp.callback_query_handler(lambda c: c.data == 'youtube')
async def Youtube(call: types.CallbackQuery):
    os.system(f'start https://www.youtube.com/')

@dp.callback_query_handler(lambda c: c.data == 'Twitch')
async def Twitch(call: types.CallbackQuery):
    os.system(f'start https://www.twitch.tv/')

# Program _-----------------_-------------------_--------------------_--------------_----------------_---------------_------------------_
@dp.callback_query_handler(lambda c: c.data == 'NextMessage')
async def NextMessage(call: types.CallbackQuery):
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
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="SEND NAME PROGRAM", reply_markup=markup)
    
@dp.callback_query_handler(lambda c: c.data == 'BackGame')
async def BackGame(call: types.CallbackQuery):
    markup0 = types.InlineKeyboardMarkup()
    game1 = types.InlineKeyboardButton("💙Fortnite💙", callback_data='Fortnite')
    game2 = types.InlineKeyboardButton("💚🤎Minecraft🤎💚", callback_data='Minecraft')
    gamenext = types.InlineKeyboardButton("Message➡", callback_data='NextMessage')
                
    markup0.add(game1,game2)
    markup0.add(gamenext)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="SEND NAME PROGRAM", reply_markup=markup0)

@dp.callback_query_handler(lambda c: c.data == 'NextProgram')
async def NextProgram(call: types.CallbackQuery):
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
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="SEND NAME PROGRAM", reply_markup=markup1)

@dp.callback_query_handler(lambda c: c.data == "Telegram")
async def Telegram(call: types.CallbackQuery):
    os.system(f'start C:/Users/Евгений/Desktop/Telegram.lnk')
@dp.callback_query_handler(lambda c: c.data == "WhatsApp")
async def WhatsApp(call: types.CallbackQuery):
    os.system(f'start "" "C:/Users/Евгений/Desktop/WhatsApp.lnk"')
@dp.callback_query_handler(lambda c: c.data == "Yandex_Music")
async def Yandex_Music(call: types.CallbackQuery):
    os.system(f'start "" "C:/Users/Евгений/Desktop/Yandex.Music.lnk"')
@dp.callback_query_handler(lambda c: c.data == "Discord")
async def Discord(call: types.CallbackQuery):
    os.system(f'start "" "C:/Users/Евгений/Desktop/Discord.lnk"')
@dp.callback_query_handler(lambda c: c.data == "Cmd")
async def Cmd(call: types.CallbackQuery):
    os.system(f'start "" "C:/Users/Евгений/Desktop/Console.lnk"')
@dp.callback_query_handler(lambda c: c.data == "Fortnite")
async def Fortnite(call: types.CallbackQuery):
    pass
@dp.callback_query_handler(lambda c: c.data == "Minecraft")
async def Minecraft(call: types.CallbackQuery):
    pass
@dp.callback_query_handler(lambda c: c.data == "Photoshop")
async def Photoshop(call: types.CallbackQuery):
    os.system(f'start "" "C:/Users/Евгений/Desktop/Photoshop.lnk"')
@dp.callback_query_handler(lambda c: c.data == "PremierePro")
async def PremierePro(call: types.CallbackQuery):
    os.system(f'start "" "C:/Users/Евгений/Desktop/PremierePro.lnk"')
@dp.callback_query_handler(lambda c: c.data == "AfterEffects")
async def AfterEffects(call: types.CallbackQuery):
    os.system(f'start "" "C:/Users/Евгений/Desktop/AfterEffects.lnk"')
@dp.callback_query_handler(lambda c: c.data == "Illustrator")
async def Illustrator(call: types.CallbackQuery):
    os.system(f'start "" "C:/Users/Евгений/Desktop/Illustrator.lnk"')
@dp.callback_query_handler(lambda c: c.data == "VisualStudio")
async def VisualStudio(call: types.CallbackQuery):
    os.system(f'start "" "C:/Users/Евгений/Desktop/VisualStudioCode.lnk"')

if __name__ == '__main__':
    executor.start_polling(dp)