import httpx
import time
import random
from bs4 import BeautifulSoup


class RST:
    def __init__(self):
        self.min_price = "1000"
        self.max_price = "15000"
        self.region = "kyiv"
        self.pages = 20
        self.TOKEN = "токен ТГ бота"
        self.CHANEL_ID = "@ссылка на ТГ канал"

    def get_html(self, page: str):
        url = f"https://rst.ua/oldcars/{self.region}/?price[]={self.min_price}&price[]={self.max_price}&start={page}"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "cookie": "_rst=61a6403e130ea1.24318508.34; PHPSESSID=1d65e1ce634d7c95b038f9b7b5ae0f42; _rst_u=61a6403e144ae9.05046325.34; _rst_adview=1; c8557071a593cd9c53c8af71a2b542a8=d42334c48afe5ed2ba3c4245aded194c",
        }
        print(f"парсинг страницы .... {page}")
        resp = httpx.get(url=url, headers=headers)
        if resp.status_code == 200:
            return resp.status_code, resp.content
        else:
            return resp.status_code, f"{page} стр."

    def parsing(self, page: str, html: str):
        cars_list = []
        soup = BeautifulSoup(html, 'html.parser')
        main_div = soup.find("div", class_="rst-page-wrap")
        cars = main_div.find_all("div", class_="rst-ocb-i")
        for car in cars:
            if "Быстрая навигация на RST" not in car.text:
                published = car.find("div", class_="rst-ocb-i-s")
                if "вчера" in published.text or "сегодня" in published.text:
                    car_info = {}
                    title = car.find("h3", class_="rst-ocb-i-h")
                    car_info["title"] = f"{title.text} | {page} стр."

                    image = car.find("div", class_="rst-ocb-i-i")\
                                .find("img").get("src").replace("thumb/", "").replace("middle/", "")
                    car_info["image"] = f"http:{image}"

                    link = car.find("a", class_="rst-ocb-i-a")
                    car_info["link"] = f"https://rst.ua{link['href']}"

                    info_i = car.find_all("li", class_="rst-ocb-i-d-l-i")
                    info_j = car.find_all("li", class_="rst-ocb-i-d-l-j")
                    car_info["price"] = info_i[0].text
                    car_info["year"] = info_i[1].text
                    car_info["engine"] = info_i[2].text
                    car_info["city"] = info_j[0].text
                    car_info["status"] = info_j[1].text

                    description = car.find("div", class_="rst-ocb-i-d-d")
                    car_info["description"] = description.text.replace("\r\n", "")
                    cars_list.append(car_info)
        return cars_list

    def send_to_telegram(self, cars: list):
        url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&parse_mode=html'
        for car in cars:
            message = f"{car['title']}\t\n\n{car['image']}\n{car['price']}\n{car['year']}" \
                f"\n{car['engine']}\n{car['city']}\n{car['status']}\n\n{car['description']}\n{car['link']}"

            with open("links.txt", "r+") as links:

                if car["link"] not in links.read():
                    links.write(car["link"] + '\n')
                    print(f"{car['title']}\n{car['price']}\n{car['year']}\n{car['city']}\n{car['status']}\n\n\n")
                    httpx.get(url % (self.TOKEN, self.CHANEL_ID, (message)))
                    time.sleep(random.uniform(3, 5))

    def start(self):
        for page in range(1, self.pages + 1):
            status_code, html = self.get_html(f"{str(page)}")

            if status_code == 200:
                cars = self.parsing(f"{str(page)}", html)
                self.send_to_telegram(cars)
                time.sleep(random.uniform(5, 15))
            else:
                print(f"{status_code} - {html}")


if __name__ == "__main__":
    pars = RST()
    pars.start()
