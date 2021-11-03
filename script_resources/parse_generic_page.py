from datetime import datetime
from time import sleep
# from tkinter import messagebox

import winsound
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def poll_out_of_stock_web_page_for_stock(primary_driver, web_page):
    page_url = web_page["page_url"]
    out_of_stock_xpath = web_page["out_of_stock_xpath"]
    out_of_stock_text = get_raw_string(web_page["out_of_stock_text"])
    product_name = web_page["product_name"]
    vendor_name = web_page["vendor_name"]
    prerequisites_to_click = web_page["prerequisite_xpaths"]

    reload_page = 'true'

    # Normally we don't know exactly what state the element will be in when the product stock is available,
    # only what state it will be in when it is OUT of stock.  So we'll query the element until its state changes.
    while reload_page == 'true':

        # Refresh the page and click on any prerequisite elements that need to be dismissed/closed
        primary_driver.get(page_url)

        if (prerequisites_to_click is not None) & (len(prerequisites_to_click)) > 0:
            click_prerequisites(primary_driver, prerequisites_to_click)

        # Query by xpath the text of the element that will have the out of stock message we need
        try:
            out_of_stock_element_to_inspect = primary_driver.find_element_by_xpath(out_of_stock_xpath)
            actual_out_of_stock_element_text = get_raw_string(out_of_stock_element_to_inspect.get_attribute("textContent"))
        except Exception :
            # Sometimes a website doesn't use the same element to display in-stock and out of stock messages,
            # so if the out of stock element is no longer available, we'll treat that as an in-stock alert
            actual_out_of_stock_element_text = "ELEMENT MISSING"

        # If the element is in stock, play some notification sounds and close the original driver
        if actual_out_of_stock_element_text != out_of_stock_text:
            print("Page shows " + actual_out_of_stock_element_text + ", expected " + out_of_stock_text)
            winsound.Beep(1000, 440)
            winsound.Beep(1000, 440)

            # Enable if you want a popup telling you where the product is available.  This prevented navigating to the
            # final window until the message was clicked off, so I'm disabling it for now.
            # messagebox.showerror(product_name + ' available at ' + vendor_name)

            primary_driver.close()
            break

        print(str(datetime.now()) + ' No available ' + product_name + ' found at ' + vendor_name + '.  Restarting.')
        sleep(1)
    proceed_to_site(page_url)


def proceed_to_site(page_url):
    # If the product is in stock, spin up a second Chrome window that is not headless,
    # and navigate to the product page for purchase.
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    secondary_driver = webdriver.Chrome(options=chrome_options)
    secondary_driver.set_window_position(0, 0)
    secondary_driver.set_window_size(1920, 1440)
    secondary_driver.get(page_url)
    winsound.Beep(1000, 440)
    winsound.Beep(1000, 440)


def get_raw_string(string_to_convert):
    return string_to_convert.strip(' \t\n\r')\
        .lower()


def click_prerequisites(primary_driver, prerequisites):
    # Some websites have popups or other elements that need to be cleared before we can begin to poll the in or out of
    # stock elements for status.  This will identify and close any elements that are passed in if they exist.
    for prerequisite in prerequisites:
        try:
            button_xpath = primary_driver.get(prerequisite)
            primary_driver.clickButton(button_xpath)
        except Exception:
            continue