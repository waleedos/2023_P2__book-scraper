import os
import requests
from bs4 import BeautifulSoup
import re	


"""La fonction "parse_links_products_pages" commence par envoyer une requête HTTP à l'URL 
spécifiée en utilisant la méthode "get" de l'objet "requests" et en stockant la réponse dans 
la variable "page". Cette réponse est ensuite passée en argument à la méthode "BeautifulSoup" 
pour créer un objet "soup_product_page" qui contient la structure HTML de la page."""
# Parse URLs links of product pages for the category "Romance"
def parse_links_products_pages():
    url = "https://books.toscrape.com/catalogue/category/books/romance_8/page-1.html"
    page = requests.get(url)
    soup_product_page = BeautifulSoup(page.content, "html.parser")
    
    """La méthode "find_all" de l'objet "soup_product_page" est utilisée pour récupérer tous 
    les éléments "h3" de la page HTML. Ces éléments représentent le titre des produits de 
    la page et contiennent un lien vers la page du produit.
    La variable "main_div" contient donc une liste de tous les éléments "h3" de la page HTML."""
    main_div = soup_product_page.find_all("h3")

    """La boucle "for" parcourt chaque élément de la liste "main_div" et utilise la méthode "a" 
    pour récupérer l'élément "a" du titre du produit. La méthode "a" retourne un objet qui représente 
    le lien vers la page du produit."""
    list_links_products_pages = []
    for item in main_div:

        """Le lien du produit est ensuite construit en concaténant la chaîne de caractères 
        "https://books.toscrape.com/catalogue/" avec l'élément de l'attribut "href" du lien, 
        en omettant les neuf premiers caractères de la chaîne (car ils représentent le chemin de base 
        du site web)."""
        link_product_page = "https://books.toscrape.com/catalogue/" + item.a["href"][9:]


        """Le lien du produit est ajouté à la liste "list_links_products_pages", qui contiendra 
        tous les liens vers les pages des produits."""
        list_links_products_pages.append(link_product_page)

    """Enfin, la liste des liens de produits est renvoyée à l'appelant de la fonction."""        
    return list_links_products_pages



"""Déclaration de variable "url_base" qui contient l'URL de base pour le site "http://books.toscrape.com/"."""
url_base = "https://books.toscrape.com/catalogue/category/books/romance_8/page-1.html"



"""La variable "page" utilise le module requests pour envoyer une requête GET au site "http://books.toscrape.com/" 
et stocke la réponse dans la variable "page"."""
page = requests.get(url_base)


"""La variable "soup" utilise le module BeautifulSoup pour parser le contenu HTML de la page et stocke le résultat 
dans une variable soup."""
soup = BeautifulSoup(page.content, "html.parser")

