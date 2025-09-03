import json, os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATA_FILE = "data.json"

# Helpers
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Register Consumer Number", callback_data="register")],
        [InlineKeyboardButton("Bill Due Reminders", callback_data="reminder")],
        [InlineKeyboardButton("Quick Pay", url="https://www.tangedco.org")],
        [InlineKeyboardButton("Report Outage", callback_data="outage")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⚡ Welcome to TANGEDCO Helper!", reply_markup=reply_markup)

# Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "register":
        await query.edit_message_text("Please send me your Consumer Number.")
    elif query.data == "reminder":
        await query.edit_message_text("✅ Reminders will be sent (7/3/1 days before due date).")
    elif query.data == "outage":
        await query.edit_message_text("🚨 Power outage reported. ETA: 2 hours.")

# Save consumer number
async def save_consumer_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    consumer_number = update.message.text

    data = load_data()
    data[user_id] = consumer_number
    save_data(data)

    await update.message.reply_text(f"✅ Consumer Number {consumer_number} registered!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_consumer_number))
    app.run_polling()

if __name__ == "__main__":
    main()
