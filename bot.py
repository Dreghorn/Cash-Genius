import telegram.ext

Token = "5900385828:AAETyA08oV2hGinvkDs8-zkUksIAzJGqpks"

updater = telegram.ext.Updater("5900385828:AAETyA08oV2hGinvkDs8-zkUksIAzJGqpks", use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    update.message.reply_text("Hello! Welcome to Cash Genius! Click /help")

def help(update, context):
    update.message.reply_text(
        """
        The following commands are available: 

        /start -> Welcome to the channel
        /help -> This message
        /content -> what you can do here
        /checkthework -> перевірити чи працює
        /contacts -> our contacts
        
        """)
    
def content(update, context):
    update.message.reply_text("Here you will play the game!")

def checkthework(update, context):
    update.message.reply_text("If you see this link, it works! https://youtu.be/dQw4w9WgXcQ")

def contacts(update, context):
    update.message.reply_text("Проджект менеджер	styur555@gmail.com\nBack Dev	yuliiazhosan@gmail.com\nBack Lead	Lytnev2001@gmail.com\nProject manager Site	Anni0112@icloud.com\nFrontend Developer	elenatishko1@gmail.com\nProject Manager Bot	kachanova.viktoria@gmail.com\nMentor	bandydan@gmail.com\nQA Engineer	denyscr994@gmail.com\nBack Lead	mykyta.cherpakov@gmail.com\nContent + QA Lead	helltarasova@gmail.com\nFrontend Developer	grechkosey.n@gmail.com\nФронтенд лід	alex.koniushenko@gmail.com\nUI/UX designer	olyagiruk@gmail.com\nQA Engineer	natakostyk33@gmail.com")

dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.CommandHandler('content', content))
dispatcher.add_handler(telegram.ext.CommandHandler('checkthework', checkthework))
dispatcher.add_handler(telegram.ext.CommandHandler('contacts', contacts))
dispatcher.add_handler(telegram.ext.CommandHandler('help', help))


updater.start_polling()
updater.idle()