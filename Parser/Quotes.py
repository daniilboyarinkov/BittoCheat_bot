def parse_quotes_category(category):
    from requests import post
    from fake_useragent import UserAgent
    useragent = UserAgent()
    headers = {
        "User-Agent": useragent.random,
        "Accept": "*/*",
    }
    data = {
        "category": category,
    }
    target_url = "https://quotes-generator.com/library/ajax-generator.php"
    response = post(url=target_url, headers=headers, data=data)

    with open(f"Sources/{category}.html", "w", encoding='utf-8') as file:
        file.write(response.text)


def html_to_json(category):
    import json
    from bs4 import BeautifulSoup
    with open(f"./Sources/{category}.html", "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        all_qoutes = soup.find_all('div', class_='quote-box-inner')
        QOUTES = {"quotes": []}
        for qoute in all_qoutes:
            author = qoute.find('span', class_="author").get_text().replace("-", "").strip()
            text = qoute.find_all('span', limit=1)[0].get_text().replace("Â", "").replace("€", "").replace(r"\x", "").replace("™", "").replace(r" \ ".strip(), "")
            QOUTES["quotes"].append({"text": text, "author": author})
        with open(f"./Sources/JSONS/{category}.json", 'w', encoding="utf-8") as json_file:
            json.dump(QOUTES, json_file, indent=4, ensure_ascii=False)


def get_quote(category):
    from random import randint
    import json
    with open(f"Parser/Sources/JSONS/{category}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        max_number = len(data["quotes"])
        random_quote = data["quotes"][randint(0, max_number+1)]
        return f"{random_quote['text']} \n\n ©{random_quote['author']}"


if __name__ == "__main__":
    categories = ["inspiration", "motivation", "love", "life", "friendship", "sad", "philosophy", "happiness", "humor", "relationship", "truth", "funny", "death", "god", "romance", "hope", "writing", "religion", "success", "knowledge", "education", "music"]
    # for category in categories:
    #     try:
    #         parse_quotes_category(category)
    #         print(f"{category}: done")
    #     except:
    #         print(f"{category}: not done")

    for category in categories:
        try:
            html_to_json(category)
            print(f"{category} is DONE")
        except Exception as e:
            print(f"{category} is ERROR")
            print(e)
    pass
