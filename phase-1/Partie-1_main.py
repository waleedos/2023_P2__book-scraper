import os
import requests
from bs4 import BeautifulSoup
import csv
import re

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#       LA FONCTION : parse_links_products_pages():       #
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# La fonction "parse_links_products_pages" commence par envoyer une requête HTTP à l'URL
# spécifiée en utilisant la méthode "get" de l'objet "requests" et en stockant la réponse dans 
# la variable "page". Cette réponse est ensuite passée en argument à la méthode "BeautifulSoup" 
# pour créer un objet "soup_product_page" qui contient la structure HTML de la page."""
# Parse URLs links of product pages for the category "Romance"
def parse_links_products_pages():
    url = "https://books.toscrape.com/catalogue/category/books/childrens_11/page-1.html"
    page = requests.get(url)
    soup_product_page = BeautifulSoup(page.content, "html.parser")

    # La méthode "find_all" de l'objet "soup_product_page" est utilisée pour récupérer tous 
    # les éléments "h3" de la page HTML. Ces éléments représentent le titre des produits de 
    # la page et contiennent un lien vers la page du produit.
    # La variable "main_div" contient donc une liste de tous les éléments "h3" de la page HTML."""
    main_div = soup_product_page.find_all("h3")

    # La boucle "for" parcourt chaque élément de la liste "main_div" et utilise la méthode "a" 
    # pour récupérer l'élément "a" du titre du produit. La méthode "a" retourne un objet qui représente 
    # le lien vers la page du produit."""
    list_links_products_pages = []
    for item in main_div:
        # Le lien du produit est ensuite construit en concaténant la chaîne de caractères
        # "https://books.toscrape.com/catalogue/" avec l'élément de l'attribut "href" du lien, 
        # en omettant les neuf premiers caractères de la chaîne (car ils représentent le chemin de base 
        # du site web)."""
        link_product_page = "https://books.toscrape.com/catalogue/" + item.a["href"][9:]

        # Le lien du produit est ajouté à la liste "list_links_products_pages", qui contiendra 
        # tous les liens vers les pages des produits."""
        list_links_products_pages.append(link_product_page)

    # Enfin, la liste des liens de produits est renvoyée à l'appelant de la fonction."""        
    return list_links_products_pages


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#     LA FONCTION : parse_product_page(url_product):     #
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# La fonction nommée "parse_product_page" qui prend en entrée une URL de produit (variable "url_product") et qui retourne
# trois variables en sortie : "product_page_info", "image_url_text" et "universal_product_code".

