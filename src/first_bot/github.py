import httpx


async def search_github(query: str | None) -> list[str]:

    URL = "https://api.github.com/search/repositories"
    PARAMS = {
        "q": query,
        "per_page": 3
    }
    HEADERS = {"Accept": "application/vnd.github+json"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, params=PARAMS, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except httpx.RequestError:
            return ["Github: Не удалось выполнить поиск, попробуйте позже"]
        except httpx.HTTPStatusError as error:
            return [f"Ошибка сервиса: {error.response.status_code}"]

        data = response.json()

        if not data["items"]:
            return ["Github: По вашему запросу ничего не найдено"]

        articles = data["items"]
        result = []

        for article in articles:
            title = article["name"] # название
            description = article["description"] # описание
            stars = article["stargazers_count"] # кол-во звёзд
            language = article["language"] # основной язык
            url = article["html_url"] # ссылка на репозиторий
            source = "GitHub"

            result.extend([
                title,
                description or "Нет описания",
                f"{stars} звёзд",
                language or "Язык не указан",
                url,
                source
            ])

            # result.append(title)
            # result.append(description or "Нет описания")
            # result.append(f"{stars} звёзд")
            # result.append(language or "Язык не указан")
            # result.append(url)


        return result
