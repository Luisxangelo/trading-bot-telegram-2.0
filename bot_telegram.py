from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)
from datetime import date

# ================= CONFIGURACIÓN =================

TOKEN = "8529903726:AAEU7BLVq_3wMSCbU_Fve4kPfoXSVRADS-8"

BINANCE_REF = "https://accounts.binance.com/register?ref=ROZTAFCJ"

CANAL_FREE = "-1003648632391"
CANAL_VIP = "-1003504953186"  # ID del canal privado VIP

ADMIN_IDS = [5297138695]  # TU ID DE TELEGRAM

MAX_FREE_PER_DAY = 2
MAX_VIP_PER_DAY = 10

# ================= CONTADORES =================

signal_counter = {
    "date": date.today(),
    "free": 0,
    "vip": 0
}

def reset_if_new_day():
    today = date.today()
    if signal_counter["date"] != today:
        signal_counter["date"] = today
        signal_counter["free"] = 0
        signal_counter["vip"] = 0

# ================= TECLADO PRINCIPAL =================

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("ℹ️ Cómo funciona", callback_data="info")],
        [InlineKeyboardButton("📈 Canal FREE", url="https://t.me/CryptoSignalsPro_Free")],
        [InlineKeyboardButton("💎 Canal VIP", url="https://t.me/+V3bKF5RumKNmYzJh")],
        [InlineKeyboardButton("🟡 Registrarme en Binance", callback_data="tutorial_binance")],
        [InlineKeyboardButton("📜 Reglas del Sistema", callback_data="rules")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dashboard_text = (
        "🟢─────────────────────────────🟢\n"
        "🤖 *Bienvenido al Sistema de Trading Automático*\n"
        "🟢─────────────────────────────🟢\n\n"
        "*📊 Estado del Sistema:*\n"
        "✅ Señales confiables y educativas\n"
        "✅ Para todos los niveles de traders\n"
        "❌ Resultados pasados no garantizan resultados futuros\n\n"
        "*💹 Canales de Señales:*\n"
        "📈 FREE: 1–2 señales diarias ✅\n"
        "💎 VIP: Hasta 10 señales diarias + análisis avanzado ✅\n\n"
        "*⚡ Pasos para interactuar:*\n"
        "1️⃣ Registrarte en Binance 🟡\n"
        "2️⃣ Elegir el canal que quieras seguir\n"
        "3️⃣ Revisar reglas y funcionamiento\n\n"
        "*💡 Tips Rápidos:*\n"
        "✅ Usa Stop Loss siempre\n"
        "✅ No arriesgues más del 1–2%\n"
        "❌ No operes si no entiendes la señal\n\n"
        "👇 *Usa los botones para empezar*"
    )

    await update.message.reply_text(
        dashboard_text,
        reply_markup=main_keyboard(),
        parse_mode="Markdown"
    )

# ================= REGLAS =================

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "📜 *REGLAS DEL SISTEMA*\n\n"
        "1️⃣ Las señales son educativas\n"
        "2️⃣ Usa SIEMPRE Stop Loss\n"
        "3️⃣ No arriesgues más del 1–2%\n"
        "4️⃣ No operes si no entiendes la señal\n"
        "5️⃣ Resultados pasados no garantizan resultados futuros\n\n"
        "⚠️ Cada usuario es responsable de su capital"
    )
    await query.edit_message_text(text, parse_mode="Markdown")

# ================= INFO =================

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "ℹ️ *¿CÓMO FUNCIONA EL SISTEMA?*\n\n"
        "📊 Analizamos múltiples pares en Binance Futures\n"
        "🤖 Sistema automático detecta oportunidades\n"
        "📨 Señales enviadas al canal\n\n"
        "🔹 FREE: 1–2 señales diarias\n"
        "🔹 VIP: Hasta 10 señales diarias\n\n"
        "💡 Tú decides si ejecutas"
    )
    await query.edit_message_text(text, parse_mode="Markdown")

# ================= BINANCE TUTORIAL =================

async def tutorial_binance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        f"🟡 Regístrate en Binance aquí:\n\n{BINANCE_REF}",
        parse_mode="Markdown"
    )

# ================= ENVÍO DE SEÑALES =================

async def send_free(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    reset_if_new_day()

    if signal_counter["free"] >= MAX_FREE_PER_DAY:
        await update.message.reply_text("❌ Límite diario FREE alcanzado")
        return

    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("⚠️ Usa: /send_free TEXTO")
        return

    await context.bot.send_message(chat_id=CANAL_FREE, text=text)
    signal_counter["free"] += 1

    await update.message.reply_text(
        f"✅ Señal enviada a FREE ({signal_counter['free']}/{MAX_FREE_PER_DAY})"
    )

async def send_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    reset_if_new_day()

    if signal_counter["vip"] >= MAX_VIP_PER_DAY:
        await update.message.reply_text("❌ Límite diario VIP alcanzado")
        return

    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("⚠️ Usa: /send_vip TEXTO")
        return

    await context.bot.send_message(chat_id=CANAL_VIP, text=text)
    signal_counter["vip"] += 1

    await update.message.reply_text(
        f"✅ Señal enviada a VIP ({signal_counter['vip']}/{MAX_VIP_PER_DAY})"
    )

# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send_free", send_free))
    app.add_handler(CommandHandler("send_vip", send_vip))
    app.add_handler(CallbackQueryHandler(rules, pattern="^rules$"))
    app.add_handler(CallbackQueryHandler(info, pattern="^info$"))
    app.add_handler(CallbackQueryHandler(tutorial_binance, pattern="^tutorial_binance$"))

    print("🤖 Bot corriendo correctamente...")
    app.run_polling()

if __name__ == "__main__":
    main()
