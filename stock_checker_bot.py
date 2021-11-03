import json
import sys
from concurrent.futures import ThreadPoolExecutor

from script_resources import web_driver_builder
from script_resources.parse_generic_page import poll_out_of_stock_web_page_for_stock


def main():
    # Grab the json from the selected json file
    json_file_to_use = select_json_file_from_page_jsons()
    page_list = open(json_file_to_use)
    pages_to_query = json.load(page_list)
    page_list.close()

    # There's probably a cleaner way to do this when creating the executor map, but I'm lazy - the TPE below only takes
    # lists, so we have to create a list of drivers to use
    web_drivers = []
    for _ in pages_to_query:
        web_drivers.append(web_driver_builder.get_primary_driver())

    with ThreadPoolExecutor() as executor:
        executor.map(poll_out_of_stock_web_page_for_stock, web_drivers, pages_to_query)


def select_json_file_from_page_jsons():
    # Allow users to select from a json by passing in the name of the json file they'd like to use
    # instead of the default.json file (which we use if there is no argument provided)
    if len(sys.argv) > 1:
        return 'page_jsons/' + sys.argv[1]
    else:
        return 'page_jsons/default.json'


if __name__ == "__main__":
    main()


# TODO List:
# TODO Add ability to poll for an IN-STOCK element instead of just out-of-stock
# TODO This can't be completely closed out if you run it from the command line - figure that out and fix it
# TODO Make non-required properties (product/vendor name, etc) optional
# TODO maybe need a price inspector too, for something like Walmart/Amazon where they list in-stock items
#  but they're from scalpers and the prices are egregious:
# https://www.walmart.com/search?q=xbox+series+x&affinityOverride=default
# TODO for sites like Costco, going to need to be able to log in to use the page:
# https://www.costco.com/xbox-series-x-1tb-console-bundle.product.100757146.html
# TODO Improve polling methods so that they can run some queries involving js in headless mode
