from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
import random


def testA(driverA, source):
    result = "passed"
    how_many_products_per_cat = 5
    how_many_max = 3

    print("Test A sie rozpoczyna")

    try:
        driverA.get(source)
        WebDriverWait(driver=driverA, timeout=25).until(
            EC.presence_of_element_located((By.ID, 'header'))
        )

        categories = driverA.find_elements(By.XPATH,
                                           "//header[@id='header']//div[@class='main-navigation-janek']/a[@class='button-item']")
        categories_temp = []
        categories_temp.append(categories[3])

        ddmenu = driverA.find_element(By.CLASS_NAME, "button-item.topic-items-button")
        driverA.execute_script("arguments[0].scrollIntoView();",
                               ddmenu)
        driverA.execute_script("window.scrollBy(0, -100);")
        WebDriverWait(driver=driverA, timeout=25).until(
            EC.visibility_of(ddmenu)
        )
        ActionChains(driver=driverA).move_to_element(ddmenu).perform()
        categories_temp.append(driverA.find_element(By.XPATH, ".//li[@id='category-148']/a"))

        categories = categories_temp
        cat_addresses = []

        for category in categories:
            cat_addresses.append(category.get_attribute('href'))

        for cat_address in cat_addresses:
            driverA.get(cat_address)
            WebDriverWait(driver=driverA, timeout=25).until(
                EC.presence_of_element_located((By.ID, 'js-product-list'))
            )

            product_addresses = []
            products = driverA.find_elements(By.XPATH,
                                             ".//div[@class='product-description']/h2/a")

            while len(product_addresses) != how_many_products_per_cat:
                try:
                    products[-1].find_element(By.XPATH, "./../../../ul/li[@class='product-flag out_of_stock']")

                except NoSuchElementException:
                    product_addresses.append(products[-1].get_attribute('href'))

                products.pop()
                if len(products) == 0:
                    nxtPage = driverA.find_element(By.XPATH,
                                                     ".//a[contains(text(), 'Następny')]")
                    nxtPageSrc = nxtPage.get_attribute('href')
                    nxtPage.click()
                    while driverA.current_url != nxtPageSrc:
                        continue
                    WebDriverWait(driver=driverA, timeout=25).until(
                        EC.presence_of_element_located((By.ID, 'js-product-list'))
                    )
                    products = driverA.find_elements(By.XPATH,
                                                     ".//div[@class='product-description']/h2/a")
                    continue



            for product_address in product_addresses:
                while True:
                    try:
                        driverA.get(product_address)
                        WebDriverWait(driver=driverA, timeout=25).until(
                            EC.presence_of_element_located(
                                (By.CLASS_NAME, 'product-add-to-cart.js-product-add-to-cart'))
                        )

                        col_prod_txt = driverA.find_element(By.XPATH,
                                                            ".//div[@class='product-add-to-cart js-product-add-to-cart']")

                        items_up = col_prod_txt.find_element(By.XPATH,
                                                             ".//button[@class='btn btn-touchspin js-touchspin bootstrap-touchspin-up']")

                        driverA.execute_script("arguments[0].scrollIntoView();",
                                               items_up)
                        driverA.execute_script("window.scrollBy(0, -100);")
                        WebDriverWait(driver=driverA, timeout=25).until(
                            EC.visibility_of(items_up)
                        )

                        how_many = random.randint(1, how_many_max)
                        for i in range(how_many - 1):
                            WebDriverWait(driver=driverA, timeout=25).until(
                                EC.element_to_be_clickable(items_up)
                            )
                            items_up.click()

                        add_to_cart = col_prod_txt.find_element(By.XPATH,
                                                                ".//button[@class='btn btn-primary add-to-cart']")
                        WebDriverWait(driver=driverA, timeout=25).until(
                            EC.element_to_be_clickable(add_to_cart)
                        )
                        add_to_cart.click()

                        WebDriverWait(driver=driverA, timeout=25).until(
                            EC.visibility_of_element_located((By.ID, 'blockcart-modal'))
                        )

                        blockcart = driverA.find_element(By.ID, 'blockcart-modal')

                        how_many_added = int(blockcart.find_element(By.XPATH,
                                                                    ".//div[@class='modal-body']/div/div[1]/div/div[2]/span/strong").text)

                        adding_result_text = blockcart.find_element(By.XPATH, "//h4[@id='myModalLabel']").text[1:]

                        if how_many_added != how_many or adding_result_text != "Produkt dodany poprawnie do Twojego koszyka":
                            raise ValueError()

                        print("Test A pomyślnie dodal obiekt do koszyka")

                        break

                    except TimeoutException as e:
                        continue

        print("Test A sie zakonczyl")

    except ValueError as e:
        result = "failed"
        print("Test A nieudany")

    '''
    except Exception as e:
        result = "failed"
        print("W tescie A wystapil wyjatek " + str(type(e)))
        '''

    return result


