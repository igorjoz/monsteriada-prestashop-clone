import http
import os
from http.client import HTTPException
from pathlib import Path

from parsel import Selector
from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
import threading

from urllib3.exceptions import ReadTimeoutError

httpAddressOffset = 22
numberOfFetchedPhotos = 2


def fetchImgGeneral(drvImg, txt):
    err = False
    while True:
        try:
            if err is True:
                err = False
                drvImg.refresh()
            txt_col_prod = Selector(text=drvImg.page_source)
            img_paths_general = [
                txt_col_prod.xpath(txt + "//div[contains(@class, 'product-manufacturer')]/a").css(
                    "img::attr(src)").get()]
            save_img_path = "img/img-general/"
            if img_paths_general[0] is not None:
                for url in img_paths_general:
                    if not Path(save_img_path + url[(url.rfind("/") + 1):]).exists():
                        response = requests.get(url, stream=True, timeout=5)
                        if response.status_code == http.HTTPStatus.NOT_FOUND:
                            raise HTTPException()
                        img_path = save_img_path + url[(url.rfind("/") + 1):]
                        with open(img_path, 'wb') as file:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    file.write(chunk)
                    else:
                        return

            break

        except (HTTPException, ReadTimeoutError, WebDriverException, requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError, TimeoutError) as e:
            err = True
            continue


def fetchImgMedium(drvImg, txt):
    global numberOfFetchedPhotos, httpAddressOffset
    err = False
    while True:
        try:
            if err is True:
                err = False
                drvImg.refresh()
            img_col_prod = Selector(text=drvImg.page_source)
            img_paths_medium = img_col_prod.xpath(txt + "//ul[contains(@class, 'product-images')]").css(
                "img::attr(data-image-medium-src)").getall()[:numberOfFetchedPhotos]
            save_img_path = "img/img-medium/"

            if len(img_paths_medium) != 0:
                for url in img_paths_medium:
                    if not Path(save_img_path + url[(httpAddressOffset + 1):]).exists():
                        response = requests.get(url, stream=True, timeout=5)
                        if response.status_code == http.HTTPStatus.NOT_FOUND:
                            raise HTTPException()
                        dir_path = save_img_path + url[(httpAddressOffset + 1):(url.rfind("/"))]
                        os.makedirs(dir_path, exist_ok=True)
                        img_path = save_img_path + url[(httpAddressOffset + 1):]
                        with open(img_path, 'wb') as file:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    file.write(chunk)
                    else:
                        return

            break

        except (HTTPException, ReadTimeoutError, WebDriverException, requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError, TimeoutError) as e:
            err = True
            continue


def fetchImgLarge(drvImg, txt):
    global numberOfFetchedPhotos, httpAddressOffset
    err = False
    while True:
        try:
            if err is True:
                err = False
                drvImg.refresh()
            img_col_prod = Selector(text=drvImg.page_source)
            img_paths_large = img_col_prod.xpath(txt + "//ul[contains(@class, 'product-images')]").css(
                "img::attr(data-image-large-src)").getall()[:numberOfFetchedPhotos]
            save_img_path = "img/img-large/"

            if len(img_paths_large) != 0:
                for url in img_paths_large:
                    if not Path(save_img_path + url[(httpAddressOffset + 1):]).exists():
                        response = requests.get(url, stream=True, timeout=5)
                        if response.status_code == http.HTTPStatus.NOT_FOUND:
                            raise HTTPException()
                        dir_path = save_img_path + url[(httpAddressOffset + 1):(url.rfind("/"))]
                        os.makedirs(dir_path, exist_ok=True)
                        img_path = save_img_path + url[(httpAddressOffset + 1):]
                        with open(img_path, 'wb') as file:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    file.write(chunk)
                    else:
                        return

            break

        except (HTTPException, ReadTimeoutError, WebDriverException, requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError, TimeoutError) as e:
            err = True
            continue


