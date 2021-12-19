def get_random_theme():
    import json
    from random import randint
    with open("../Bot/Links/themes_linksn.json", "r") as f:
        data = json.load(f)
        max_number = len(data["links"])+1
        r = randint(0, max_number)
        result = f"Название: {data['links'][r]['name']}\n\n{data['links'][r]['link']} "
    return result


if __name__ == '__main__':
    print(get_random_theme())
