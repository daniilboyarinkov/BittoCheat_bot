def get_url():
    from requests import get
    tarhet_url = "https://inspirobot.me/api?generate=true"
    from fake_useragent import UserAgent
    useragent = UserAgent()
    headers = {
        "User-Agent": useragent.random,
        "Accept": "*/*",
    }
    response = get(url=tarhet_url, headers=headers)
    return response.text


def get_inspire_picture(url):
    import requests
    img = requests.get(url)
    name = url.split("/")[-1]
    with open(f'P_Sources/Pictures/{name}.jpg', 'wb') as img_file:
        img_file.write(img.content)
    return name


if __name__ == "__main__":
    print(get_inspire_picture(get_url()))
