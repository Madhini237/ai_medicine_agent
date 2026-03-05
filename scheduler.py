from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests

from database import get_all_medicines

BOT_TOKEN = "7989386136:AAGmix50sJzBY2hAKXNQHF4mOcKcKNYlBJU"


def send_message(chat_id, text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    requests.post(url, data=data)


def check_medicines():

    current_time = datetime.now().strftime("%H:%M")

    medicines = get_all_medicines()

    for chat_id, name, medicine, time in medicines:

        if current_time == time:

            message = f"Hi {name}, please take your {medicine}. Reply after taking."

            send_message(chat_id, message)


def start_scheduler():

    scheduler = BackgroundScheduler()

    scheduler.add_job(check_medicines, "interval", minutes=1)

    scheduler.start()