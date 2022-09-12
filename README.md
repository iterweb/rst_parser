# RST Парсер
Скрипт для парсинга популярного в Украине сайта **rst.ua**, с отправкой в Телеграм.
## Как работает
Скрипт ищет все объявления, которые были добавлены "сегодня" и "вчера". Если объявление было найдено, отправит сообщение в Телеграм, а ссылку на авто сохранит в файле **links.txt**.
## Требования
* [python 3.7+](https://www.python.org/)
* pip install httpx
* pip install beautifulsoup4
## Как пользоваться
* 9 строка - минимальная цена в $
* 10 строка - максимальная цена в $
* 11 строка - область для поиска (можно посмотреть в строке браузера)
* 12 строка - количество страниц для парсинга
* 13 строка - токен ТГ бота
* 14 строка - id канала в ТГ
* запуск ```python rst.py```
**Важно!** Бота нужно добавить в Телеграм канал, как администратора!