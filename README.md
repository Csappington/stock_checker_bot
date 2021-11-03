# Stock checker bot
A small web scraper bot for facilitating purchasing, made using a mixture of Python and Selenium for web interactions.

Will continuously poll a group of websites looking at the value for a specific element (e.g. a button reading "Out of stock") until the text on the element changes or the element is no longer available, at which point it will stop refreshing, beep twice, and open the site again in a standard web view, allowing for purchase.

## Prerequisites
* Python
* Selenium
* Google Chrome (currently we use Selenium's Chrome web driver for page interactions)

## Instructions for use:
 Define a json file in the page_json folder containing a list of web pages for the bot to poll for in-stock status of something.  Page format:
 * page_url (String) - page url to refresh and then poll for status
 * out_of_stock_xpath (String) - exact xpath to the out of stock element that we'll poll for status
 * out_of_stock_text (String) - text of the out of stock element that we'll poll for status, which should change when the thing we're polling for becomes available
 * product_name (String) - human-readable name of the thing we're polling for, for use in logging
 * vendor_name (String) - human-readable name of the site that's being polled, for use in logging
 * prerequisite_xpaths (List) - any prerequisite pop-up elements that need to be cleared before we can begin polling the site

 Note: The xpath of an element can be discovered by entering inspection mode on chrome, then right-clicking on the desired element in the inspector and selecting copy > copy full xpath)
 
 Note: When providing a prerequisite xpath, try to isolate the xpath of the popup's close/dismiss button, as anything provided in this list will be clicked on

 Json example:
 ```
 {
  "page_url": "https://www.gamestop.com/products/microsoft-xbox-series-x/224744.html",
  "out_of_stock_xpath": "/html/body/div[6]/div[5]/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[11]/div[2]/div/div[1]/button",
  "out_of_stock_text": "unavailable",
  "product_name": "Xbox",
  "vendor_name": "Gamestop",
  "prerequisite_xpaths": []
 }
```
 Once you have your json file, provide the file name to the purchase bot via a command line arg, e.g. 'python purchase_bot.py test.json' to provide the file for use.

 Note: If there is no custom json filename provided, the bot will default to using the default.json file.
