from telegram import *
from telegram.ext import *
import logging, time , requests, flask, threading
from multiprocessing import Process as pp

# You can add multiple chatids in the admins list to escape from getting the message limit

admins = ["Your Chat ID -> int", 1920911015]


# Your bot's token
key = "5364216031:AGXEuot4tJrjt_9x2KxkhPDF9eN9cuhaYM"
key = "5364216031:AAG4ZlxS4X9V602qvhH-RncAvFsGaXUp6ik"

# Logging what's happening
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


async def start_commmand(update:Update, context) -> None:
	msg = "Hello there!\nThis is the start command."
	await update.effective_message.reply_text(msg)



class Hello:
	# I'm skipping the __init__ functions for now. We don't need that here
	time_dict = {} # The dict where we'll keep track of user's limit


def can_message(chatid) -> bool:
	# No limit for admins :P
	if chatid in admins:
		return True
	
	the_dict = Hello.time_dict
	current_time = time.time()
	
	# If the chatid is not in the dict, it will through KeyError
	# So, using try except to escape that
	try:
		the_dict[chatid] # If this passes, the chatid is in the dict
	except:
		the_dict[chatid] = None # As the chatid is not in the list, putting the value as None
	
	if the_dict[chatid] == None:
		the_dict[chatid] = current_time
		return True
		
	else:
		if current_time - the_dict[chatid] >= 3: # If the difference between the last message is >= 3 seconds
			the_dict[chatid] = current_time
			return True
		else:
			return False






# Your function that you want to limit for normal users
async def cute_cats(update:Update, context) -> None:
	chatid = update.effective_user.id
	
	if can_message(chatid):
		# I'm just taking some data from an API
		req = requests.get("https://api.thecatapi.com/v1/images/search").json()[0]["url"]
		await context.bot.send_photo(chatid, req)
	else:
		await update.effective_message.reply_text("Calm down man... :')")




def main():
    app = ApplicationBuilder().token(key).build()
    
    # Command Handlers...
    start_h = CommandHandler("start", start_commmand, block=False)
    
    cat_h = CommandHandler("cat", cute_cats, block=False)
    app.add_handler(start_h)
    app.add_handler(cat_h)
    app.run_polling()



# Keep alive
app = flask.Flask(__name__)
@app.route('/')
def home():return "Alive on the mercy of Allah (SWT)"
def run():app.run(host='0.0.0.0',port=8080)
def keep_alive():t = threading.Thread(target = run);t.start()


if __name__ == "__main__":
	#keep_alive()
	pp(target=main).start()
