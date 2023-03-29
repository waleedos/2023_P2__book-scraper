import os
import requests
from bs4 import BeautifulSoup
import re	

# Parse URLs links of product pages for the category "Romance"
def parse_links_products_pages():
    url = "https://books.toscrape.com/catalogue/category/books/romance_8/page-1.html"
    page = requests.get(url)
    soup_product_page = BeautifulSoup(page.content, "html.parser")
    main_div = soup_product_page.find_all("h3")

    list_links_products_pages = []
    for item in main_div:
        link_product_page = "https://books.toscrape.com/catalogue/" + item.a["href"][9:]
        list_links_products_pages.append(link_product_page)
    return list_links_products_pages