def scrapeElement(address, driverElement, stridx):
    global httpAddressOffset, numberOfFetchedPhotos
    while True:
        try:

            driverElement.get(address)

            WebDriverWait(driver=driverElement, timeout=5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'row.product-container'))
                and EC.presence_of_element_located((By.CLASS_NAME, 'clearfix.tabs'))
            )

            sel = Selector(text=driverElement.page_source)

            WebDriverWait(driver=driverElement, timeout=5).until(
                EC.presence_of_element_located((By.ID, 'img-col-prod'))
                and EC.presence_of_element_located((By.ID, 'txt-col-prod'))
            )

            img_col_prod_txt = "//div[@class='row product-container']/div[@id='img-col-prod']"
            txt_col_prod_txt = "//div[@class='row product-container']/div[@id='txt-col-prod']"

            fetchImgGeneral(driverElement, txt_col_prod_txt)
            fetchImgMedium(driverElement, img_col_prod_txt)
            fetchImgLarge(driverElement, img_col_prod_txt)

            img_col_prod = sel.xpath("//div[@class='row product-container']/div[@id='img-col-prod']")
            txt_col_prod = sel.xpath("//div[@class='row product-container']/div[@id='txt-col-prod']")
            clearfix_tabs = sel.xpath("//div[@class='clearfix tabs']")

            result = {
                'title': txt_col_prod.xpath("//div[@class='title-status']").css("h1::text").get(),
                'flags': img_col_prod.xpath("section/ul[@class='product-flags']").css("li::text").getall(),
                'locationsOfImgMediumResources': [s[httpAddressOffset:] for s in
                                                  img_col_prod.xpath(
                                                      "section//ul[contains(@class, 'product-images')]").css(
                                                      "img::attr(data-image-medium-src)").getall()[
                                                  :numberOfFetchedPhotos]],
                'locationsOfImgLargeResources': [s[httpAddressOffset:] for s in
                                                 img_col_prod.xpath(
                                                     "section//ul[contains(@class, 'product-images')]").css(
                                                     "img::attr(data-image-large-src)").getall()[
                                                 :numberOfFetchedPhotos]],
                'available': txt_col_prod.xpath("//div[@class='title-status']//span[contains(@class, 'badge')]").css(
                    "span::text").get(),
                'availability': txt_col_prod.xpath("//span[@id='product-availability']/text()").get(),
                'facebookIconLink': txt_col_prod.xpath(
                    "//div[@class='title-status']//div[contains(@class, 'social-sharing')]").css(
                    "a::attr(href)").get(),
                'brandName': txt_col_prod.xpath("//div[contains(@class, 'product-manufacturer')]/a").css(
                    "meta::attr(content)").get() if txt_col_prod.xpath(
                    "//div[contains(@class, 'product-manufacturer')]/a").get() is not None else 'None',
                'locationOfBrandLogoResource': txt_col_prod.xpath(
                    "//div[contains(@class, 'product-manufacturer')]/a").css(
                    "img::attr(src)").get()[httpAddressOffset:] if txt_col_prod.xpath(
                    "//div[contains(@class, 'product-manufacturer')]").get() is not None else 'None',
                'locationOfSearchingByBrandResource': txt_col_prod.xpath(
                    "//div[contains(@class, 'product-manufacturer')]").css(
                    "a::attr(href)").get()[httpAddressOffset:] if txt_col_prod.xpath(
                    "//div[contains(@class, 'product-manufacturer')]").get() is not None else 'None',
                'shortDescription': txt_col_prod.xpath("//div[@class='product-description']").css('p::text').get(),
                'token': txt_col_prod.xpath("//div[@class='product-actions']//input[@name='token']/@value").get(),
                'id_product': txt_col_prod.xpath(
                    "//div[@class='product-actions']//input[@name='id_product']/@value").get(),
                'id_customization': txt_col_prod.xpath(
                    "//div[@class='product-actions']//input[@name='id_customization']/@value").get(),
                'variants': txt_col_prod.xpath("//div[contains(@class, 'product-variants')]").get(),
                'priceData': {
                    'currency': txt_col_prod.xpath(
                        "//div[@class='product-actions']//meta[@itemprop='priceCurrency']/@content").get(),
                    'validUntil': txt_col_prod.xpath(
                        "//div[@class='product-actions']//meta[@itemprop='priceValidUntil']/@content").get(),
                    'price': txt_col_prod.xpath(
                        "//div[@class='product-actions']//span[@itemprop='price']/@content").get(),
                    'priceText': txt_col_prod.xpath("//div[@class='product-actions']//div[@class='current-price']").css(
                        "span::text").get().replace(u'\xa0', " "),
                    'additionalInfo': txt_col_prod.xpath(
                        "//div[@class='product-actions']//div[@class='product-prices']/div[2]").get(),
                    'discounts': txt_col_prod.xpath("//section[contains(@class, 'product-discounts')]").get()
                },
                'tags': txt_col_prod.xpath("//div[@class='iqitproducttags']").css(
                    "a::text").getall() if txt_col_prod.xpath(
                    "//div[@class='iqitproducttags']") is not None else [],
                'tagsLinks': [s[httpAddressOffset:] for s in txt_col_prod.xpath("//div[@class='iqitproducttags']").css(
                    "a::attr(href)").getall()] if txt_col_prod.xpath(
                    "//div[@class='iqitproducttags']") is not None else [],
                'moreData': [{
                    'productDescription': clearfix_tabs.xpath("//ul[contains(@class, 'nav-tabs')]/li[1]").css(
                        "a::text").get(),
                    'productDescriptionContent': clearfix_tabs.xpath("//div[@id='tab-content']/div[1]/div[1]").get()
                },
                    {
                        'productDetails': clearfix_tabs.xpath("//ul[contains(@class, 'nav-tabs')]/li[2]").css(
                            "a::text").get(),
                        'productDetailsContent': clearfix_tabs.xpath("//div[@id='product-details']/section/dl").get()
                    }
                ]
            }

            print(stridx + ". Scraped " + result['title'])
            return result

        except (HTTPException, ReadTimeoutError, WebDriverException, requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError, TimeoutError) as e:
            continue

        except NoSuchElementException as e:
            print("Nie zaladowalo sie")
            continue


