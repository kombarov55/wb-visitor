from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
browser = webdriver.Chrome(r"C:\Users\komba\Documents\chromedriver.exe", options=options)
browser.implicitly_wait(5000)

def get_name_and_img_by_article(article: str) -> (str, str):
    browser.get("https://www.wildberries.ru/catalog/{}/detail.aspx".format(article))
    name = browser.find_element(By.XPATH, "(//h1[@data-link='text{:selectedNomenclature^goodsName || product^goodsName}'])[1]").text

    browser.find_element(By.XPATH, "(//canvas[@class='photo-zoom__preview j-image-canvas'])[1]").click()
    src = browser.find_element(By.XPATH, "//div[@class='swiper-slide img-plug swiper-slide-visible swiper-slide-active swiper-slide-thumb-active']//img").get_attribute("src")

    return name, src


def get_name_and_img_by_brand(brand: str) -> (str, str, str):
    browser.get("https://www.wildberries.ru/brands/{}".format(brand))
    elements = browser.find_elements(By.CSS_SELECTOR, ".product-card span.goods-name")
    names = list(map(lambda v: v.text, elements))

    elements = browser.find_elements(By.CSS_SELECTOR, ".product-card img")
    imgs = list(map(lambda v: v.get_attribute("src"), elements))

    elements = browser.find_elements(By.CSS_SELECTOR, ".product-card a.j-card-link")
    articles = list(map(lambda v: v.get_attribute("href").split("/")[4], elements))

    result = []

    for i in range(0, len(names)):
        result.append((articles[i], names[i], imgs[i]))

    return result


def get_name_and_img_by_shop(shop: str) -> (str, str, str):
    browser.get("https://www.wildberries.ru/seller/{}".format(shop))
    elements = browser.find_elements(By.CSS_SELECTOR, ".product-card span.goods-name")
    names = list(map(lambda v: v.text, elements))

    elements = browser.find_elements(By.CSS_SELECTOR, ".product-card img")
    imgs = list(map(lambda v: v.get_attribute("src"), elements))

    elements = browser.find_elements(By.CSS_SELECTOR, ".product-card a.j-card-link")
    articles = list(map(lambda v: v.get_attribute("href").split("/")[4], elements))

    result = []

    for i in range(0, len(names)):
        result.append((articles[i], names[i], imgs[i]))

    return result