def testB(driverB, source):
    result = "passed"
    print("Test B sie rozpoczyna")
    try:
        driverB.get(source)
        WebDriverWait(driver=driverB, timeout=25).until(
            EC.presence_of_element_located((By.ID, 'header'))
        )

        search_bar = driverB.find_element(By.XPATH,
                                          ".//input[@class='ui-autocomplete-input']")

        driverB.execute_script("arguments[0].scrollIntoView();",
                               search_bar)
        driverB.execute_script("window.scrollBy(0, -100);")
        WebDriverWait(driver=driverB, timeout=25).until(
            EC.element_to_be_clickable(
                search_bar)
        )
        search_bar.send_keys('yoda')
        search_bar.send_keys(Keys.ENTER)

        WebDriverWait(driver=driverB, timeout=25).until(
            EC.presence_of_element_located((By.ID, "js-product-list"))
        )

        print("Test B wyszukal produkt po nazwie")

        products = driverB.find_elements(By.XPATH,
                                         ".//div[@class='product-description']/h2/a")

        list_of_checked = []
        how_many_checked = 0
        how_many = len(products)
        while how_many_checked != how_many:
            idx = random.randint(0, how_many - 1)
            if idx in list_of_checked:
                continue
            try:
                products[idx].find_element(By.XPATH, "./../../../ul/li[@class='product-flag out_of_stock']")
                list_of_checked.append(idx)
                how_many_checked += 1
                continue

            except NoSuchElementException:
                driverB.get(products[idx].get_attribute('href'))
                break

        if how_many_checked == how_many:
            print("TEST B: Wszystkie produkty byly out-of-stock")
            raise ValueError

        WebDriverWait(driver=driverB, timeout=25).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-add-to-cart.js-product-add-to-cart'))
        )

        col_prod_txt = driverB.find_element(By.XPATH,
                                            ".//div[@class='product-add-to-cart js-product-add-to-cart']")

        add_to_cart = col_prod_txt.find_element(By.XPATH, ".//button[@class='btn btn-primary add-to-cart']")

        driverB.execute_script("arguments[0].scrollIntoView();",
                               add_to_cart)
        driverB.execute_script("window.scrollBy(0, -100);")

        WebDriverWait(driver=driverB, timeout=25).until(
            EC.element_to_be_clickable(add_to_cart)
        )
        add_to_cart.click()

        WebDriverWait(driver=driverB, timeout=25).until(
            EC.visibility_of_element_located((By.ID, 'blockcart-modal'))
        )

        blockcart = driverB.find_element(By.ID, 'blockcart-modal')
        how_many_added = int(
            blockcart.find_element(By.XPATH, ".//span[contains(text(), 'Ilość:')]/strong").text)
        adding_result_text = blockcart.find_element(By.XPATH, "//h4[@id='myModalLabel']").text[1:]
        if how_many_added != 1 or adding_result_text != "Produkt dodany poprawnie do Twojego koszyka":
            raise ValueError()

        print("Test B poprawnie dodal do koszyka")
        print("Test B sie zakonczyl")

    except ValueError as e:
        result = "failed"
        print("Test B nieudany")

    '''
    except Exception as e:
        result = "failed"
        print("W tescie B wystapil wyjatek " + str(type(e)))
    '''

    return result


