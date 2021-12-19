from aiogram.utils import executor
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher, types
from time import sleep
from Parser.parser_stickersets import parse_ajax
from Assistent import send_me_log
from Parser.parser_random_word import parser_random_word
from Parser.parser_social_talk import parser_social_talk
from Parser.parser_random_quote import parse_random_quote
from Parser.Quotes import get_quote
from Parser.picture_from_inspire_bot import get_url
from Parser.parser_quotes_from_songs import parse_quote_from_songs
from Parser.Languages import get_random_language
from Parser.Themes import get_random_theme
from aiogram.dispatcher.filters.state import StatesGroup, State
from pymorphy2 import MorphAnalyzer
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
morph = MorphAnalyzer()
page = 0
keywords = ""


class FindStickerpacks(StatesGroup):
    keywords = State()


class FindSocialTalk(StatesGroup):
    keywords = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    find_stickers_item = types.KeyboardButton("Найти стикеры по ключевым словам")
    inspiro_picture_item = types.KeyboardButton("Получить картинку от ©InspiroBot")
    random_language_item = types.KeyboardButton("Получить рандомный язык")
    random_theme_item = types.KeyboardButton("Получить рандомную тему")
    song_quote_item = types.KeyboardButton("Цитата из песни")
    random_word_item = types.KeyboardButton("Генерировать рандомное слово")
    social_talk_item = types.KeyboardButton("Генерировать светскую беседу")
    random_quote_item = types.KeyboardButton("Генерировать рандомную цитату en")
    get_quote_item = types.KeyboardButton("Получить цитату en")
    help_item = types.KeyboardButton("Нужна помощь?")
    markup.row(find_stickers_item)
    markup.row(inspiro_picture_item)
    markup.row(random_language_item)
    markup.row(random_theme_item)
    markup.row(song_quote_item)
    markup.row(get_quote_item)
    markup.row(random_word_item)
    markup.row(random_quote_item)
    markup.row(social_talk_item)
    markup.row(help_item)
    await bot.send_sticker(message.chat.id, sticker="CAACAgIAAxkBAAEDSFVhkPaBJwMnFNolBJQu83C1Xq8bGAACVAADQbVWDGq3-McIjQH6IgQ")
    await message.answer(text=f"\tДобро пожаловать, {message.from_user.full_name}. \n\nЯ - <b>BittoCheat</b> - бот, личный проект BDW. \nЧем я могу вам помочь?\n\nДля того чтобы увидеть подсказку можете написать /help",
                         reply_markup=markup)


@dp.message_handler(commands=['help'])
@dp.message_handler(lambda message: message.text.lower() == "нужна помощь?")
async def send_help(message: Message):
    await message.answer(text=f"Команды: \n"
                              f"/find_stickers - поиск стикеров по ключевым словам \n"
                              f"/get_quote - получить цитату en \n"
                              f"/get_language - получить рандомный язык \n"
                              f"/get_theme - получить рандомную тему \n"
                              f"/get_inspiro_picture - получить картинку от inspirobot \n"
                              f"/random_word - генерировать рандомное слово \n"
                              f"/random_quote - генерировать рандомную цитату \n"
                              f"/social_talk - генерировать светскую беседу \n"
                              f"/help - подсказка \n"
                              f"/start - запуск бота \n")


@dp.message_handler(Command('find_stickers'))
@dp.message_handler(lambda message: message.text.lower() == "найти стикеры по ключевым словам")
async def find_stickers(message: Message):
    global page
    page = 0
    await message.answer(text="Введите ключевые слова: ")
    await FindStickerpacks.keywords.set()


@dp.message_handler(state=FindStickerpacks.keywords)
async def show_stickers(message: Message, state: FSMContext):
    global page
    global keywords
    async with state.proxy() as query:
        query['name'] = message.text
        parsed_data = parse_ajax(query=query['name'], HPP=3, page=page)
        await message.answer(text='Выполняю поиск стикеров...')

        send_me_log(f"Действие: Поиск стикеров \n"
                    f"{message.from_user.full_name} \n"
                    f"id: {message.from_user.id} \n"
                    f"запрос: <b>{query['name']}</b> \n")
        sleep(2.1)
        await send_stickers(user=message.chat.id, data=parsed_data, text=message.text)
        keywords = query['name']
    await state.finish()


async def send_stickers(user, data, text):
    global page
    stick = morph.parse('стикер')[0]
    if not data:
        await bot.send_message(user, f'Извините, по вашему запросу "{text}" ничего не найдено... ')
        return
    if len(data['hits']) >= 3:
        await bot.send_message(user, f'По вашему запросу "{text}" было найдено: ')
        for i in range(3):
            sleep(.21)
            await bot.send_message(user,
                             f"<b>{data['hits'][i]['name']}</b> \n"
                             f"<b>{data['hits'][i]['name_en']}</b> \n"
                             f"<b>{data['hits'][i]['count']}</b> {stick.make_agree_with_number(data['hits'][i]['count']).word}\n")
            # ссылка: f"<b>https://tlgrm.ru/stickers/{data['hits'][i]['link']}</b>\n"
            await send_sticker(user, data['hits'][i]['link'])
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("Загрузить ещё", callback_data="more_stickers_yes"))
        markup.row(types.InlineKeyboardButton("Спасибо, я нашел всё что искал", callback_data="more_stickers_no"))
        await bot.send_message(user, "Загрузить ещё?", reply_markup=markup)
        page += 1

    elif len(data['hits']) > 0:
        await bot.send_message(user, f'По вашему запросу "{text}" было найдено: ')
        for i in range(len(data['hits'])):
            sleep(.21)
            await bot.send_message(user,
                             f"<b>{data['hits'][i]['name']}</b> \n"
                             f"<b>{data['hits'][i]['name_en']}</b> \n"
                             f"Кол-во стикеров: <b>{data['hits'][i]['count']}</b> \n"
                             f"Ссылка: <b>https://tlgrm.ru/stickers/{data['hits'][i]['link']}</b> \n"
                             f"Автор: <b>{data['hits'][i]['author']} </b> \n"
                             )
        page += 1
    else:
        await bot.send_message(user, "Извините ничего найдено не было")


