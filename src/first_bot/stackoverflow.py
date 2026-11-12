import httpx


async def search_stackoverflow(query: str | None) -> list[str]:
    URL = "https://api.stackexchange.com/2.3/search/advanced"
    PARAMS = {
        "site": "stackoverflow",
        "q": query,
        "sort": "relevance",
        "pagesize": 3,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, params=PARAMS, timeout=10)
            response.raise_for_status()
        except httpx.RequestError:
            return ["StackOverflow: Не удалось выполнить поиск, попробуйте позже"]
        except httpx.HTTPStatusError as error:
            return [f"Ошибка сервиса: {error.response.status_code}"]

        data = response.json()

        if not data["items"]:
            return ["StackOverflow: По вашему запросу ничего не найдено"]

        articles = data["items"]
        result = []

        for article in articles:
            title = article["title"]
            url = article["link"]
            answ_count = article["answer_count"]
            rating = article["score"]
            is_answered = article["is_answered"]
            source = "StackOverflow"

            result.extend([
                title,
                url,
                f"Кол-во ответов: {answ_count}",
                f"Рейтинг: {rating}",
                f"Есть ответ: {'да' if is_answered else 'нет'}",
                source
            ])

        return result
