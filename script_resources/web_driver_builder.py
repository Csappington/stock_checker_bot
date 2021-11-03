from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_primary_driver():
    # Set up our primary Selenium driver
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("detach", True)

    # Some websites want to use geolocation, but since we're using an incognito so we can bot without getting a cookie
    # or ip ban, we need to set the geolocation permissions manually.  This can be disabled if you don't need it.
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 2})

    # Note: some websites, like Best Buy, don't seem to be able to open in headless mode.
    # chrome_options.add_argument("--headless")

    primary_driver = webdriver.Chrome(options=chrome_options)
    # How long we'll wait for a web element to become available before timing out.
    primary_driver.implicitly_wait(10)
    return primary_driver