# La fonction commence par faire une requête à l'URL donnée en utilisant la bibliothèque "requests" et stocke la réponse 
# dans la variable "page_response". Elle utilise ensuite la bibliothèque "BeautifulSoup" pour analyser le contenu HTML de 
# la page en question, et stocke le résultat dans la variable "soup_page".
def parse_product_page(url_product):
    page_response = requests.get(url_product)
    soup_page = BeautifulSoup(page_response.content, 'html.parser')

    # Définition d’une variable "product_page_url" en lui donnant la valeur de "url_product".
    product_page_url = url_product
    
    # Trouver l'élément HTML contenant le code produit universel (UPC) et stocke sa valeur dans la variable "universal_product_code".
    universal_product_code = soup_page.find(string="UPC").next_element.string

    # Trouver l'élément HTML contenant le titre du produit et stocke sa valeur dans la variable "title".
    title = soup_page.h1.string

    # Pour trouver les éléments HTML contenant le prix du produit incluant et excluant la taxe, et stockent leur valeur 
    # respective dans les variables "price_including_tax" et "price_excluding_tax".
    price_including_tax = soup_page.find(string="Price (incl. tax)").next_element.string
    price_excluding_tax = soup_page.find(string="Price (excl. tax)").next_element.string

    # La ligne suivante utilise la méthode find() de BeautifulSoup pour trouver l'élément HTML contenant 
    # le texte "instock availability", puis la méthode get_text() pour extraire le texte brut de l'élément. 
    # Ce texte est ensuite nettoyé en utilisant la méthode strip() et stocké dans la variable "number_available_text". 
    # La ligne suivante utilise une expression régulière pour extraire le nombre d'articles disponibles à partir 
    # de ce texte et stocke le résultat dans la variable "number_available".
    number_available_text = soup_page.find("p", class_="instock availability").get_text().strip()
    number_available = re.search(" \((.*) available", number_available_text)
    number_available = number_available.group(1)

    # Pour trouver  l'élément HTML contenant la description du produit, s'il existe, et stockent sa valeur 
    # dans la variable "product_description". Elles trouvent également l'élément HTML contenant la catégorie du produit 
    # en utilisant la méthode find_all() de BeautifulSoup, puis stockent la valeur de la troisième balise <a> dans la
    # variable "category".
    product_description_div = soup_page.find(id="product_description")
    product_description = ""
    if product_description_div:
        product_description = product_description_div.find_next("p").string

    breadcrumb = soup_page.find('ul', class_='breadcrumb')
    list_breadcrumb = breadcrumb.find_all("a")
    category = list_breadcrumb[2].string

    # Pour trouver l’element HTML contenant la note de l'examen (review_rating) du produit et stocke sa valeur dans la
    # variable "review_rating".
    review_rating = soup_page.find("p", class_="star-rating")["class"][1]

    # La ligne suivante trouve l'élément HTML contenant l'URL de l'image du produit et stocke sa valeur dans la variable
    # "image_url". La ligne suivante construit l'URL complète de l'image en utilisant la concaténation de chaînes de
    # caractères, en ajoutant le nom de domaine "https://books.toscrape.com" et en enlevant les cinq premiers caractères
    # de la valeur de "src" dans "image_url".
    image_url = soup_page.find("div", class_="carousel-inner").find_next("img")
    image_url_text = "https://books.toscrape.com" + image_url["src"][5:]

    product_page_info = [
        product_page_url,
        universal_product_code,
        title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        product_description,
        category,
        review_rating,
        image_url_text
    ]
    # Création d'une liste contenant toutes les informations extraites du produit, puis retourne cette liste, l'URL de
    # l'image et le code produit universel.
    return product_page_info, image_url_text, universal_product_code


# Déclaration de variable "url_base" qui contient l'URL de base pour le site "http://books.toscrape.com/".
url_base = "https://books.toscrape.com/catalogue/category/books/childrens_11/page-1.html"

# La variable "page" utilise le module requests pour envoyer une requête GET au site "http://books.toscrape.com/" 
# et stocke la réponse dans la variable "page".
page = requests.get(url_base)

# La variable "soup" utilise le module BeautifulSoup pour parser le contenu HTML de la page et stocke le résultat 
# dans une variable soup."""
soup = BeautifulSoup(page.content, "html.parser")

# La variable "categories_div" utilise la méthode "find "de l'objet "soup" pour rechercher un élément "div" ayant une
# classe "side_categories".
categories_div = soup.find("div", class_="side_categories")

# Utilisation de la méthode "find_all" de l'objet "categories_div" pour récupérer tous les liens "a" contenus dans la
# variable categories_div.
links_categories = categories_div.find_all("a")

# La variable "list_links_categories" est une liste vide qui est ensuite remplie en utilisant une boucle "for" pour
# parcourir chaque élément de "links_categories" à partir du deuxième élément, qui est ignoré. Dans chaque itération de
# la boucle, la variable "link" est mise à jour en concaténant l'URL de base avec l'attribut "href" de l'élément "a".
# Ensuite, le lien mis à jour est ajouté à la liste "list_links_categories".
list_links_categories = []
for link in links_categories[1:]:
    link = url_base + link["href"]
    list_links_categories.append(link)

# Parse categories links
list_links_products_pages = parse_links_products_pages()

# Create result directory
if not os.path.exists("result"):
    os.makedirs("result")

# Create CSV file
en_tete = [
    "product_page_url",
    "universal_product_code",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url_text",
]

category_name = "Romance"
with open("result/data_" + category_name + ".csv", "w", newline="", encoding="utf-8") as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=",")
    writer.writerow(en_tete)
    for link_product in list_links_products_pages:
        # Function parse product information in product page
        product_info = parse_product_page(link_product)
        writer.writerow(product_info[0])

print("Téléchargement terminé avec succès !")
