import json

from telethon import TelegramClient
import configparser
import re

from telethon.tl import functions

config = configparser.ConfigParser()
config.read("config.ini")

API_ID = int(config['My_Assistant']['api_id'])
API_HASH = config['My_Assistant']['api_hash']
USERNAME = config['My_Assistant']['username']

client = TelegramClient('anon', API_ID, API_HASH)


async def parse_links_from_messages():
    query = re.compile(r"((https://)*t.me/setlanguage/\w+)")
    result = set()
    async for message in client.iter_messages('translation_ru', search="t.me/setlanguage/"):
        finded_links = re.findall(query, message.text)
        for i in range(len(finded_links)):
            link = finded_links[i][0]
            if "https://" in link:
                result.add(link)
            else:
                result.add("https://" + link)
    print("translation_ru - done")
    async for message in client.iter_messages('setlanguagetelegrammm', search="t.me/setlanguage/"):
        finded_links = re.findall(query, message.text)
        for i in range(len(finded_links)):
            link = finded_links[i][0]
            if "https://" in link:
                result.add(link)
            else:
                result.add("https://" + link)
    print("setlanguagetelegrammm - done")
    async for message in client.iter_messages('setlanguagetelegram', search="t.me/setlanguage/"):
        finded_links = re.findall(query, message.text)
        for i in range(len(finded_links)):
            link = finded_links[i][0]
            if "https://" in link:
                result.add(link)
            else:
                result.add("https://" + link)
    print("setlanguagetelegram - done")
    async for message in client.iter_messages('languagetga', search="t.me/setlanguage/"):
        finded_links = re.findall(query, message.text)
        for i in range(len(finded_links)):
            link = finded_links[i][0]
            if "https://" in link:
                result.add(link)
            else:
                result.add("https://" + link)
    print("languagetga - done")

    # with open("#.json", "w") as file:
    #     links = []
    #     for link in result:
    #         links.append({"link": link})
    #     json.dump({"links": links}, file)


async def parse_theme_links_from_messages():
    groups = ["temidasuli", "bejaixicucytsywb", "temdlatg", "Temaapl", "temy_android", "tems_ios_android", "setlanguagetelegram", "setlanguagetelegrammm", "languagetga"]
    query = re.compile(r"((https://)*t.me/addtheme/\w+)")
    result = set()
    for group in groups:
        async for message in client.iter_messages(group, search="t.me/addtheme/"):
            finded_links = re.findall(query, message.text)
            for i in range(len(finded_links)):
                link = finded_links[i][0]
                if "https://" in link:
                    result.add(link)
                else:
                    result.add("https://" + link)
                print(link)
    with open("#", "w") as file:
        links = []
        for link in result:
            links.append({"link": link})
        json.dump({"links": links}, file)


def get_themes_name():
    import requests
    from bs4 import BeautifulSoup
    Links_Name = []
    with open("#", 'r') as f:
        data = json.load(f)
        for i in range(len(data['links'])):
            try:
                link = data['links'][i]['link']
                response = requests.get(url=link)
                html = response.content
                soup = BeautifulSoup(html, "html.parser")
                name = soup.select("div.tgme_page_description>strong")[0].get_text()
                Links_Name.append({"link": link, "name": name})
            except:
                continue
    with open("Links/themes_linksn.json", "w") as f:
        json.dump({"links": Links_Name}, f)



async def main():
    # async for message in client.iter_messages('pinkraspberry1'):
    #     print(message.text)
    # message = await client.send_message("pinkraspberry1", "Я тебя люблю❤🐾")
    # await client.pin_message('pinkraspberry1', message=message, notify=True)
    # async for photo in client.iter_profile_photos(entity='https://t.me/translation_ru'):
    #     print(photo)
    # await parse_links_from_messages()
    # get_names()
    # await parse_theme_links_from_messages()
    # get_themes_name()
    pass
    

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
