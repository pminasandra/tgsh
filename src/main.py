import os
import config
import glob

from telegram.ext import Updater, Dispatcher, CommandHandler, Filters
import telegram

from system_navigation import *
from config import *
import cam_mic_access


def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Greetings {}. {} is up and running.".format(EMPLOYER_FIRST_NAME, SECRETARY_NAME))
        context.bot.send_message(chat_id=update.effective_chat.id, text=pstring())
        print(update.message.from_user['username'], update.message.text)
#        context.bot.send_message(chat_id=update.effective_chat.id, text=pstring(BOT_CWD))

def cd(update, context):
        print(update.message.from_user['username'], update.message.text)
        try:
                context.bot.send_message(chat_id=update.effective_chat.id, text=change_dir(" ".join(context.args)))
                context.bot.send_message(chat_id=update.effective_chat.id, text=pstring())
 #               context.bot.send_message(chat_id=update.effective_chat.id, text=pstring(BOT_CWD))
        except Exception as e:
                context.bot.send_message(chat_id=update.effective_chat.id, text=e)
                context.bot.send_message(chat_id=update.effective_chat.id, text=pstring())
  #              context.bot.send_message(chat_id=update.effective_chat.id, text=pstring(BOT_CWD))

def main_ls(update, context):
        print(update.message.from_user['username'], update.message.text)
        full_str = " ".join(context.args)
        queries = [x.replace("%&%", " ") for x in full_str.replace("\ ", "%&%").split()]
        context.bot.send_message(chat_id=update.effective_chat.id, text=ls(*queries), parse_mode=telegram.ParseMode.HTML)
        context.bot.send_message(chat_id=update.effective_chat.id, text=pstring())

def main_get(update, context):
        print(update.message.from_user['username'], update.message.text)
        full_str = " ".join(context.args)
        queries = [x.replace("%&%", " ") for x in full_str.replace("\ ", "%&%").split()]
        Result_str, Results_list = get(*queries)

        context.bot.send_message(chat_id = update.effective_chat.id, text=Result_str)
        for File in Results_list:
                context.bot.send_chat_action(chat_id = update.effective_chat.id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
                print("Sending file", File)
                context.bot.send_document(chat_id=update.effective_chat.id, document=open(File, 'rb'), filename=os.path.basename(File), caption=os.path.basename(File))
        context.bot.send_message(chat_id=update.effective_chat.id, text=pstring())

def cam_access(update, context):
        print(update.message.from_user['username'], update.message.text)
        caption, img = cam_mic_access.take_pic()

        context.bot.send_chat_action(chat_id = update.effective_chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
        print("Sending a webcam capture")
        context.bot.send_photo(chat_id = update.effective_chat.id, photo=img, caption=caption)
        context.bot.send_message(chat_id=update.effective_chat.id, text=pstring())

if __name__ == "__main__":
        ud = Updater(token=BOT_TOKEN, use_context=True)
        start_handler = CommandHandler('start', start, Filters.user(username="@"+TG_USERNAME))
        cd_handler = CommandHandler('cd', cd, Filters.user(username="@"+TG_USERNAME))
        ls_handler = CommandHandler('ls', main_ls, Filters.user(username="@"+TG_USERNAME))
        get_handler = CommandHandler('get', main_get, Filters.user(username="@"+TG_USERNAME))
        pic_handler = CommandHandler('pic', cam_access, Filters.user(username="@"+TG_USERNAME))
        ud.dispatcher.add_handler(start_handler)
        ud.dispatcher.add_handler(cd_handler)
        ud.dispatcher.add_handler(ls_handler)
        ud.dispatcher.add_handler(get_handler)
        ud.dispatcher.add_handler(pic_handler)
        ud.start_polling()
