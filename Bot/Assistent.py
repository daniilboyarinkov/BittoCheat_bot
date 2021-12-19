import requests
# from aiogram import Bot, Dispatcher
# from aiogram.types import Message
# from aiogram.utils import executor

# bot = Bot(token=TOKEN, parse_mode='HTML')
# dp = Dispatcher(bot)


# @dp.message_handler()
# async def send_my_id(message: Message):
#     await message.answer(text=f"your chat id: {message.chat.id}")


def send_me_log(message):
    import json
    TOKEN = "2102738030:AAFT-rBdAs-evCdZW_syVTD8nrBXXkKRE_0"
    MY_CHAT_ID = "841428305"
    ML_CHAT_ID = "867766948"
    my_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={MY_CHAT_ID}&disable_notification=true&parse_mode=HTML&text={message}"
    ml_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ML_CHAT_ID}&disable_notification=true&parse_mode=HTML&text={message}"
    my_response = requests.get(my_url)
    ml_response = requests.get(ml_url)
    return


if __name__ == "__main__":
    send_me_log("test")
    # executor.start_polling(dp, skip_updates=True)
