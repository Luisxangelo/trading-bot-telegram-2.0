from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)
from datetime import date, datetime, timedelta
import json
from payments.mercadopago import create_payment_link

# ================= CONFIG =================

TOKEN = "TU_TOKEN_AQUI"

BINANCE_REF = "https://accounts.binance.com/register?ref=ROZTAFCJ"

CANAL_FREE = "-1003648632391"
CANAL_VIP = "-1003504953186"

ADMIN_IDS = [5297138695]

MAX_FREE_PER_DAY = 2
MAX_VIP_PER_DAY = 10

VIP_FILE = "vip_users.json"

# ================= UTIL VIP =================

def load_vips():
    try:
        with open(VIP_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_vips(data):
    with open(VIP_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_vip(user_id):
    vips = load_vips()
    vips[str(user_id)] = {
        "expires": (datetime.now() + timedelta(days=30)).isoformat()
    }
    save_vips(vips)

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
        "<b>🤖 Sistema de Trading Automático</b>\n\n"
        "📊 Señales educativas basadas en reglas\n"
        "📈 Canal FREE y 💎 VIP disponibles\n\n"
        "👇 Elige una opción:"
    )

    if update.message:
        await update.message.reply_text(
            text,
            reply_markup=main_keyboard(),
            parse_mode="HTML"
        )
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text,
            reply_markup=main_keyboard(),
            parse_mode="HTML"
        )

# ================= VIP INFO =================

async def vip_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    payment_link = create_payment_link(user.id, user.username or "usuario")

    text = (
        "<b>💎 ACCESO VIP – SEÑALES AUTOMÁTICAS</b>\n\n"
        "📊 Hasta <b>10 señales diarias</b>\n"
        "🤖 Estrategia automática BTC / ETH\n"
        "📈 RR dinámico + TP escalonados\n"
        "🛑 Filtro de volatilidad y noticias\n\n"
        "<b>💰 Precio:</b> 10 USD / 30 días\n\n"
        "👇 Paga aquí para activar tu acceso:"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 PAGAR ACCESO VIP", url=payment_link)],
        [InlineKeyboardButton("📩 Solicitar Acceso VIP", callback_data="vip_request")],
        [InlineKeyboardButton("🔙 Volver", callback_data="start")]
    ])

    await query.edit_message_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

# ================= VIP REQUEST =================

async def vip_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    username = f"@{user.username}" if user.username else "Sin username"

    for admin_id in ADMIN_IDS:
        await context.bot.send_message(
            chat_id=admin_id,
            text=(
                "<b>📩 SOLICITUD VIP</b>\n\n"
                f"👤 Usuario: {username}\n"
                f"🆔 ID: {user.id}\n\n"
                "➡️ Verificar pago y habilitar acceso"
            ),
            parse_mode="HTML"
        )

    await query.edit_message_text(
        "<b>✅ Solicitud enviada</b>\n\n"
        "Un administrador revisará tu acceso.\n"
        "Gracias por tu interés 💎",
        parse_mode="HTML"
    )

# ================= INFO =================

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "<b>ℹ️ Funcionamiento</b>\n\n"
        "🤖 Análisis automático BTC / ETH\n"
        "📊 Estrategias con filtros avanzados\n"
        "⚠️ Usa siempre gestión de riesgo",
        parse_mode="HTML"
    )

# ================= REGLAS =================

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "<b>📜 Reglas</b>\n\n"
        "1️⃣ Uso educativo\n"
        "2️⃣ Stop Loss obligatorio\n"
        "3️⃣ No sobreoperar\n"
        "4️⃣ Riesgo máximo 1–2%",
        parse_mode="HTML"
    )

# ================= BINANCE =================

async def tutorial_binance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        f"<b>🟡 Regístrate en Binance</b>\n\n{BINANCE_REF}",
        parse_mode="HTML"
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

    print("🤖 Bot Telegram activo y estable")
    app.run_polling()

if __name__ == "__main__":
    main()
