from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from datetime import datetime, timedelta
import json
import os

from payments.mercadopago import create_payment_link

# ================= CONFIG =================

TOKEN = "8529903726:AAEU7BLVq_3wMSCbU_Fve4kPfoXSVRADS-8"

CANAL_FREE = "-1003648632391"
CANAL_VIP = "-1003504953186"

ADMIN_IDS = [5297138695]

BINANCE_REF = "https://accounts.binance.com/register?ref=ROZTAFCJ"
BINANCE_PAY_LINK = "https://app.binance.com/uni-qr/B5oanxR3"

VIP_FILE = "vip_users.json"

# ================= VIP STORAGE =================

def load_vips():
    if not os.path.exists(VIP_FILE):
        return {}
    with open(VIP_FILE, "r") as f:
        return json.load(f)

def save_vips(vips):
    with open(VIP_FILE, "w") as f:
        json.dump(vips, f, indent=2)

def is_vip(user_id):
    vips = load_vips()
    user = vips.get(str(user_id))
    if not user:
        return False
    return datetime.fromisoformat(user["expires"]) > datetime.now()

def add_vip(user_id):
    vips = load_vips()
    vips[str(user_id)] = {
        "expires": (datetime.now() + timedelta(days=30)).isoformat()
    }
    save_vips(vips)

def remove_vip(user_id):
    vips = load_vips()
    vips.pop(str(user_id), None)
    save_vips(vips)

# ================= TECLADOS =================

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📈 Canal FREE", url="https://t.me/CryptoSignalsPro_Free")],
        [InlineKeyboardButton("💎 Acceso VIP", callback_data="vip_info")],
        [InlineKeyboardButton("🟡 Binance", url=BINANCE_REF)],
        [InlineKeyboardButton("ℹ️ Cómo funciona", callback_data="info")]
    ])

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 <b>¡Bienvenido!</b>\n\n"
        "Soy un <b>sistema de trading automático</b> que analiza el mercado "
        "de <b>Bitcoin (BTC)</b> y <b>Ethereum (ETH)</b> en tiempo real.\n\n"

        "📊 <b>¿Qué encontrarás aquí?</b>\n"
        "• Señales basadas en reglas claras\n"
        "• Gestión de riesgo y TP escalonados\n"
        "• Enfoque educativo y disciplinado\n\n"

        "📈 <b>CANAL FREE</b>\n"
        "• Resultados\n"
        "• Ejemplos de señales\n"
        "• Contenido educativo\n\n"

        "💎 <b>CANAL VIP</b>\n"
        "• Señales automáticas en tiempo real\n"
        "• Hasta 10 señales diarias\n"
        "• Estrategia avanzada BTC / ETH\n\n"

        "👇 <b>Usa los botones para continuar</b>"
    )

    if update.message:
        await update.message.reply_text(
            text,
            reply_markup=main_keyboard(),
            parse_mode="HTML"
        )
    else:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text,
            reply_markup=main_keyboard(),
            parse_mode="HTML"
        )

# ================= INFO =================

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "ℹ️ <b>Cómo funciona</b>\n\n"
        "🤖 Sistema automático BTC / ETH\n"
        "📊 TP escalonados + RR dinámico\n"
        "🛑 Filtros de volatilidad y noticias\n\n"
        "⚠️ Uso educativo",
        parse_mode="HTML"
    )

# ================= VIP INFO =================

async def vip_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.callback_query.from_user
    await update.callback_query.answer()

    mp_link = create_payment_link(user.id, user.username or "usuario")

    text = (
        "💎 <b>ACCESO VIP – $10 USD / 30 días</b>\n\n"
        "✔ Hasta 10 señales diarias\n"
        "✔ BTC / ETH\n"
        "✔ TP escalonados\n\n"
        "💳 <b>Paga con:</b>"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 MercadoPago", url=mp_link)],
        [InlineKeyboardButton("🟡 Binance Pay", url=BINANCE_PAY_LINK)],
        [InlineKeyboardButton("📩 Solicitar Acceso", callback_data="vip_request")],
        [InlineKeyboardButton("🔙 Volver", callback_data="start")]
    ])

    await update.callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")

# ================= VIP REQUEST =================

async def vip_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.callback_query.from_user
    await update.callback_query.answer()

    username = f"@{user.username}" if user.username else "Sin username"

    for admin in ADMIN_IDS:
        await context.bot.send_message(
            chat_id=admin,
            text=(
                "📩 <b>SOLICITUD VIP</b>\n\n"
                f"👤 {username}\n"
                f"🆔 {user.id}\n\n"
                "➡️ Verificar pago"
            ),
            parse_mode="HTML"
        )

    await update.callback_query.edit_message_text(
        "✅ Solicitud enviada.\nUn admin revisará tu pago.",
        parse_mode="HTML"
    )

# ================= ADMIN PANEL =================

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    vips = load_vips()
    text = "📊 <b>PANEL VIP</b>\n\n"

    for uid, data in vips.items():
        text += f"🆔 {uid} → expira {data['expires']}\n"

    await update.message.reply_text(text, parse_mode="HTML")

async def admin_add_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    user_id = context.args[0]
    add_vip(user_id)
    await update.message.reply_text(f"✅ VIP activado para {user_id}")

async def admin_remove_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    user_id = context.args[0]
    remove_vip(user_id)
    await update.message.reply_text(f"❌ VIP removido para {user_id}")

# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("addvip", admin_add_vip))
    app.add_handler(CommandHandler("removevip", admin_remove_vip))

    app.add_handler(CallbackQueryHandler(start, pattern="^start$"))
    app.add_handler(CallbackQueryHandler(info, pattern="^info$"))
    app.add_handler(CallbackQueryHandler(vip_info, pattern="^vip_info$"))
    app.add_handler(CallbackQueryHandler(vip_request, pattern="^vip_request$"))

    print("🤖 BOT TELEGRAM ACTIVO Y ESTABLE")
    app.run_polling()

if __name__ == "__main__":
    main()
