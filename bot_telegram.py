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
CANAL_VIP = "-1003504953186"

ADMIN_IDS = [5297138695]

MAX_FREE_PER_DAY = 2
MAX_VIP_PER_DAY = 10

VIP_PRICE_TEXT = (
    "💎 *ACCESO VIP – SEÑALES AUTOMÁTICAS*\n\n"
    "📊 Hasta 10 señales diarias\n"
    "🤖 Estrategia automática (BTC / ETH)\n"
    "📈 RR dinámico + TP escalonados\n"
    "🛑 Filtro de volatilidad y noticias\n\n"
    "💰 *Precio:* $10 USD / mes\n\n"
    "📩 Para acceder:\n"
    "1️⃣ Realiza el pago\n"
    "2️⃣ Pulsa *Solicitar Acceso*\n"
    "3️⃣ Un admin te habilita\n\n"
    "⚠️ Educativo – no asesoría financiera"
)

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

# ================= TECLADO =================

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📈 Canal FREE", url="https://t.me/CryptoSignalsPro_Free")],
        [InlineKeyboardButton("💎 Acceso VIP", callback_data="vip_info")],
        [InlineKeyboardButton("🟡 Registrarme en Binance", callback_data="tutorial_binance")],
        [InlineKeyboardButton("ℹ️ Cómo funciona", callback_data="info")],
        [InlineKeyboardButton("📜 Reglas", callback_data="rules")]
    ])

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 *Sistema de Trading Automático*\n\n"
        "📊 Señales educativas basadas en reglas\n"
        "📈 FREE y 💎 VIP disponibles\n\n"
        "👇 Elige una opción:"
    )
    await update.message.reply_text(text, reply_markup=main_keyboard(), parse_mode="Markdown")

# ================= VIP INFO =================

async def vip_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📩 Solicitar Acceso VIP", callback_data="vip_request")],
        [InlineKeyboardButton("🔙 Volver", callback_data="start")]
    ])

    await query.edit_message_text(
        VIP_PRICE_TEXT,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# ================= VIP REQUEST =================

async def vip_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    for admin_id in ADMIN_IDS:
        await context.bot.send_message(
            chat_id=admin_id,
            text=(
                f"📩 *SOLICITUD VIP*\n\n"
                f"👤 Usuario: @{user.username or 'sin_username'}\n"
                f"🆔 ID: {user.id}\n\n"
                f"➡️ Revisar pago y agregar al canal VIP"
            ),
            parse_mode="Markdown"
        )

    await query.edit_message_text(
        "✅ *Solicitud enviada*\n\n"
        "Un administrador revisará tu acceso.\n"
        "Gracias por tu interés 💎",
        parse_mode="Markdown"
    )

# ================= INFO =================

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "ℹ️ *Funcionamiento*\n\n"
        "🤖 El sistema analiza BTC y ETH\n"
        "📊 Señales automáticas con filtros\n"
        "⚠️ Siempre usa gestión de riesgo",
        parse_mode="Markdown"
    )

# ================= REGLAS =================

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📜 *Reglas*\n\n"
        "1️⃣ Uso educativo\n"
        "2️⃣ Stop Loss obligatorio\n"
        "3️⃣ No sobreoperar\n"
        "4️⃣ Riesgo máx 1–2%",
        parse_mode="Markdown"
    )

# ================= BINANCE =================

async def tutorial_binance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        f"🟡 Regístrate en Binance:\n{BINANCE_REF}",
        parse_mode="Markdown"
    )

# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start, pattern="^start$"))
    app.add_handler(CallbackQueryHandler(vip_info, pattern="^vip_info$"))
    app.add_handler(CallbackQueryHandler(vip_request, pattern="^vip_request$"))
    app.add_handler(CallbackQueryHandler(info, pattern="^info$"))
    app.add_handler(CallbackQueryHandler(rules, pattern="^rules$"))
    app.add_handler(CallbackQueryHandler(tutorial_binance, pattern="^tutorial_binance$"))

    print("🤖 Bot Telegram activo")
    app.run_polling()

if __name__ == "__main__":
    main()
