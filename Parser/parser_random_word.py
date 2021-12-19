def parser_random_word():
    from requests import get
    from fake_useragent import UserAgent
    useragent = UserAgent()
    result = ""
    for i in range(1, 3):
        request_url = f"http://ig-mag.ru/random/getText.php?act=getByType&type=w{i}&lastWord="
        headers = {
                'Accept': "*/*",
                "User-Agent": useragent.random,
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}
        response = get(url=request_url, headers=headers)
        result += response.text
    return result.capitalize()


if __name__ == "__main__":
    print(parser_random_word())
