def parse_ajax(query, HPP, page):
    from fake_useragent import UserAgent
    from requests import post
    useragent = UserAgent()
    request_url = "https://xgemcn70bo-dsn.algolia.net/1/indexes/stickers/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.11.0)%3B%20Browser%20(lite)&x-algolia-api-key=19b4a7255a132835763a95eae757a5eb&x-algolia-application-id=XGEMCN70BO"
    data = {
        "query": query,
        "hitsPerPage": HPP,
        "filters": "lang:NA OR lang:RU",
        "removeWordsIfNoResults": "allOptional",
        "clickAnalytics": True,
        "page": page,
        "attributesToHighlight": [],
    }
    headers = {
        "Accept": "*/*",
        "User-Agent": useragent.random
    }
    try:
        result = post(url=request_url, headers=headers, json=data)
        return filter_data(result.json())
    except:
        return {}


def filter_data(data):
    dataTosort = data
    try:
        del dataTosort['page']
        del dataTosort['nbPages']
        del dataTosort['hitsPerPage']
        del dataTosort['exhaustiveNbHits']
        del dataTosort['exhaustiveTypo']
        del dataTosort['params']
        del dataTosort['queryID']
        del dataTosort['processingTimeMS']
    except:
        pass
    for v in dataTosort['hits']:
        try:
            del v["external"]
            del v["objectID"]
        except: continue
        continue
    return dataTosort


if __name__ == '__main__':
    print(parse_ajax("малина", 3, 0))
