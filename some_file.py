from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
GOOGLE_BOOKS_API_KEY = 'YOUR_GOOGLE_BOOKS_API_KEY'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Введите название книги для поиска.')

def search_books(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text('Пожалуйста, введите название книги.')
        return
    
    url = f'https://www.googleapis.com/books/v1/volumes?q={requests.utils.quote(query)}&key={GOOGLE_BOOKS_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            books = data['items']
            message = ''
            for book in books[:5]:  # Показать до 5 книг
                volume_info = book['volumeInfo']
                title = volume_info.get('title', 'Нет названия')
                authors = ', '.join(volume_info.get('authors', ['Нет авторов']))
                message += f'Title: {title}\nAuthors: {authors}\n\n'
            update.message.reply_text(message if message else 'Книги не найдены.')
        else:
            update.message.reply_text('Книги не найдены.')
    else:
        update.message.reply_text('Ошибка при запросе к API.')

def main() -> None:
    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, search_books))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    # в гугл шитс надо загрузить
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # Настройте доступ к Google Sheets
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
# client = gspread.authorize(creds)
# sheet = client.open('YourSpreadsheetName').sheet1

# def add_to_sheet(title, authors):
#     sheet.append_row([title, authors])
