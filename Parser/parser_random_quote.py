def parse_random_quote():
    from requests import get
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent

    userAgent = UserAgent()
    target_url = "http://wisdomofchopra.com/iframe.php"
    headers = {
        "User-Agent": userAgent.random,
    }
    html = get(url=target_url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')

    quote_en = soup.find("h2").text

    return f'{quote_en}'


if __name__ == "__main__":
    print(parse_random_quote())
