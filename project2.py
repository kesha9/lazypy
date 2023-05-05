import os
import pyowm
import telebot
from dotenv import load_dotenv


load_dotenv()

OWM_API_KEY = os.getenv("OWM_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

owm = pyowm.OWM(OWM_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def send_echo(message):
    try:
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temp = w.temperature('celsius')["temp"]

        answer = f"in {message.text} now: {w.detailed_status}\n"
        answer += f"temperature now: {temp}°C\n\n"

        if temp < 10:
            answer += "It's very cold now, so dress warmer"
        elif temp < 20:
            answer += "It's warmer now, you can dress for spring"
        else:
            answer += "The weather is very nice now! Take a walk :)"

        bot.send_message(message.chat.id, answer)

    except pyowm.commons.exceptions.NotFoundError:
        bot.send_message(message.chat.id, "Sorry, I couldn't find that location. Please try again.")

bot.polling(none_stop=True)
