
import httpx
from bs4 import BeautifulSoup

from first_bot.classes import SearchResult


async def search_wiki(query: str | None) -> tuple[list[SearchResult], str | None]:

    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srlimit": 3,
        "srsearch": query
    }
    HEADERS = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, params=PARAMS, headers=HEADERS, timeout=None)
            response.raise_for_status()
        except httpx.RequestError:
            return [], "Wikipedia: Не удалось выполнить поиск, попробуйте позже"
        except httpx.HTTPStatusError as error:
            return [], f"Ошибка сервиса: {error.response.status_code}"

        data = response.json()

        # Пустой ответ wiki
        if not data["query"]["search"]:
            return [], "Wikipedia: По вашему запросу ничего не найдено"

        articles = data["query"]["search"]
        result: list[SearchResult] = []

        for article in articles:

            item = SearchResult(
                title = article["title"],
                description = BeautifulSoup(article["snippet"], "html.parser").get_text(),
                url = f"https://en.wikipedia.org/?curid={article["pageid"]}",
                source = "Wikipedia"
            )

            result.append(item)

        return result, None


async def search_github(query: str | None) -> tuple[list[SearchResult], str | None]:

    URL = "https://api.github.com/search/repositories"
    PARAMS = {
        "q": query,
        "per_page": 3
    }
    HEADERS = {"Accept": "application/vnd.github+json"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, params=PARAMS, headers=HEADERS, timeout=None)
            response.raise_for_status()
        except httpx.RequestError:
            return [], "Github: Не удалось выполнить поиск, попробуйте позже"
        except httpx.HTTPStatusError as error:
            return [], f"Ошибка сервиса: {error.response.status_code}"

        data = response.json()

        if not data["items"]:
            return [], "Github: По вашему запросу ничего не найдено"

        articles = data["items"]
        result: list[SearchResult] = []

        for article in articles:

            item = SearchResult(
                title = article["name"],
                description = article["description"] or "Нет описания",
                url = article["html_url"],
                source = "GitHub"
            )
            item.stars = f"Звёзды: {article['stargazers_count']}"
            item.language = f"Язык: {article['language'] or 'не указан'}"

            result.append(item)

        return result, None


async def search_stackoverflow(query: str | None) -> tuple[list[SearchResult], str | None]:
    URL = "https://api.stackexchange.com/2.3/search/advanced"
    PARAMS = {
        "site": "stackoverflow",
        "q": query,
        "sort": "relevance",
        "pagesize": 3,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, params=PARAMS, timeout=None)
            response.raise_for_status()
        except httpx.RequestError:
            return [], "StackOverflow: Не удалось выполнить поиск, попробуйте позже"
        except httpx.HTTPStatusError as error:
            return [], f"Ошибка сервиса: {error.response.status_code}"

        data = response.json()

        if not data["items"]:
            return [], "StackOverflow: По вашему запросу ничего не найдено"

        articles = data["items"]
        result: list[SearchResult] = []

        for article in articles:

            item = SearchResult(
                title = article["title"],
                description = None,
                url = article["link"],
                source = "StackOverflow"
            )
            item.answ_count = f"Кол-во ответов: {article['answer_count']}"
            item.rating = f"Рейтинг: {article['score']}"
            item.is_answered = f"Есть ответ: {'да' if article['is_answered'] else 'нет'}"

            result.append(item)

        return result, None
