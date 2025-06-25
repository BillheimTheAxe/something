import argparse
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from collections import deque

# Настройка ведения журнала для мониторинга выполнения программы
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger(__name__)

async def fetch(session, url):
    """Функция для асинхронной загрузки содержания страницы."""
    async with session.get(url) as response:
        return await response.text()

async def get_links(session, url):
    """
    Получает все внутренние ссылки внутри статьи и блока "References",
    подходящие под критерий "/wiki/" и принадлежащие странице.
    """
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')
    links = set()

    # Собираем ссылки из основного тела статьи (#bodyContent)
    for link in soup.select('#bodyContent a'):
        href = link.get('href')
        if href is not None and href.startswith('/wiki/') and ':' not in href:
            links.add(urljoin(url, href))

    # Дополнительно собираем ссылки из раздела "References"
    references_section = soup.find('span', {'class': 'references'})
    if references_section:
        for ref_link in references_section.find_all('a'):
            href = ref_link.get('href')
            if href is not None and href.startswith('/wiki/'):
                links.add(urljoin(url, href))

    return links

def collect_keywords():
    """Запрашиваем у пользователя ключевые слова для поиска."""
    keywords_input = input("Введите ключевые слова через пробел: ").lower().split()
    return keywords_input

def check_keywords_in_page(page_text, keywords):
    """
    Проверяет, содержатся ли все указанные ключевые слова в тексте страницы.
    Возвращает True, если найдено совпадение, иначе False.
    """
    text_words = page_text.lower().split()
    found = all(key in text_words for key in keywords)
    return found

async def bfs_search_with_keywords(start_url, end_url, keywords, rate_limit):
    visited = set()
    paths = {start_url: []}
    queue = asyncio.Queue()
    await queue.put((start_url, 0))  # Начальное состояние: стартовая ссылка и нулевая глубина

    async with aiohttp.ClientSession() as session:
        while not queue.empty():
            current_url, depth = await queue.get()
            
            # Ограничение глубины (глубина <= 5)
            if depth > 5:
                continue
                
            # Ограничение максимальной длины пути (до 5 переходов включительно)
            if len(paths[current_url]) > 5:
                continue
                
            if current_url == end_url:
                return paths[current_url]  # Нашли целевую страницу!

            if current_url in visited:
                continue  # Пропускаем повторно встреченную страницу

            visited.add(current_url)

            # Загружаем страницу и проверяем ключевые слова
            page_text = await fetch(session, current_url)
            if not check_keywords_in_page(page_text, keywords):
                continue  # Страница не подходит по ключевым словам, переходим дальше

            logger.info(f"Обрабатываю страницу: {current_url}")  # Ведение журнала

            # Запрашиваем доступные ссылки на данной странице
            links = await get_links(session, current_url)
            await asyncio.sleep(1 / rate_limit)  # Пауза для соблюдения rate limit

            # Добавляем новые ссылки в очередь для дальнейшей обработки
            for link in links:
                if link not in visited:
                    new_path = paths[current_url] + [current_url]
                    
                    # Контроль максимального количества переходов
                    if len(new_path) <= 5:
                        paths[link] = new_path
                        await queue.put((link, depth + 1))

    return None  # Путь не найден

async def main():
    # Интерактивный ввод URL
    start_url = input("Введите начальную ссылку: ")
    end_url = input("Введите конечную ссылку: ")
    keywords = collect_keywords()
    rate_limit = float(input("Введите ограничение запросов в секунду (минимум 3): "))

    path = await bfs_search_with_keywords(start_url, end_url, keywords, rate_limit)
    if path:
        final_path = " -> ".join(path)
        print(f"Путь найден:\n{final_path}\nКонечная страница: {end_url}")
    else:
        print("Путь не найден.")

if __name__ == "__main__":
    asyncio.run(main())
