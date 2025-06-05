import pyotp
from pyzbar.pyzbar import decode
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re

user_secrets = {}  # Store users' Secret Keys

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 សួស្តី! ផ្ញើរូប QR code ឬសរសេរ Secret Key!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    file_path = "qr_code.png"
    await file.download_to_drive(file_path)

    qr_data = decode(Image.open(file_path))
    if qr_data:
        uri = qr_data[0].data.decode()
        match = re.search(r'secret=([A-Z0-9]+)', uri)
        if match:
            secret = match.group(1)
            user_secrets[update.effective_user.id] = secret
            await update.message.reply_text(f"✅ Secret Key របស់អ្នក៖ `{secret}`", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ មិនអាចរកបាន Secret Key ពី QR នេះទេ។")
    else:
        await update.message.reply_text("❌ មិនអាចអាន QR Code បានទេ។")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    if re.fullmatch(r'[A-Z2-7]{16,}', text):
        user_secrets[update.effective_user.id] = text
        await update.message.reply_text("✅ បានរក្សាទុក Secret Key! សាកល្បង /code")
    else:
        await update.message.reply_text("📌 បញ្ចូល Secret Key មិនត្រឹមត្រូវ។")

async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_secrets:
        await update.message.reply_text("⚠️ សូមផ្ញើ Secret Key ជាមុនសិន។")
        return
    secret = user_secrets[user_id]
    otp = pyotp.TOTP(secret)
    await update.message.reply_text(f"🔐 2FA Code៖ `{otp.now()}`", parse_mode="Markdown")

import os
bot_token = os.environ.get("BOT_TOKEN")  # <-- Load from env variable
app = ApplicationBuilder().token(bot_token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("code", code))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

app.run_polling()