@dp.callback_query_handler(lambda call: True)
async def callback_query(call: CallbackQuery):
    categories = ["inspiration", "motivation", "love", "life", "friendship", "sad", "philosophy", "happiness", "humor",
                  "relationship", "truth", "funny", "death", "god", "romance", "hope", "writing", "religion", "success",
                  "knowledge", "education", "music"]
    if call.data in categories:
        try:
            await bot.send_message(call.message.chat.id, get_quote(call.data))
        except Exception as e:
            await bot.send_message(call.message.chat.id, "ooops")
            print(e)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        try:
            global page
            global keywords
            if call.message:
                await call.answer(cache_time=21)
                if call.data == "more_stickers_yes":
                    data = parse_ajax(query=keywords, HPP=3, page=page)
                    await send_stickers(data=data, user=call.message.chat.id, text=keywords)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*" * 57)
                    await call.message.answer(text="")
                elif call.data == "more_stickers_no":
                    await bot.send_message(call.message.chat.id, "Всегда рады помочь!")
                    page = 0
                    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass


async def send_sticker(user, name):
    from json import loads
    sticker = loads(str(await bot.get_sticker_set(name=name)))['stickers'][0]['file_id']
    await bot.send_sticker(user, sticker=sticker)


@dp.message_handler(Command('random_word'))
@dp.message_handler(lambda message: message.text.lower() == "генерировать рандомное слово")
async def random_word(message: Message):
    await message.answer(parser_random_word())


@dp.message_handler(Command('get_language'))
@dp.message_handler(lambda message: message.text.lower() == "получить рандомный язык")
async def get_random__language(message: Message):
    await message.answer(text="<b>Предупреждение!</b>\n\nНе все языки могут быть установлены на модель вашего устройства")
    await message.answer(text=get_random_language())


@dp.message_handler(Command('get_theme'))
@dp.message_handler(lambda message: message.text.lower() == "получить рандомную тему")
async def get_random__theme(message: Message):
    await message.answer(text="<b>Предупреждение!</b>\n\nНе все темы могут поддерживаться вашим устройством")
    await message.answer(text=get_random_theme())


@dp.message_handler(Command('social_talk'))
@dp.message_handler(lambda message: message.text.lower() == "генерировать светскую беседу")
async def social_talk(message: Message):
    await message.answer(text="Введите ключевое слово: ")
    await FindSocialTalk.keywords.set()


@dp.message_handler(state=FindSocialTalk.keywords)
async def show_stickers(message: Message, state: FSMContext):
    async with state.proxy() as query:
        query['name'] = message.text
        send_me_log(f"Действие: Генерация светской беседы \n"
                    f"{message.from_user.full_name} \n"
                    f"id: {message.from_user.id} \n"
                    f"запрос: <b>{query['name']}</b> \n")
        try:
            await message.answer(text=parser_social_talk(query['name']))
        except:
            await message.answer(text="ooops")
    await state.finish()


@dp.message_handler(Command('random_quote'))
@dp.message_handler(lambda message: message.text.lower() == "генерировать рандомную цитату en")
async def random_quote(message: Message):
    await message.answer(parse_random_quote())


@dp.message_handler(Command('get_inspiro_picture'))
@dp.message_handler(lambda message: message.text.lower() == "получить картинку от ©inspirobot")
async def get_inspiro_picture(message: Message):
    await bot.send_photo(message.chat.id, get_url())


@dp.message_handler(Command('song_quote_item'))
@dp.message_handler(lambda message: message.text.lower() == "цитата из песни")
async def quote_from_song(message: Message):
    await message.answer(text=parse_quote_from_songs())


@dp.message_handler(Command('get_quote'))
@dp.message_handler(lambda message: message.text.lower() == "получить цитату en")
async def get_quotee(message: Message):
    categories = ["inspiration", "motivation", "love", "life", "friendship", "sad", "philosophy", "happiness", "humor",
                  "relationship", "truth", "funny", "death", "god", "romance", "hope", "writing", "religion", "success",
                  "knowledge", "education", "music"]
    markup = types.InlineKeyboardMarkup()
    for category in categories:
        markup.row(types.InlineKeyboardButton(category.capitalize(), callback_data=category))
    await message.answer("Выберите категорию: ", reply_markup=markup)


@dp.message_handler()
async def send_default(message: Message):
    await send_help(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
