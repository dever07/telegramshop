from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN: Final = '7034268632:AAGB79RIijwtfcmoCAs6oK69ylRmCFQuXYE'
BOT_USERNAME: Final = '@Faudra_que_tu_me_dise_comment_lappeller'

# Products
products = {
    "produit1": {"name": "Produit1", "description": "Description du produit 1", "price": 10},
    "produit2": {"name": "Produit2", "description": "Description du produit 2", "price": 15},
    "produit3": {"name": "Produit3", "description": "Description du produit 3", "price": 20},
}


# Start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour, \n\nBienvenue à notre shop!\n \nUtilisez: \n/products pour voir nos produits. \n/buy <nom_du_produit> pour acheter\n/help pour avoir de l'aide")


# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Envoyez: \n/products pour voir les produits disponibles \n/buy <nom_du_produit> pour acheter.")


# Product listing
async def products_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Voici nos produits disponibles:\n"
    for key, product in products.items():
        message += f"{product['name']} - {product['price']}€: {product['description']}\n"
    await update.message.reply_text(message)


# Buy command
async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Veuillez spécifier le produit après /buy. Exemple: /buy produit1")
        return

    product_key = args[0].lower()
    if product_key in products:
        product = products[product_key]
        keyboard = [
            [InlineKeyboardButton("Confirmer l'achat", callback_data=f"buy_{product_key}")],
            [InlineKeyboardButton("Annuler", callback_data="cancel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Vous avez choisi d'acheter {product['name']} pour {product['price']}€. Confirmez-vous l'achat?",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "Produit non trouvé. Utilisez /products pour voir la liste des produits disponibles.")


# Handle button press in InlineKeyboard
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "cancel":
        await query.edit_message_text(text="Achat annulé.")
    elif data.startswith("buy_"):
        product_key = data.split("_")[1]
        product = products[product_key]
        await query.edit_message_text(text=f"Merci pour votre achat de {product['name']}!")


# Main block to run the bot
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('products', products_command))
    app.add_handler(CommandHandler('buy', buy_command))  # Modification ici
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