def testC(driverC, source):
    result = "passed"
    how_many_to_delete = 3
    print("Test C sie rozpoczyna")
    try:
        driverC.get(source)
        WebDriverWait(driver=driverC, timeout=25).until(
            EC.presence_of_element_located((By.ID, "main"))
        )

        items_start = driverC.find_elements(By.XPATH, "//section[@id='main']//li[@class='cart-item']")
        items_start_count = len(items_start)

        for _ in range(how_many_to_delete):
            item_tbd = driverC.find_elements(By.XPATH, "//section[@id='main']//li[@class='cart-item']")[0]
            driverC.execute_script("arguments[0].scrollIntoView();",
                                   item_tbd.find_element(By.XPATH, ".//button[@class='btn btn-touchspin js-touchspin "
                                                                   "js-decrease-product-quantity "
                                                                   "bootstrap-touchspin-down']"))
            driverC.execute_script("window.scrollBy(0, -100);")
            item_tbd_how_many = int(item_tbd.find_element(By.XPATH, ".//input[@class='js-cart-line-product-quantity "
                                                                    "form-control']").get_attribute('value'))

            arrow_down_tbd = item_tbd.find_element(By.XPATH, ".//button[@class='btn btn-touchspin "
                                                             "js-touchspin js-decrease-product-quantity "
                                                             "bootstrap-touchspin-down']")

            for _ in range(item_tbd_how_many):
                WebDriverWait(driver=driverC, timeout=25).until(
                    EC.element_to_be_clickable(arrow_down_tbd)
                    and EC.visibility_of(arrow_down_tbd)
                )
                arrow_down_tbd.click()

            print("Test C usunal produkt z koszyka")

            WebDriverWait(driver=driverC, timeout=25).until(
                EC.invisibility_of_element(item_tbd)
            )

        items_end = driverC.find_elements(By.XPATH, "//section[@id='main']//li[@class='cart-item']")
        items_end_count = len(items_end)

        if items_end_count != items_start_count - how_many_to_delete:
            raise ValueError()

    except ValueError as e:
        result = "failed"
        print("Test C nieudany")

    '''
    except Exception as e:
        result = "failed"
        print("W tescie C wystapil wyjatek " + str(type(e)))
        '''

    print("Test C sie zakonczyl")
    return result


