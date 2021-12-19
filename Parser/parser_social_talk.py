def parser_social_talk(query):
    import urllib.parse as up
    from requests import get
    from fake_useragent import UserAgent
    q = up.quote(query.encode('cp1251'))
    useragent = UserAgent()
    target_url = f"http://www.gatchina.biz/conversation?q={q}&l=http%3A//www.google.com/"
    headers = {
    "User-Agent": useragent.random,
    "Accept": "*/*",
    "Referer": "http://www.gatchina.biz/generator",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ru - RU, ru",

    }

    response = get(target_url, headers=headers)
    return filter_data(query, str(response.text.replace("document.getElementById('text').innerHTML='", "").replace("&nbsp;", "").replace("';document.forms['rform'].elements['query'].value='';", "").replace("&laquo;", '"').replace("&raquo;", '"').encode(), 'utf-8'))


def filter_data(query, data):
    big_letters = 0
    for letter in data:
        if letter.upper() == letter:
            big_letters += 1
        else:
            big_letters -= 1
    if big_letters > 0:
        parser_social_talk(query)
    else:
        return data


if __name__ == "__main__":
    print(parser_social_talk("машина"))
