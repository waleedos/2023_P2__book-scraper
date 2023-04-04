import os
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin


def get_book(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content,'html.parser')
    universal_product_code= soup.find('th', string='UPC').find_next_sibling('td').text
    title= soup.find('h1').text
    price_including_tax= soup.find('th', string='Price (incl. tax)').find_next_sibling('td').text
    price_excluding_tax= soup.find('th', string='Price (excl. tax)').find_next_sibling('td').text
    number_available= soup.find('th', string='Availability').find_next_sibling('td').text.strip('In stock () available')
    product_description= soup.find(class_='sub-header').find_next('p').text
    category= soup.find(class_='breadcrumb').find_all('a')[2].text
    review_rating= soup.find('p', class_='star-rating').get('class')[1]
    image_url= soup.find('div', class_='item active').find_next('img').get('src')
    return {
        'universal_product_code' : universal_product_code,
        'title' : title,
        'price_including_tax' : price_including_tax,
        'price_excluding_tax' : price_excluding_tax,
        'number_available' : number_available,
        'product_description' : product_description,
        'category' : category,
        'review_rating' : review_rating,
        'image_url' : urljoin(link,image_url)
    }


def save_img(url, category_name, path):
    res = requests.get(url)
    os.makedirs('images', exist_ok=True)
    os.makedirs('images/'+ category_name, exist_ok=True)
    with open ('images/'+  category_name + '/' + path + '.jpg', 'wb') as img_file:
        img_file.write(res.content)
link = 'https://books.toscrape.com/catalogue/twenty-yawns_773/index.html'

book = get_book(link)

os.makedirs('data_csv', exist_ok=True)

with open('data_csv/book.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["universal_product_code","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"])
    writer.writerow([book['universal_product_code'],book['title'],book['price_including_tax'],book['price_excluding_tax'],book['number_available'],book['product_description'],book['category'],book['review_rating'],book['image_url']])
    save_img(url = book['image_url'], category_name = book['category'], path = book['universal_product_code'])