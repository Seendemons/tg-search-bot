
import httpx
from bs4 import BeautifulSoup


async def search_wiki(query: str | None) -> list:

    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query
    }
    HEADERS = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, params=PARAMS, headers=HEADERS, timeout=10)
        except httpx.RequestError:
            return ["Wikipedia: Не удалось выполнить поиск, попробуйте позже"]

        data = response.json()

        # Пустой ответ wiki
        if not data["query"]["search"]:
            return ["Wikipedia: По вашему запросу ничего не найдено"]

        article = data["query"]["search"][0] # самая первая статья
        title = article["title"] # название статьи
        snippet  = BeautifulSoup(article["snippet"], "html.parser").get_text() # краткое описание
        url = f"https://en.wikipedia.org/?curid={article["pageid"]}" # ссылка на статью
        source = "Wikipedia" # источник

        result = [title, snippet, url, source]

        return result
