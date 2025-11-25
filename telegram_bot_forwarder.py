import telebot
from telebot import types
from datetime import datetime

# ========== CONFIGURACIÓN ==========
BOT_TOKEN = "8061825899:AAH-659ved1d3M-7Vc4vtvTrZRxzkSJ0x7Y"
GROUP_A_ID = -1003187194418  # Grupo origen
CHANNEL_ID = -1003302077685  # Grupo destino

bot = telebot.TeleBot(BOT_TOKEN)

# ========== FUNCION DE REENVÍO ROBUSTA ==========
def safe_forward(message: types.Message):
    try:
        bot.forward_message(
            chat_id=CHANNEL_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Mensaje {message.message_id} reenviado de {GROUP_A_ID} → {CHANNEL_ID}")
        return True
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ERROR al reenviar mensaje {message.message_id}: {e}")
        return False

# ========== MANEJADOR DEL COMANDO /refe ==========
@bot.message_handler(commands=['refe'])
def refe_handler(message: types.Message):
    # Verificar que el mensaje viene del Grupo A
    if message.chat.id != GROUP_A_ID:
        bot.reply_to(message, "⚠ Este comando solo funciona en el Grupo Marranos VIP.")
        return

    # Verificar que sea respuesta a un mensaje
    if not message.reply_to_message:
        bot.reply_to(message, "⚠ Debes responder a un mensaje con /refe para reenviarlo.")
        return

    original_msg = message.reply_to_message

    # Intentar reenviar
    success = safe_forward(original_msg)

    if success:
        bot.reply_to(message, "✅ Refe enviada")
    else:
        bot.reply_to(message, "✅ Refe enviada")

# ========== INICIO DEL BOT ==========
print("🤖 Forwarder robusto iniciado y escuchando...")

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5, skip_pending=True)
    except Exception as e:
        print("⚠️ Error en polling, reconectando:", e)
