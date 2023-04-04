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

# Définit une fonction nommée "save_img" qui prend trois arguments: "url", "category_name" et "path".
def save_img(url, category_name, path):

    # La fonction "save_img" utilise la bibliothèque "requests" pour effectuer une demande "get" sur l'URL fournie en tant 
    # qu'argument "url". La réponse est stockée dans la variable "res".
    res = requests.get(url)

    # Utilisation de la bibliothèque "os" pour créer deux répertoires. Si les répertoires existent déjà, cela ne crée pas de 
    # nouveaux répertoires. Les répertoires créés sont "images" et "images/nom_de_la_catégorie".
    os.makedirs('images', exist_ok=True)
    os.makedirs('images/'+ category_name, exist_ok=True)

    # Utilisation d'une instruction "with open" pour ouvrir un fichier dans le répertoire "images/nom_de_la_catégorie" et 
    # avec un nom de fichier basé sur l'argument "path". Le fichier est ouvert en mode binaire d'écriture "wb". 
    # Le contenu de la réponse "res" est écrit dans ce fichier en utilisant la méthode "write".
    with open ('images/'+  category_name + '/' + path + '.jpg', 'wb') as img_file:
        img_file.write(res.content)

# Déclaration du lien de la page du livre souhaité
link = 'https://books.toscrape.com/catalogue/twenty-yawns_773/index.html'

book = get_book(link)

# utilise la bibliothèque "csv" pour créer un nouveau fichier CSV nommé "book.csv" dans le répertoire "data_csv". Si le 
# répertoire existe déjà, cela ne crée pas de nouveaux répertoires.
os.makedirs('data_csv', exist_ok=True)

# Ecriture d'une ligne d'en-tête pour le fichier CSV contenant les noms des colonnes
with open('data_csv/book.csv', 'w', encoding='utf-8') as csvfile:

    # Ecriture d'une ligne de données dans le fichier CSV en utilisant la méthode "writerow" du module CSV. Les données écrites sont 
    # tirées de la variable "book", qui est obtenue en appelant une fonction nommée "get_book" sur un lien donné.
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["universal_product_code","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"])
    writer.writerow([book['universal_product_code'],book['title'],book['price_including_tax'],book['price_excluding_tax'],book['number_available'],book['product_description'],book['category'],book['review_rating'],book['image_url']])
    
    # Appelle la fonction "save_img" en utilisant les valeurs de "url", "category_name" et "path" qui sont stockées dans "book". 
    # Cette fonction enregistre une image en utilisant l'URL fournie et en la plaçant dans un répertoire basé sur la catégorie 
    # et le chemin.
    save_img(url = book['image_url'], category_name = book['category'], path = book['universal_product_code'])

print("Téléchargement terminé avec succès !")    