def testEFGH(driverE, source):
    result = ["failed", "failed", "failed", "failed"]

    # TEST E------------------------------------------------------------------------------

    print("Test E sie rozpoczyna")
    try:
        driverE.get(source)
        WebDriverWait(driver=driverE, timeout=25).until(
            EC.presence_of_element_located((By.ID, "main"))
        )

        driverE.find_element(By.XPATH,
                             ".//div[@class='checkout cart-detailed-actions js-cart-detailed-actions card-block']").click()

        try:
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cart-grid-body.col-xs-12.col-lg-8"))
            )
            result[0] = "passed"
            print("Test E sie zakonczyl")

        except TimeoutException:
            raise ValueError("E")

        # first form

        di_first_stage = driverE.find_element(By.ID, "checkout-personal-information-step")

        try:
            di_first_stage.find_element(By.XPATH, ".//span[@class='step-edit text-muted']")

        except NoSuchElementException:

            necessary_customer_form_rows = di_first_stage.find_elements(By.XPATH,
                                                                        ".//form[@id='customer-form']/div/div")
            tos_check = necessary_customer_form_rows[-1].find_element(By.CLASS_NAME,
                                                                      "material-icons.rtl-no-flip.checkbox-checked")
            rodo_check = necessary_customer_form_rows[7].find_element(By.CLASS_NAME,
                                                                      "material-icons.rtl-no-flip.checkbox-checked")
            first_stage_gender = necessary_customer_form_rows[0].find_element(By.ID, "field-id_gender-1")
            first_stage_name = necessary_customer_form_rows[1].find_element(By.ID, "field-firstname")
            first_stage_surname = necessary_customer_form_rows[2].find_element(By.ID, "field-lastname")
            first_stage_mail = necessary_customer_form_rows[3].find_element(By.ID, "field-email")
            first_stage_button = di_first_stage.find_element(By.XPATH, ".//form[@id='customer-form']/footer/button")

            driverE.execute_script("arguments[0].scrollIntoView();", rodo_check)
            driverE.execute_script("window.scrollBy(0, -100);")
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.element_to_be_clickable(rodo_check.find_element(By.XPATH, "./../.."))
            )
            rodo_check.find_element(By.XPATH, "./../..").click()

            driverE.execute_script("arguments[0].scrollIntoView();", tos_check)
            driverE.execute_script("window.scrollBy(0, -100);")
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.element_to_be_clickable(tos_check.find_element(By.XPATH, "./../.."))
            )
            tos_check.find_element(By.XPATH, "./../..").click()

            driverE.execute_script("arguments[0].scrollIntoView();", first_stage_gender)
            driverE.execute_script("window.scrollBy(0, -100);")
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.element_to_be_clickable(first_stage_gender.find_element(By.XPATH, "./../.."))
            )
            first_stage_gender.find_element(By.XPATH, "./../..").click()

            driverE.execute_script("arguments[0].scrollIntoView();", first_stage_name)
            driverE.execute_script("window.scrollBy(0, -100);")
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.element_to_be_clickable(
                    first_stage_name)
            )
            first_stage_name.send_keys('A')

            driverE.execute_script("arguments[0].scrollIntoView();", first_stage_surname)
            driverE.execute_script("window.scrollBy(0, -100);")
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.element_to_be_clickable(
                    first_stage_surname)
            )
            first_stage_surname.send_keys('A')

            driverE.execute_script("arguments[0].scrollIntoView();", first_stage_mail)
            driverE.execute_script("window.scrollBy(0, -100);")
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.element_to_be_clickable(
                    first_stage_mail)
            )
            first_stage_mail.send_keys('A@gmail.com')

            driverE.execute_script("arguments[0].scrollIntoView();", first_stage_button)
            driverE.execute_script("window.scrollBy(0, -100);")
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.element_to_be_clickable(
                    first_stage_button)
            )
            first_stage_button.click()

        # second form

        WebDriverWait(driver=driverE, timeout=25).until(
            EC.presence_of_element_located((By.ID, "checkout-addresses-step"))
        )

        di_second_stage = driverE.find_element(By.ID, "checkout-addresses-step")
        try:
            driverE.find_element(By.XPATH, ".//a[contains(text(), 'dodaj nowy adres')]")
        except NoSuchElementException:
            necessary_second_stage_rows = driverE.find_elements(By.XPATH,
                                                                "//div[@id='delivery-address']/div/section/div")
            second_stage_address = necessary_second_stage_rows[5].find_element(By.XPATH,
                                                                               ".//input[@class='form-control']")
            second_stage_postcode = necessary_second_stage_rows[7].find_element(By.XPATH,
                                                                                ".//input[@class='form-control']")
            second_stage_city = necessary_second_stage_rows[8].find_element(By.XPATH, ".//input[@class='form-control']")
            second_stage_phone = necessary_second_stage_rows[10].find_element(By.XPATH,
                                                                              ".//input[@class='form-control']")

            driverE.execute_script("arguments[0].scrollIntoView();", second_stage_address)
            driverE.execute_script("window.scrollBy(0, -100);")
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.element_to_be_clickable(second_stage_address)
            )
            second_stage_address.send_keys('ul. Narutowicza 13')

            driverE.execute_script("arguments[0].scrollIntoView();", second_stage_postcode)
            driverE.execute_script("window.scrollBy(0, -100);")
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.element_to_be_clickable(second_stage_postcode)
            )
            second_stage_postcode.send_keys('80-233')

            driverE.execute_script("arguments[0].scrollIntoView();", second_stage_city)
            driverE.execute_script("window.scrollBy(0, -100);")
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.element_to_be_clickable(second_stage_city)
            )
            second_stage_city.send_keys('Gdańsk')

            driverE.execute_script("arguments[0].scrollIntoView();", second_stage_phone)
            driverE.execute_script("window.scrollBy(0, -100);")
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.element_to_be_clickable(second_stage_phone)
            )
            second_stage_phone.send_keys('123456789')

        second_stage_button = di_second_stage.find_element(By.XPATH, ".//button[contains(text(), 'Dalej')]")
        driverE.execute_script("arguments[0].scrollIntoView();", second_stage_button)
        driverE.execute_script("window.scrollBy(0, -100);")
        WebDriverWait(driver=driverE, timeout=25).until(
            EC.element_to_be_clickable(
                second_stage_button)
        )
        second_stage_button.click()

        # TEST G-------------------------------------------------------------------------------

        print("Test G sie rozpoczyna")

        WebDriverWait(driver=driverE, timeout=25).until(
            EC.presence_of_element_located((By.ID, "checkout-delivery-step"))
        )

        di_third_stage = driverE.find_element(By.ID, "checkout-delivery-step")

        third_stage_delivery = di_third_stage.find_element(By.XPATH, ".//input[@id='delivery_option_14']/..")
        third_stage_button = di_third_stage.find_element(By.XPATH, ".//button[contains(text(), 'Dalej')]")

        driverE.execute_script("arguments[0].scrollIntoView();", third_stage_delivery)
        driverE.execute_script("window.scrollBy(0, -100);")
        WebDriverWait(driver=driverE, timeout=25).until(
            EC.element_to_be_clickable(third_stage_delivery)
        )
        third_stage_delivery.click()

        driverE.execute_script("arguments[0].scrollIntoView();", third_stage_button)
        driverE.execute_script("window.scrollBy(0, -100);")
        WebDriverWait(driver=driverE, timeout=25).until(
            EC.element_to_be_clickable(
                third_stage_button)
        )
        third_stage_button.click()

        try:
            WebDriverWait(driver=driverE, timeout=25).until(
                EC.presence_of_element_located((By.ID, "checkout-payment-step"))
                and EC.visibility_of_element_located((By.ID, "checkout-payment-step"))
            )
            result[2] = "passed"
            print("Test G sie zakonczyl")

        except TimeoutException:
            raise ValueError("G")

        # TEST F---------------------------------------------------------------------------------------------------

        print("Test F sie rozpoczyna")

        WebDriverWait(driver=driverE, timeout=25).until(
            EC.presence_of_element_located((By.ID, "checkout-payment-step"))
            and EC.visibility_of_element_located((By.ID, "checkout-payment-step"))
        )

        di_fourth_stage = driverE.find_element(By.ID, "checkout-payment-step")
        fourth_stage_payment = di_fourth_stage.find_element(By.ID, "payment-option-3").find_element(By.XPATH, "./..")

        driverE.execute_script("arguments[0].scrollIntoView();", fourth_stage_payment)
        driverE.execute_script("window.scrollBy(0, -100);")
        WebDriverWait(driver=driverE, timeout=25).until(
            EC.element_to_be_clickable(
                fourth_stage_payment)
        )
        fourth_stage_payment.click()

        WebDriverWait(driver=driverE, timeout=25).until(
            EC.element_to_be_clickable(
                fourth_stage_payment)
        )
        try:
            driverE.find_element(By.XPATH, ".//p[text()='Płacisz za towar przy dostawie']")
            result[1] = "passed"
            print("Test F sie zakonczyl")

        except NoSuchElementException:
            raise ValueError("F")

        # TEST H------------------------------------------------------------------------------------------------------

        print("Test H sie rozpoczyna")

        fourth_stage_conds = di_fourth_stage.find_element(By.XPATH,
                                                          ".//input[@id='conditions_to_approve[terms-and-conditions]']")

        driverE.execute_script("arguments[0].scrollIntoView();", fourth_stage_conds)
        driverE.execute_script("window.scrollBy(0, -100);")

        driverE.execute_script("arguments[0].click();", fourth_stage_conds)

        fourth_stage_button = di_fourth_stage.find_element(By.XPATH, ".//button[contains(text(), 'Złóż zamówienie')]")

        driverE.execute_script("arguments[0].scrollIntoView();", fourth_stage_button)
        driverE.execute_script("window.scrollBy(0, -100);")
        WebDriverWait(driver=driverE, timeout=25).until(
            EC.element_to_be_clickable(
                fourth_stage_button)
        )
        fourth_stage_button.click()

        WebDriverWait(driver=driverE, timeout=25).until(
            EC.presence_of_element_located((By.ID,
                                            "content-hook_order_confirmation"))
        )

        if "Twoje zamówienie zostało potwierdzone" in driverE.page_source:
            result[3] = "passed"
            print("Test H sie zakonczyl")

        else:
            raise ValueError("H")



    except ValueError as e:
        print("Test " + str(e) + " nieudany")

    '''
    except Exception as e:
        print("Podczas testow E-H wystapil wyjatek " + str(type(e)))
        '''

    return result


