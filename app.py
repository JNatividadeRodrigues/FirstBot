from flask import Flask,request
import telegram
from telebot.credentials import bot_token,bot_user_name,URL
import re

global BOT
global TOKEN
TOKEN = bot_token
bot =telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN),methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True),BOT)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    text = update.message.text.encode('utf-8').decode()
    if text == "/start":
        bot_welcome = "Welcome to your first telegram bot"
    
        bot.sendMessage(chat_id=chat_id,text=bot_welcome,reply_to_message_id=msg_id)
    else:
        try:
            text= re.sub(r"\W","_",text)
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
            bot.sendPhoto(chat_id=chat_id,photo=url,reply_to_message_id=msg_id)
        except Exception:
            bot.sendMessage(chat_id=chat_id,text="There was a problem with the name you used, please enter diferent name",reply_to_message=msg_id)
    return "ok"

@app.route('/set_webhook',methods=['GET','POST'])
def set_webhook():
    s= BOT.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "Webhook setup Ok"
    else:
        return "WebHook setup Failed"


@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)