def parse_quote_from_songs():
    from bs4 import BeautifulSoup
    from requests import get
    from fake_useragent import UserAgent
    useragent = UserAgent()
    target_url = "https://citaty.info/ajax/random_quote/0/quote_song/0/0"
    headers = {
        "User-Agent": useragent.random,
        "Accept": "*/*",
    }
    response = get(url=target_url, headers=headers)
    html = response.content.decode('unicode-escape').replace(r" \ ".strip(), "")
    soup = BeautifulSoup(html, "html.parser")
    # with open("index.html", "w", encoding="utf-8") as f:
    #     f.write(html)
    text = soup.select_one("div.field-item>p").get_text() or ""
    author = soup.find("a", title="Исполнитель").get_text() or ""
    song = soup.find("a", title="Песня").get_text() or ""

    return f"{text}\n\n©{author}\nПесня: {song}"


if __name__ == "__main__":
    print(parse_quote_from_songs())