def testD(driver, source):  # create new account
    print("Test D sie rozpoczyna")

    try:
        driver.get(source)
        WebDriverWait(driver=driver, timeout=25).until(
            EC.presence_of_element_located((By.ID, '_desktop_user_info'))
        )
        driver.find_element(By.ID, '_desktop_user_info').click()

        WebDriverWait(driver=driver, timeout=25).until(
            EC.presence_of_element_located((By.XPATH, "//a[@data-link-action='display-register-form']"))
        )
        driver.execute_script("window.scrollBy(0, 600);")
        driver.find_element(By.XPATH, "//a[@data-link-action='display-register-form']").click()
        driver.execute_script("window.scrollBy(0, 600);")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'register-form'))
        )

        driver.find_element(By.XPATH, "//input[@name='id_gender' and @value='1']").click()
        driver.find_element(By.NAME, 'firstname').send_keys("Robert")
        driver.find_element(By.NAME, 'lastname').send_keys("Kowalski")
        driver.find_element(By.NAME, 'email').send_keys("robert.kowalski@example.com")
        driver.find_element(By.NAME, 'password').send_keys("Password123")
        driver.find_element(By.NAME, 'birthday').send_keys("1999-01-02")
        consent_checkbox = driver.find_element(By.NAME, 'customer_privacy')
        if not consent_checkbox.is_selected():
            consent_checkbox.click()
        consent_checkbox2 = driver.find_element(By.NAME, 'psgdpr')
        driver.execute_script("window.scrollBy(0, 400);")
        if not consent_checkbox2.is_selected():
            consent_checkbox2.click()

        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        if driver.current_url == source + "/":
            result = "passed"
        else:
            print("Test D - user already exists")
            result = "failed"
            return result

        result = "passed"

    except TimeoutException:
        result = "failed"
        print("Test D timed out")

    except Exception as e:
        result = "failed"
        print("Test D failed")

    print("Test D sie zakonczyl")
    return result