def scrapeGroup(address, driverCat, stridx):
    current_page = address
    current_page_nr = 1

    elements = []

    while True:
        print(stridx + ". Scraping page nr " + str(current_page_nr))
        elementsBeforeError = elements
        try:
            driverCat.get(current_page)
            WebDriverWait(driver=driverCat, timeout=5).until(
                EC.presence_of_element_located((By.ID, 'js-product-list'))
            )
            products = driverCat.find_elements(By.XPATH,
                                               "//div[@id='js-product-list']//div[@itemprop='itemListElement']//a[@itemprop='url']")
            productsAddr = [pr.get_attribute('href') for pr in products]
            for productAddr in productsAddr:
                elements.append(scrapeElement(productAddr, driverCat, stridx))

            driverCat.get(current_page)
            WebDriverWait(driver=driverCat, timeout=5).until(
                EC.presence_of_element_located((By.ID, 'js-product-list'))
            )
            try:
                nextPage = driverCat.find_element(By.XPATH, "//li[@class='next_li']/a")
                nextPageAddr = nextPage.get_attribute('href')

                current_page = nextPageAddr
                current_page_nr += 1

            except NoSuchElementException as e:
                break

        except (HTTPException, ReadTimeoutError, WebDriverException, requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError, TimeoutError) as e:
            elements = elementsBeforeError
            continue

    return elements


def defineSubcategoriesTree(subs, idx, txt):
    global httpAddressOffset
    err = False
    while True:
        try:

            if err is True:
                err = False
                subs.refresh()
            subbbDirs = subs.find_elements(By.XPATH, txt[0])[idx + 1]
            subbDirs = subbbDirs.find_element(By.XPATH, txt[1])
            subDirs = subbDirs.find_elements(By.XPATH, ".//div[@class='ets_mm_block_content']")

            subDirDatas = []

            for subDir in subDirs:
                s = subDir.find_element(By.XPATH, ".//a[1]")
                try:
                    subSubDir = subDir.find_element(By.XPATH, ".//li[@class='has-sub']")
                    subSubDirData = [{'name': s.get_attribute('innerText'), 'address': s.get_attribute('href')} for s in
                                     subSubDir.find_elements(By.XPATH, "./ul/li/a")]

                    subDirDatas.append(
                        {'name': s.get_attribute('innerText'), 'address': s.get_attribute('href'),
                         'data': subSubDirData})

                except NoSuchElementException as err:
                    subDirDatas.append({
                        'name': s.get_attribute('innerText'),
                        'address': s.get_attribute('href'),
                        'data': None
                    })

            return subDirDatas

        except (HTTPException, ReadTimeoutError, WebDriverException, requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError, TimeoutError) as e:
            err = True
            continue


