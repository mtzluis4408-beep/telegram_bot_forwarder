import telebot
from telebot import types
from datetime import datetime
from flask import Flask
import threading

# ========== CONFIGURACIÓN ==========
BOT_TOKEN = "8061825899:AAH-659ved1d3M-7Vc4vtvTrZRxzkSJ0x7Y"
GROUP_A_ID = -1003187194418
CHANNEL_ID = -1003302077685

bot = telebot.TeleBot(BOT_TOKEN)

# ========== WEB SERVER PARA RENDER ==========
app = Flask(__name__)

@app.get("/")
def home():
    return "Bot corriendo correctamente en Render!"

def start_web():
    app.run(host="0.0.0.0", port=10000)

@app.get("/ping")
def ping():
    return "pong", 200

# ========== FUNCION DE REENVÍO ==========
def safe_forward(message: types.Message):
    try:
        bot.forward_message(
            chat_id=CHANNEL_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        print(f"Reenviado: {message.message_id}")
        return True
    except Exception as e:
        print("Error:", e)
        return False

# ========== MANEJADOR /refe ==========
@bot.message_handler(commands=['refe'])
def refe_handler(message: types.Message):

    if message.chat.id != GROUP_A_ID:
        bot.reply_to(message, "⚠ Solo funciona en el grupo VIP.")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠ Debes responder a un mensaje con /refe.")
        return

    success = safe_forward(message.reply_to_message)
    bot.reply_to(message, "✅ Refe enviada" if success else "✅ Refe enviada")
# ========== test /test ==========
@bot.message_handler(commands=['test'])
def test(message):
    try:
        bot.forward_message(
            chat_id=CHANNEL_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        bot.reply_to(message, "Reenvío OK")
    except Exception as e:
        bot.reply_to(message, f"ERROR: {e}")
# ========== INICIO ==========
def start_bot():
    print("🤖 Bot iniciando en Render FREE...")
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    # Crear hilo separando el bot y el servidor web
    threading.Thread(target=start_bot).start()
    start_web()
