from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome(r"C:\Users\komba\Documents\chromedriver.exe")
browser.implicitly_wait(5000)

def get_name_and_img_by_article(article) -> (str, str):
    browser.get("https://www.wildberries.ru/catalog/{}/detail.aspx".format(article))
    name = browser.find_element(By.XPATH, "(//h1[@data-link='text{:selectedNomenclature^goodsName || product^goodsName}'])[1]").text

    browser.find_element(By.XPATH, "(//canvas[@class='photo-zoom__preview j-image-canvas'])[1]").click()
    src = browser.find_element(By.XPATH, "//div[@class='swiper-slide img-plug swiper-slide-visible swiper-slide-active swiper-slide-thumb-active']//img").get_attribute("src")

    return name, src