def scrapeSubcategories(subDirDatas, driverSubs, stridx):
    result = []

    for subcategory in subDirDatas:
        subName = subcategory['name']
        subAddress = subcategory['address'][httpAddressOffset:]
        print(stridx + ". Scraping subcategory " + subName)
        if subcategory['data'] is not None:
            subSubData = []
            for subSubCategory in subcategory['data']:
                print(stridx + ". Scraping sub-subcategory " + subSubCategory['name'])
                subSubData.append({
                    'sub-subcategoryName': subSubCategory['name'],
                    'sub-subcategoryAddress': subSubCategory['address'][httpAddressOffset:],
                    'sub-subcategoryContent': scrapeGroup(subSubCategory['address'], driverSubs, stridx)
                })
                print(stridx + ". Scraped sub-subcategory " + subSubCategory['name'])
            result.append({
                'subcategoryName': subName,
                'subCategoryAddress': subAddress,
                'subCategoryContent': subSubData
            })
        else:
            result.append({
                'subcategoryName': subName,
                'subCategoryAddress': subAddress,
                'subCategoryContent': scrapeGroup(subcategory['address'],
                                                  driverSubs, stridx) if subName != "WSZYSTKIE PRODUKTY" else []
            })

        print(stridx + ". Scraped subcategory " + subName)

    return result


def scrapeCategories(driver, baseAddress, idx):
    global httpAddressOffset
    categoryData = None
    stridx = str(idx)
    while True:
        try:
            driver.get(baseAddress)

            WebDriverWait(driver=driver, timeout=5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'x13eucookies__btn--deny'))
            )
            driver.find_element(By.XPATH, "//button[contains(@class, 'x13eucookies__btn--deny')]").click()

            WebDriverWait(driver=driver, timeout=5).until(
                EC.presence_of_element_located((By.ID, 'header'))
            )

            categories = driver.find_elements(By.XPATH,
                                              "//header[@id='header']//ul[contains(@class, 'mm_menus_ul')]/li[contains(@class, 'mm_menus_li')]")
            categories.pop()
            categories = categories[1:]

            category = categories[idx]

            ActionChains(driver=driver).move_to_element(category.find_element(By.XPATH, "./a/span")).perform()
            WebDriverWait(driver=driver, timeout=5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'mm_columns_ul'))
            )

            catName = category.find_element(By.XPATH, "./a/span").get_attribute('innerText')
            catAddress = category.find_element(By.XPATH, "./a").get_attribute('href')
            try:
                category.find_element(By.XPATH, ".//ul[@class='mm_columns_ul']")

                subcategories_txt = [
                    "//header[@id='header']//ul[contains(@class, 'mm_menus_ul')]/li[contains(@class, 'mm_menus_li')]",
                    ".//ul[@class='mm_columns_ul']"]

                categoryData = {
                    'name': catName,
                    'address': catAddress,
                    'data': defineSubcategoriesTree(driver, idx, subcategories_txt)
                }

            except NoSuchElementException as e:

                categoryData = {
                    'name': catName,
                    'address': catAddress,
                    'data': None
                }

            break

        except (HTTPException, ReadTimeoutError, WebDriverException, requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError, TimeoutError) as e:
            continue

    print(stridx + ". Scraping category " + categoryData['name'])

    if categoryData['data'] is not None:
        resultData = {
            'categoryName': categoryData['name'],
            'categoryAddress': categoryData['address'][httpAddressOffset:],
            'categoryContent': scrapeSubcategories(categoryData['data'], driver, stridx)
        }
    else:
        resultData = {
            'categoryName': categoryData['name'],
            'categoryAddress': categoryData['address'][httpAddressOffset:],
            'categoryContent': scrapeGroup(categoryData['address'], driver, stridx)
        }

    print(stridx + ". Scraped category " + categoryData['name'])

    with open("Data/" + categoryData['name'] + ".json", 'w+', encoding='utf-8') as file:
        json.dump(resultData, file, indent=5, ensure_ascii=False)

    driver.quit()


if __name__ == '__main__':
    options = Options()
    options.add_argument("-headless")
    options.add_argument("-width=1020")
    options.add_argument("-height=680")
    driver = webdriver.Firefox(options=options)
    baseAddress = "https://monsteriada.pl"
    driver.get(baseAddress)

    driver.find_element(By.XPATH, "//button[contains(@class, 'x13eucookies__btn--deny')]").click()

    WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.ID, 'header'))
    )

    categories = driver.find_elements(By.XPATH,
                                      "//header[@id='header']//ul[contains(@class, 'mm_menus_ul')]/li[contains(@class, 'mm_menus_li')]")
    categories.pop()
    categories = categories[1:]
    i = 0

    taskList = []

    for category in categories:
        drv = webdriver.Firefox(options=options)
        drv.set_page_load_timeout(5)
        taskList.append(threading.Thread(target=scrapeCategories,
                                         args=(drv, baseAddress, i,)))

        i += 1

    for task in taskList:
        task.start()

    for task in taskList:
        task.join()

    driver.quit()
