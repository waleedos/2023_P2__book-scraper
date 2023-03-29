import os
import requests
from bs4 import BeautifulSoup
import re	

# La fonction "parse_links_products_pages" commence par envoyer une requête HTTP à l'URL 
# spécifiée en utilisant la méthode "get" de l'objet "requests" et en stockant la réponse dans 
# la variable "page". Cette réponse est ensuite passée en argument à la méthode "BeautifulSoup" 
# pour créer un objet "soup_product_page" qui contient la structure HTML de la page."""
# Parse URLs links of product pages for the category "Romance"
def parse_links_products_pages():
    url = "https://books.toscrape.com/catalogue/category/books/romance_8/page-1.html"
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


# Déclaration de variable "url_base" qui contient l'URL de base pour le site "http://books.toscrape.com/".
url_base = "https://books.toscrape.com/catalogue/category/books/romance_8/page-1.html"

# La variable "page" utilise le module requests pour envoyer une requête GET au site "http://books.toscrape.com/" 
# et stocke la réponse dans la variable "page".
page = requests.get(url_base)

# La variable "soup" utilise le module BeautifulSoup pour parser le contenu HTML de la page et stocke le résultat 
# dans une variable soup."""
soup = BeautifulSoup(page.content, "html.parser")

# La variable "categories_div" utilise la méthode "find "de l'objet "soup" pour rechercher un élément "div" ayant une classe "side_categories".
categories_div = soup.find("div", class_="side_categories")

# Utilisation de la méthode "find_all" de l'objet "categories_div" pour récupérer tous les liens "a" contenus dans la variable categories_div.
links_categories = categories_div.find_all("a")

list_links_categories = []
for link in links_categories[1:]:
    link = url_base + link["href"]
    list_links_categories.append(link)

# La variable "list_links_categories" est une liste vide qui est ensuite remplie en utilisant une boucle "for" pour parcourir chaque élément 
# de "links_categories" à partir du deuxième élément, qui est ignoré. Dans chaque itération de la boucle, la variable "link" est mise à jour 
# en concaténant l'URL de base avec l'attribut "href" de l'élément "a". Ensuite, le lien mis à jour est ajouté à la liste "list_links_categories".
list_links_categories = []
for link in links_categories[1:]:
    link = url_base + link["href"]
    list_links_categories.append(link)

# Utilisation d’une boucle "for" qui parcourt chaque élément de la liste "list_links_categories". Pour chaque lien de catégorie, une requête "GET" 
# est envoyée avec le module "requests" pour récupérer le contenu "HTML" de la page. Le contenu "HTML" est ensuite analysé avec 
# le module "BeautifulSoup" et stocké dans la variable "soup_category". 
# Parse categories links
for link_category in list_links_categories:
    link_response = requests.get(link_category)
    soup_category = BeautifulSoup(link_response.content, "html.parser")

    # La variable "category_name" contient le nom de la catégorie, qui est extrait à partir de la balise "h1" du contenu HTML de la page.
    category_name = soup_category.h1.string

    # La variable "list_links_products_pages" contient la liste des liens de chaque page de produits pour cette catégorie. Cette variable 
    # est remplie en appelant une fonction personnalisée "parse_links_products_pages" qui prend comme argument le lien de la page de 
    # catégorie et renvoie la liste de liens pour chaque page de produits de cette catégorie.
    list_links_products_pages = parse_links_products_pages(link_category)

    # La variable list_next_pages est une liste vide qui sera utilisée pour stocker les liens des prochaines pages de produits. 
    list_next_pages = []

    # La variable "first_next_page" utilise la méthode "find" de l'objet "soup_category" pour trouver la première balise "a" ayant le texte "next". 
    first_next_page = soup_category.find("a", string="next")
