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

# Création d’une Fonction "get_books_data" qui récupère les liens des pages de tous les livres de la catégorie sélectionnée. 
# Elle prend en entrée l'URL de la page principale de la catégorie et renvoie une liste de liens vers les pages de chaque livre 
# de la catégorie.
# Définition de la fonction "get_books_data" qui prend l'URL de la page principale de la catégorie comme argument :
def get_books_data(url):

    # Initialisation d’une liste vide pour stocker les liens vers les pages des livres :
    links = []

    # Utilisation du module "requests" pour récupérer le contenu HTML de la page principale de la catégorie :
    r = requests.get(url)

    # Utilisation du mode "BeautifulSoup" pour analyser le contenu HTML et en extraire les éléments souhaités :
    soup = BeautifulSoup(r.content, 'html.parser')

    # Nous utilisons une boucle "for" pour parcourir tous les éléments HTML de type "article" qui ont la classe "product_pod" :
    for books in soup.find_all('article', class_='product_pod'):

        # Recherche de l'élément HTML "a" qui contient l'URL de la page du livre :
        books_link_url = books.find('a', href = True)

        # Extraire l'URL de la page du livre à partir de l'élément HTML "a" trouvé précédemment :
        books_url = books_link_url.get('href')

        # Nous utilisons maintenant la fonction "urljoin" du module "urllib.parse" pour combiner l'URL de la page principale de 
        # la catégorie avec l'URL de la page du livre pour former un lien complet :
        links.append(urljoin(url,books_url))

    # Nous trouvons l'élément HTML "li" qui a la classe "next" pour vérifier s'il y a une page suivante dans cette catégorie 
    # actuelle
    next = soup.find('li', class_='next')

    # Si nous trouvons "une page suivante" qui existe, les lignes suivantes extraient l'URL de la page suivante, l'ajoutent à 
    # la liste des liens et rappellent la fonction "get_books_data" pour extraire les liens de la page suivante :
    if next is not None:
        next_page = url.split('/')[0 : -1]
        next_page.append(next.find('a').get('href'))
        next_page_url = '/'.join(next_page)
        links.extend(get_books_data(next_page_url))

    # Enfin, la fonction "get_books_data" renvoie la liste complète des liens de toutes les pages de livres de la catégorie :
    return links


# Création de la Fonction  "save_img" qui prend trois arguments : url, category_name, et path. Elle a pour but de télécharger 
# une image à partir de l'URL fournie (url), et de la sauvegarder dans un dossier appelé "images", qui est organisé en 
# sous-dossiers pour chaque catégorie d'images (category_name). L'image téléchargée sera enregistrée avec un nom de fichier 
# spécifié par l'argument path.
# Définition de la Fonction appelée save_img qui prend trois paramètres : url, category_name, et path.
def save_img(url, category_name, path):

    # Nous utilisons la bibliothèque requests pour envoyer une requête HTTP à l'URL fournie (url) et stocker la réponse dans 
    # la variable res.
    res = requests.get(url)

    # Nous utilisons la bibliothèque os pour créer deux dossiers : un dossier appelé "images" à la racine du projet (si ce 
    # dossier n'existe pas déjà), et un sous-dossier appelé category_name dans le dossier "images" (si ce sous-dossier 
    # n'existe pas déjà). exist_ok=True permet de ne pas lever d'exception si les dossiers existent déjà.
    os.makedirs('images', exist_ok=True)
    os.makedirs('images/'+ category_name, exist_ok=True)

    # Nous utilisons la syntaxe with open() pour ouvrir un fichier en mode binaire ('wb') dans le sous-dossier category_name 
    # du dossier "images". Le nom de fichier est déterminé par l'argument path, avec l'extension .jpg.
    with open ('images/'+  category_name + '/' + path + '.jpg', 'wb') as img_file:

        # Et enfin Nous écrivons le contenu de la réponse HTTP (res.content) dans le fichier que nous avons ouvert à l'étape 
        # précédente.
        img_file.write(res.content)


# Définit le lien de la catégorie en créant une variable "category_url" qui contient l'URL de la page web de la catégorie des 
# livres à scraper
category_url = 'https://books.toscrape.com/catalogue/category/books/childrens_11/index.html'

# Récupère le nom de la catégorie à partir du lien en utilisant la méthode split() pour diviser l'URL en segments. Ensuite, 
# elle sélectionne l'avant-dernier segment, qui contient le nom de la catégorie, et le stocke dans une variable 
# appelée "category_name".
category_name = category_url.split('/')[-2]

# Utilisation de la fonction makedirs() du module os pour créer un dossier nommé "data_csv". L'argument exist_ok=True permet 
# de ne pas lever d'erreur si le dossier existe déjà.
os.makedirs('data_csv', exist_ok=True)

# Ouvre un fichier CSV dans le dossier "data_csv" avec le nom de la catégorie suivi de ".csv". L'argument 'w' indique que le fichier 
# sera ouvert en mode écriture. Le paramètre encoding='utf-8' indique que le fichier utilise l'encodage UTF-8.
with open('data_csv/' + category_name + '.csv', 'w', encoding='utf-8') as csvfile:

    # Création d’un objet "writer" à partir de la classe writer du module csv. L'objet "writer" permet d'écrire des lignes dans 
    # le fichier CSV. Le paramètre delimiter=',' indique que les données seront séparées par une virgule.
    writer = csv.writer(csvfile, delimiter=',')

    # Puis nous utilisons ici la méthode writerow() de l'objet "writer" pour écrire la première ligne du fichier CSV. Cette ligne 
    # contient les noms des colonnes du fichier.
    writer.writerow(["universal_product_code","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"])

    # Nous utilisons une boucle for pour parcourir tous les liens de livres de la catégorie. La fonction "get_books_data" est 
    # appelée pour récupérer les liens de tous les livres de la catégorie.
    for url in get_books_data(category_url):

        # Utilisation de la fonction "get_book" pour récupérer toutes les informations sur un livre donné.
        book = get_book(url)

        # Nous ecrivons avec la méthode writerow() de l'objet "writer" les informations sur le livre dans le fichier CSV.
        writer.writerow([book['universal_product_code'],book['title'],book['price_including_tax'],book['price_excluding_tax'],book['number_available'],book['product_description'],book['category'],book['review_rating'],book['image_url']])

        # Appelle de la fonction "save_img" en lui passant trois arguments : "url", "category_name", et "path" pour télécharger 
        # l'image à partir de l'URL et la sauvegarder dans un dossier spécifique. Le nom de fichier est généré en combinant le nom 
        # de la catégorie et le code produit universel (UPC) du livre, qui sont fournis en arguments.
        save_img(url = book['image_url'], category_name = book['category'], path = book['universal_product_code'])
