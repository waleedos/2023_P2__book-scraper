import os
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

#--------------------------------------------#
# Création de la Fonction "get_book" qui prend le lien (URL) comme argument et renvoie un dictionnaire contenant les
# informations d'un livre à partir de ce lien.

# Déclaration de la fonction et prend un paramètre "link" comme entrée.
def get_book(link):

    # Appel de la bibliothèque "requests" pour envoyer une requête HTTP à l'URL spécifiée et récupérer le contenu
    # de la page.
    page = requests.get(link)

    # Appel de la bibliothèque "BeautifulSoup" pour analyser le contenu HTML de la page récupérée dans la ligne
    # précédente et stocker l'objet résultant dans la variable "soup".
    soup = BeautifulSoup(page.content,'html.parser')

    # Utilisation de la méthode "find" de BeautifulSoup pour trouver l'élément HTML contenant le texte 'UPC' dans
    # une balise <th> et accède à l'élément suivant de la même ligne (c'est-à-dire la balise <td>) pour extraire le
    # texte de l'UPC.
    universal_product_code= soup.find('th', string='UPC').find_next_sibling('td').text

    # Utilisation de la méthode "find" de BeautifulSoup pour trouver la balise <h1> contenant le titre du livre et
    # extraire son texte.
    title= soup.find('h1').text

    # Utilisation de la méthode "find" de BeautifulSoup pour trouver l'élément HTML contenant le texte 'Price
    # (incl. tax)' dans une balise <th> et accède à l'élément suivant de la même ligne pour extraire le texte du
    # prix incluant la taxe.
    price_including_tax= soup.find('th', string='Price (incl. tax)').find_next_sibling('td').text

    # Utilisation de la méthode "find" de BeautifulSoup pour trouver l'élément HTML contenant le texte 'Price
    # (excl. tax)' dans une balise <th> et accède à l'élément suivant de la même ligne pour extraire le texte du
    # prix hors taxe.
    price_excluding_tax= soup.find('th', string='Price (excl. tax)').find_next_sibling('td').text

    # Utilisation de la méthode "find" de BeautifulSoup pour trouver l'élément HTML contenant le texte 'Availability'
    # dans une balise <th> et accède à l'élément suivant de la même ligne pour extraire le texte de la disponibilité
    # du livre. La méthode "strip" est utilisée pour supprimer le texte inutile dans la chaîne extraite.
    number_available= soup.find('th', string='Availability').find_next_sibling('td').text.strip('In stock () available')

    # Utilisation de la méthode "find" de BeautifulSoup pour trouver la balise <p> contenant la description du livre.
    # La méthode "find_next" est utilisée pour trouver la première balise <p> suivant la balise contenant la classe
    # 'sub-header', qui est utilisée pour identifier la section de la description du livre.
    product_description= soup.find(class_='sub-header').find_next('p').text

    # Utilisation de la méthode "find" de BeautifulSoup pour trouver la balise contenant la catégorie du livre en
    # accédant à la troisième balise <a> dans l'élément HTML contenant la classe 'breadcrumb', et ce pour récuperer
    # la catégorie du livre
    category= soup.find(class_='breadcrumb').find_all('a')[2].text

    # Utilisation de la méthode "find" de BeautifulSoup pour trouver l'élément HTML contenant la classe 'star-rating'
    # et récupérer la classe CSS correspondant à la note de l'examen.
    review_rating= soup.find('p', class_='star-rating').get('class')[1]

    # Utilisation de la méthode "find" de BeautifulSoup pour trouver la balise <div> contenant l'image du livre et
    # accède à l'élément <img> suivant pour extraire l'URL de l'image.
    image_url= soup.find('div', class_='item active').find_next('img').get('src')

    # La fonction retourne un dictionnaire contenant toutes les informations extraites du livre, y compris l'URL de
    # l'image jointe à l'URL d'origine.
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

# Définit le lien de la catégorie à scrapper
category_url = 'https://books.toscrape.com/catalogue/category/books/childrens_11/index.html'
# Récupère le nom de la catégorie à partir du lien
category_name = category_url.split('/')[-2]

os.makedirs('data_csv', exist_ok=True)
with open('data_csv/' + category_name + '.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["universal_product_code","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"])
    for url in get_books_data(category_url):
        book = get_book(url)
        writer.writerow([book['universal_product_code'],book['title'],book['price_including_tax'],book['price_excluding_tax'],book['number_available'],book['product_description'],book['category'],book['review_rating'],book['image_url']])
        save_img(url = book['image_url'], category_name = book['category'], path = book['universal_product_code'])
