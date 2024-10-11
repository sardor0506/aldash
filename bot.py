from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes

# States
NAME, SURNAME, PHONE, UNIVERSITY = range(4)

# O'zbekistonning eng yaxshi universitetlari (to'liq nomlar)
UNIVERSITIES = [
    "O'zbekiston Milliy Universiteti",
    "Samarqand Davlat Universiteti",
    "Toshkent Iqtisodiyot Universiteti",
    "Toshkent Texnika Universiteti",
    "Andijon Davlat Universiteti",
    "Namangan Davlat Universiteti",
    "Buxoro Davlat Universiteti",
    "Farg'ona Universiteti",
    "Qarshi Universiteti",
    "Sirdaryo Universiteti",
]

# Qabul qiluvchi foydalanuvchining ID sini o'rnating
TARGET_USER_ID = 5867100858  # O'zgartiring

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Ismingizni kiriting:")
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Familiyangizni kiriting:")
    
    # Har bir kiritilgan ma'lumotni yuborish
    await context.bot.send_message(chat_id=TARGET_USER_ID, text=f"Ismi: {context.user_data['name']}")
    
    return SURNAME

async def surname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['surname'] = update.message.text
    await update.message.reply_text("Telefon raqamingizni yuborish uchun tugmani bosing:", reply_markup=get_phone_keyboard())
    
    # Har bir kiritilgan ma'lumotni yuborish
    await context.bot.send_message(chat_id=TARGET_USER_ID, text=f"Familiyasi: {context.user_data['surname']}")
    
    return PHONE

def get_phone_keyboard():
    button = KeyboardButton("Telefon raqamini yuborish", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    return keyboard

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.contact:
        context.user_data['phone'] = update.message.contact.phone_number
        
        # Telefon raqamini yuborish
        await context.bot.send_message(chat_id=TARGET_USER_ID, text=f"Telefon raqami: {context.user_data['phone']}")

        # Inline keyboard yaratish (to'liq nomlar)
        keyboard = [
            [InlineKeyboardButton("O'zbekiston Milliy Universiteti", callback_data="O'zbekiston Milliy Universiteti")],
            [InlineKeyboardButton("Samarqand Davlat Universiteti", callback_data="Samarqand Davlat Universiteti")],
            [InlineKeyboardButton("Toshkent Iqtisodiyot Universiteti", callback_data="Toshkent Iqtisodiyot Universiteti")],
            [InlineKeyboardButton("Toshkent Texnika Universiteti", callback_data="Toshkent Texnika Universiteti")],
            [InlineKeyboardButton("Andijon Davlat Universiteti", callback_data="Andijon Davlat Universiteti")],
            [InlineKeyboardButton("Namangan Davlat Universiteti", callback_data="Namangan Davlat Universiteti")],
            [InlineKeyboardButton("Buxoro Davlat Universiteti", callback_data="Buxoro Davlat Universiteti")],
            [InlineKeyboardButton("Farg'ona Universiteti", callback_data="Farg'ona Universiteti")],
            [InlineKeyboardButton("Qarshi Universiteti", callback_data="Qarshi Universiteti")],
            [InlineKeyboardButton("Sirdaryo Universiteti", callback_data="Sirdaryo Universiteti")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Telefon raqamingiz qabul qilindi. Iltimos, O'zbekistondagi universitetlardan birini tanlang:", reply_markup=reply_markup)
        
        return UNIVERSITY
    else:
        await update.message.reply_text("Iltimos, raqamni yuborish tugmasini bosing!")
        return PHONE

async def university(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()  # Callbackni tasdiqlash

    selected_university = query.data

    if selected_university in UNIVERSITIES:
        context.user_data['university'] = selected_university

        # Tasdiqlash xabari
        reply_text = (f"Ma'lumotlaringiz qabul qilindi:\n"
                      f"Ism: {context.user_data['name']}\n"
                      f"Familiya: {context.user_data['surname']}\n"
                      f"Telefon: {context.user_data['phone']}\n"
                      f"Tanlangan universitet: {context.user_data['university']}")

        await query.message.reply_text(reply_text)

        # Har bir kiritilgan ma'lumotni yuborish
        await context.bot.send_message(chat_id=TARGET_USER_ID, text=reply_text)

        # Conversation ni tugatish
        return ConversationHandler.END
    else:
        await query.message.reply_text("Noto'g'ri universitet tanlandi, iltimos, qaytadan urinib ko'ring.")
        return UNIVERSITY

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Amal bekor qilindi.")
    return ConversationHandler.END

def main() -> None:
    application = ApplicationBuilder().token("7988846115:AAG1tZxCWm5uXNKFJizHm7u52Ojf0GkFs9Q").build()

    # Suhbatni boshqarish
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, surname)],
            PHONE: [MessageHandler(filters.CONTACT & ~filters.COMMAND, phone)],
            UNIVERSITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, university)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()