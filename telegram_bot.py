from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from database import add_patient, get_patient, add_medicine
from llm_handler import understand_reply

BOT_TOKEN = "7989386136:AAGmix50sJzBY2hAKXNQHF4mOcKcKNYlBJU"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to AI Medicine Reminder Bot\n\n"
        "/register to register\n"
        "/addmedicine to add medicine"
    )


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["register"] = True
    await update.message.reply_text("Enter your name")


async def add_medicine_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["add_med"] = True
    await update.message.reply_text("Enter medicine name")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    chat_id = str(update.message.chat_id)

    # Registration flow
    if context.user_data.get("register"):

        if "name" not in context.user_data:
            context.user_data["name"] = text
            await update.message.reply_text("Enter disease type")
            return

        else:
            name = context.user_data["name"]
            disease = text

            add_patient(name, chat_id, disease)

            context.user_data.clear()

            await update.message.reply_text("Registration successful")
            return

    # Add medicine flow
    if context.user_data.get("add_med"):

        if "medicine" not in context.user_data:

            context.user_data["medicine"] = text
            await update.message.reply_text("Enter reminder time (HH:MM)")
            return

        else:

            medicine = context.user_data["medicine"]
            time = text

            patient = get_patient(chat_id)

            if patient:

                patient_id = patient[0]
                add_medicine(patient_id, medicine, time)

                await update.message.reply_text("Medicine added")

            else:
                await update.message.reply_text("Please register first")

            context.user_data.clear()
            return

    # AI understanding reply
    result = understand_reply(text)

    await update.message.reply_text(f"Reply understood as: {result}")


def run_bot():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("addmedicine", add_medicine_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.run_polling()