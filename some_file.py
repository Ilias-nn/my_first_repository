from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests  # Не забудьте этот импорт

BOT_TOKEN = '8002034631:AAE9dQSDDqh4Qvz1g03COGf3SA8ppgn8JrM'
GOOGLE_BOOKS_API_KEY = 'AIzaSyDssXLPBffyny4qrmUBJ9x6zlnPLo6-L_c'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Введите название книги для поиска.')

async def search_books(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text('Пожалуйста, введите название книги.')
        return
    
    url = f'https://www.googleapis.com/books/v1/volumes?q={requests.utils.quote(query)}&key={GOOGLE_BOOKS_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            books = data['items']
            message = ''
            for book in books[:5]:
                volume_info = book['volumeInfo']
                title = volume_info.get('title', 'Нет названия')
                authors = ', '.join(volume_info.get('authors', ['Нет авторов']))
                image_links = volume_info.get('imageLinks', {})
                thumbnail = image_links.get('thumbnail', None)
                message = f'Title: {title}\nAuthors: {authors}\n'
                if thumbnail:
                    await update.message.reply_photo(photo=thumbnail, caption=message)
                else:
                    await update.message.reply_text('Image: Нет изображения\n')
            await update.message.reply_text(message if message else 'Книги не найдены.')
        else:
            await update.message.reply_text('Книги не найдены.')
    else:
        await update.message.reply_text('Ошибка при запросе к API.')

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search_books))
    application.run_polling()

if __name__ == '__main__':
    main()
