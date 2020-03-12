from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    ElementNotInteractableException
import time
import csv

SCROLL_PAUSE_TIME = 3
FILENAME = "product.csv"


class Product:
    def __init__(self, name, price, a_link, ):
        self.__name = name
        self.__price = price
        self.__a_link = a_link

    def set_price(self, price):
        self.__price = price

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_a_link(self):
        return self.__a_link


def get_full_html():
    url = "https://www.petsonic.com/pienso-royal-canin-para-perros/"
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    pages_remaining = True
    while pages_remaining:
        try:
            btn = driver.find_element_by_css_selector('button.loadMore.next.button.lnk_view.btn.btn-default')
            time.sleep(SCROLL_PAUSE_TIME)
            btn.click()
            time.sleep(SCROLL_PAUSE_TIME)
            driver.execute_script("arguments[0].scrollIntoView();", btn)
            driver.execute_script("window.scrollBy(0, -250);")
            time.sleep(SCROLL_PAUSE_TIME)
        except ElementNotInteractableException:
            pages_remaining = False
        except ElementClickInterceptedException:
            elem = driver.find_element_by_xpath('//div[contains(@class,"cn_modal_backdrop") and contains(@class, '
                                                '"undefined")] | '
                                                '//iframe[contains(@class,"cn_modal_iframe")] | '
                                                '//div[contains(@class,"cn_content") and contains(@class, '
                                                '"none")] | '
                                                '//a[contains(@href, "cn_close_modal")]')
            elem.click()
            time.sleep(SCROLL_PAUSE_TIME)
    return driver.page_source


def parce_html():
    product_list = []
    html = get_full_html()
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.findAll('a', {'class': 'product-name'})
    for item_a in a:
        product_list.append(Product(item_a.attrs['title'], "", item_a.attrs['href']))
    span = soup.findAll('span', {'class': 'price product-price'})
    for i in range(len(product_list)):
        product_list[i].set_price(span[i].text)
    return product_list


def ctreate_csv():
    product_parce = parce_html()
    products = []
    with open(FILENAME, "w", encoding="utf-8") as file:
        columns = ["product_name", "price", 'link']
        writer = csv.DictWriter(file, fieldnames=columns)
        for item in product_parce:
            products.append({"product_name": f"{item.get_name()}", "price": f"{item.get_price()}",
                       "link": f"{item.get_a_link()}"})
        writer.writerows(products)


ctreate_csv()