def testIJ(driver, source):
    print("Test I sie rozpoczyna")
    results = ["failed", "failed"]

    try:
        driver.get(source)

        WebDriverWait(driver=driver, timeout=25).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='account']"))
        )

        account_element = driver.find_element(By.XPATH, "//a[@class='account']")
        ActionChains(driver).move_to_element(account_element).perform()

        WebDriverWait(driver=driver, timeout=25).until(
            EC.element_to_be_clickable(account_element)
        )
        account_element.click()

        # order history
        driver.execute_script("window.scrollBy(0, 300);")
        WebDriverWait(driver=driver, timeout=25).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='history-link']"))
        )
        driver.find_element(By.ID, 'history-link').click()

        # order details
        WebDriverWait(driver=driver, timeout=25).until(
            EC.presence_of_element_located((By.XPATH, "//tbody"))
        )
        driver.execute_script("window.scrollBy(0, 600);")
        order = driver.find_element(By.XPATH, "//tbody/tr[1]")
        order.find_element(By.XPATH, ".//a[contains(@data-link-action, 'view-order-details')]").click()

        # confirm that order details are displayed -> I passed
        WebDriverWait(driver=driver, timeout=25).until(
            EC.presence_of_element_located((By.ID, 'invoice-address'))
        )
        driver.execute_script("window.scrollBy(0, 600);")

        results = ["passed", "failed"]

        driver.find_element(By.XPATH, "//a[contains(text(), 'Pobierz fakturę proforma w pliku PDF')]").click()

        results = ["passed", "passed"]

    except TimeoutException:
        print("Test I failed - timed out")

    except Exception as e:
        print("Test I failed")

    print("Test I sie zakonczyl")
    return results


if __name__ == '__main__':
    options = Options()

    # commenting the line below show the browser window
    # options.add_argument("--headless")

    #options.add_argument("--width=1620")
    #options.add_argument("-height=780")

    options.add_argument("--window-size=1420,780")

    driver = webdriver.Chrome(options=options)

    baseAddress = "https://localhost:19171"
    koszykAddress = "https://localhost:19171/koszyk?action=show"

    driver.get(baseAddress)
    driver.set_page_load_timeout(30)

    test_results = []

    time_before = time.perf_counter()

    test_results.append(["A", testA(driver, baseAddress)])
    test_results.append(["B", testB(driver, baseAddress)])
    test_results.append(["C", testC(driver, koszykAddress)])
    test_results.append(["D", testD(driver, baseAddress)])
    results_efgh = testEFGH(driver, koszykAddress)
    test_results.append(["E", results_efgh[0]])
    test_results.append(["F", results_efgh[1]])
    test_results.append(["G", results_efgh[2]])
    test_results.append(["H", results_efgh[3]])
    results_ij = testIJ(driver, baseAddress)
    test_results.append(["I", results_ij[0]])
    test_results.append(["J", results_ij[1]])


    time_after = time.perf_counter()
    time_of_testing = time_after - time_before

    for test_result in test_results:
        print("Test " + test_result[0] + " ma rezultat " + test_result[1])
    print("Czas wykonania: " + str(time_of_testing))

    driver.quit()