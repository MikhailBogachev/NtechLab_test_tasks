import telebot
import json
import os
import time
from pprint import pprint
TOKEN = ''
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'C:/Users/bogac/Desktop/pythonProject (копия)/images/' + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Обработка...")
    except Exception as e:
        bot.reply_to(message, e)

    import subprocess

    subprocess.Popen(['python', 'C:/Users/bogac/Desktop/pythonProject (копия)/process.py', 'images'])
    time.sleep(15)

    with open("C:/Users/bogac/Desktop/pythonProject (копия)/process_results.json", "r", encoding="utf-8") as file:
        text = json.load(file)
        bot.send_message(message.chat.id, 'Результат:')
        if 'female' in text.values():
            bot.send_message(message.chat.id, 'Женщина')
        else:
            bot.send_message(message.chat.id, 'Мужчина')

    folder = 'C:/Users/bogac/Desktop/pythonProject (копия)/images'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

bot.polling()
