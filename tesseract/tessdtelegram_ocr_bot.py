import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image
import pytesseract
import os

# Optional: Tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔐 Replace with your bot token from BotFather
TOKEN = "8155659073:AAEQ7TOesJ9ukCc9Naq1iY4F63JP7RU-_Mk"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Send me a photo with Khmer text and I will extract it.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("📷 Just send an image with Khmer text!")

def handle_photo(update: Update, context: CallbackContext):
    photo_file = update.message.photo[-1].get_file()
    image_path = f"temp_{update.message.chat.id}.jpg"
    photo_file.download(image_path)

    try:
        text = pytesseract.image_to_string(Image.open(image_path), lang='khm')
        if text.strip():
            update.message.reply_text("📝 Extracted Khmer Text:\n\n" + text)
        else:
            update.message.reply_text("😥 No readable Khmer text found.")
    except Exception as e:
        logger.error(f"OCR error: {e}")
        update.message.reply_text("⚠️ Error processing image.")
    finally:
        os.remove(image_path)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
