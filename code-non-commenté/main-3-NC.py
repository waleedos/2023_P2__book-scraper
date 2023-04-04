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
        'universal_product_code': universal_product_code,
        'title': title,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category,
        'review_rating': review_rating,
        'image_url': urljoin(link,image_url)
    }


def get_categories(url):
    data = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    category_scrape = soup.find('div', class_='side_categories').find('li').find_all('li')
    for category in category_scrape:
        books_url = category.find('a', href = True).get('href')
        category_name = category.text.strip()
        data[category_name] = urljoin(url,books_url)
    return data


def get_books_data(url):
    links = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    for books in soup.find_all('article', class_='product_pod'):
        books_link_url = books.find('a', href = True)
        books_url = books_link_url.get('href')
        links.append(urljoin(url,books_url))
    next = soup.find('li', class_='next')
    if next is not None:
        next_page = url.split('/')[0 : -1]
        next_page.append(next.find('a').get('href'))
        next_page_url = '/'.join(next_page)
        links.extend(get_books_data(next_page_url))
    return links


def save_img(url, category_name, path):
    res = requests.get(url)
    os.makedirs('images', exist_ok=True)
    os.makedirs('images/'+ category_name, exist_ok=True)
    with open ('images/'+  category_name + '/' + path + '.jpg', 'wb') as img_file:
        img_file.write(res.content)


for category_name,category_url in get_categories('https://books.toscrape.com/').items():
    os.makedirs('data_csv', exist_ok=True)
    with open('data_csv/' + category_name + '.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["universal_product_code","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"])
        for url in get_books_data(category_url):
            book = get_book(url)
            writer.writerow([book['universal_product_code'],book['title'],book['price_including_tax'],book['price_excluding_tax'],book['number_available'],book['product_description'],book['category'],book['review_rating'],book['image_url']])
            save_img(url = book['image_url'], category_name = book['category'], path = book['universal_product_code'])

