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

#--------------------------------------------#
# Création de  la Fonction et prend un paramètre "url" comme entrée.
def get_categories(url):

    # Création d’un dictionnaire vide nommé "data" pour stocker les informations sur les différentes catégories
    # de livres.
    data = {}

    # Appel de "requests" pour envoyer une requête HTTP à l'URL spécifiée et récupérer le contenu de la page.
    response = requests.get(url)

    # Appel de "BeautifulSoup" pour analyser le contenu HTML de la page récupérée dans la ligne précédente et stocker
    # l'objet résultant dans la variable "soup".
    soup = BeautifulSoup(response.content, 'html.parser')

    # La méthode "find" de BeautifulSoup pour trouver l'élément HTML contenant la classe 'side_categories' qui
    # contient les liens vers les différentes catégories de livres. La méthode "find_all" est ensuite utilisée
    # pour extraire une liste de tous les éléments HTML de la balise <li> qui sont des sous-catégories de la
    # première catégorie.
    category_scrape = soup.find('div', class_='side_categories').find('li').find_all('li')

    # Une boucle "for" parcourt chaque sous-catégorie dans la liste extraite à la ligne précédente.
    for category in category_scrape:

        # La méthode "find" de BeautifulSoup pour trouver le lien vers la page des livres correspondant à
        # la sous-catégorie courante, puis la méthode "get" est utilisée pour extraire l'URL à partir du lien
        # et stocker cette information dans la variable "books_url".
        books_url = category.find('a', href = True).get('href')

        # La huitième ligne utilise la méthode "strip" pour supprimer les espaces blancs en début et fin de
        # la chaîne de texte représentant le nom de la catégorie courante et stocker cette information dans la
        # variable "category_name".
        category_name = category.text.strip()

        # Ajout d’une entrée au dictionnaire "data", où la clé est le nom de la catégorie et la valeur est l'URL
        # de la page des livres correspondant à cette catégorie. La méthode "urljoin" est utilisée pour joindre
        # l'URL de base à l'URL relative extraite de la page Web.
        data[category_name] = urljoin(url,books_url)

    # La dernière ligne renvoie le dictionnaire "data" contenant les informations sur toutes les catégories de
    # livres disponibles sur la page Web.
    return data

#--------------------------------------------#
# Création la Fonction "get_books_data" prenant un paramètre "url" comme entrée.
def get_books_data(url):

    # Initialisation d’une liste vide appelée "links" pour stocker les URL de pages de détails de livres.
    links = []

    # Appel de "requests" pour envoyer une requête HTTP à l'URL spécifiée et récupérer le contenu de la page.
    r = requests.get(url)

    # Appel à "BeautifulSoup" pour analyser le contenu HTML de la page récupérée dans la ligne précédente et stocker
    # l'objet résultant dans la variable "soup".
    soup = BeautifulSoup(r.content, 'html.parser')

    # La boucle "for" sur la cinquième ligne parcourt tous les éléments HTML contenant la classe 'product_pod',
    # qui sont les conteneurs pour chaque livre sur la page de liste des livres.
    for books in soup.find_all('article', class_='product_pod'):

        # La méthode "find" de BeautifulSoup pour trouver le lien vers la page de détails du livre correspondant
        # au livre en cours, puis la méthode "get" est utilisée pour extraire l'URL à partir du lien et stocker
        # cette information dans la variable "books_url".
        books_link_url = books.find('a', href = True)
        books_url = books_link_url.get('href')

        # Utilisation de la méthode "urljoin" pour joindre l'URL de base à l'URL relative extraite de la page Web,
        # puis ajoute cette URL à la liste "links".
        links.append(urljoin(url,books_url))

    # Appel a la méthode "find" de BeautifulSoup pour trouver l'élément HTML correspondant au lien "Next" qui
    # pointe vers la page suivante des livres (s'il existe), et stocke cet élément dans la variable "next".
    # Si l'élément "Next" est présent (c'est-à-dire qu'il existe une page suivante),
    next = soup.find('li', class_='next')
    if next is not None:

        # On extrait l'URL de la page suivante à partir de l'URL actuelle, en remplaçant la dernière partie de l'URL
        # par l'URL extraite de l'élément "Next".
        next_page = url.split('/')[0 : -1]
        next_page.append(next.find('a').get('href'))
        next_page_url = '/'.join(next_page)

        # Puis la méthode "extend" pour ajouter les URL de pages de détails de livres trouvées sur la page suivante
        # en appelant récursivement la fonction "get_books_data" avec la nouvelle URL.
        links.extend(get_books_data(next_page_url))

    # Renvoie de la liste "links" contenant les URL de toutes les pages de détails de livres trouvées sur la page de
    # liste des livres initiale.
    return links

#--------------------------------------------#
# Création d’un Fonction "save_img" qui télécharge une image à partir d'une URL donnée, la stocke dans un répertoire
# "images" avec un sous-répertoire pour la catégorie spécifiée, et enregistre l'image sous le nom spécifié dans
# le format ".jpg".
# Cette Fonction prend trois arguments : url, category_name, et path.
# La variable url est un lien URL vers une image que nous voulons télécharger et enregistrer.
# La variable category_name est une chaîne de caractères qui indique la catégorie à laquelle appartient l'image.
# La variable path est également une chaîne de caractères qui indique le nom de l'image.
def save_img(url, category_name, path, title):

    # Une requête HTTP pour télécharger le contenu de l'URL à l'aide de la bibliothèque requests. La réponse est
    # stockée dans la variable res.
    res = requests.get(url)


    # Création de  deux répertoires: un répertoire nommé "images" pour stocker toutes les images téléchargées et
    # un répertoire pour stocker les images de la catégorie donnée par category_name.
    os.makedirs('images', exist_ok=True)
    os.makedirs('images/'+ category_name, exist_ok=True)
    
    # création d'un chemin de fichier pour l'image en utilisant les noms de catégorie et de titre de livre, 
    # ainsi que l'extension ".jpg".  
    img_path = os.path.join('images', category_name, title + '.jpg')
    
    # création récursive des répertoires nécessaires pour stocker le fichier image à l'emplacement donné par img_path. 
    # La fonction os.makedirs() crée tous les répertoires intermédiaires nécessaires.
    os.makedirs(os.path.dirname(img_path), exist_ok=True)    

    # Ouverture d’un fichier dans le répertoire correspondant avec un nom qui combine category_name et path avec
    # une extension de fichier ".jpg", et utilise le mode d'écriture binaire ('wb') pour écrire le contenu de l'image
    # dans le fichier.
    with open(img_path, 'wb') as img_file:

    # Enfin, la dernière ligne écrit le contenu de l'image (stocké dans la variable res.content) dans le fichier
    # ouvert avec la méthode write().
        img_file.write(res.content)

#--------------------------------------------#
# afficher un message au début du programme pour indiquer que le téléchargement est en cours, et à la fin de chaque 
# boucle de catégorie pour indiquer que la catégorie a été traitée avec succès. 
if __name__ == '__main__':
    print("Téléchargement en cours ... veuillez patienter !")

    # Utilisation de la 2eme Fonction "get_categories" pour récupérer les noms et les URL de chaque catégorie de livres
    # sur le site web. Ensuite, elle parcourt chaque paire nom / URL à l'aide de la boucle "for" et les stocke dans
    # les variables "category_name" et "category_url".
    for category_name,category_url in get_categories('https://books.toscrape.com/').items():

        # Création d’un dossier "data_csv" pour stocker les fichiers CSV qui seront créés pour chaque catégorie de livres.
        # Si le dossier existe déjà, la fonction ne fera rien grâce à l'argument "exist_ok=True".
        os.makedirs('data_csv', exist_ok=True)

        # Ouverture du fichier CSV portant le nom de la catégorie en cours de traitement. Le mode "w" signifie que le
        # fichier sera ouvert en mode écriture et que tout ce qui est déjà dans le fichier sera supprimé.
        # L'argument "encoding" est utilisé pour spécifier l'encodage du fichier CSV.
        with open('data_csv/' + category_name + '.csv', 'w', encoding='utf-8') as csvfile:

            # Création d’un objet "writer" à partir du module CSV, qui permet d'écrire des données dans le fichier CSV
            # ouvert précédemment. Le délimiteur "," est utilisé pour séparer les valeurs dans le fichier CSV.
            writer = csv.writer(csvfile, delimiter=',')

            # Ecriture de la première ligne (entete) du fichier CSV qui contiendra les noms des colonnes.
            writer.writerow(["universal_product_code","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"])

            # Utilisation de la 3eme Fonction "get_books_data" pour récupérer l'URL de chaque livre de la catégorie en
            # cours de traitement, puis parcourt chaque URL à l'aide de la boucle "for" et stocke l'URL dans
            # la variable "url".
            for url in get_books_data(category_url):

                # Appel et utilisation de la 1ere Fonction "get_book" pour extraire les données de chaque livre à partir
                # de son URL, puis stocke les données dans un dictionnaire appelé "book".
                book = get_book(url)

                # Ecriture des données du livre actuellement traité dans le fichier CSV. Les données sont extraites du
                # dictionnaire "book" à l'aide des clés correspondantes.
                writer.writerow([book['universal_product_code'],book['title'],book['price_including_tax'],book['price_excluding_tax'],book['number_available'],book['product_description'],book['category'],book['review_rating'],book['image_url']])

                # Utilise de la 4eme fonction "save_img" pour enregistrer l'image du livre actuellement traité. La fonction
                # prend trois arguments : l'URL de l'image, le nom de la catégorie et le code du livre.
                save_img(url=book['image_url'], category_name=book['category'], path=book['universal_product_code'], title=book['title'])
        print("Catégorie " +"\""+ category_name + "\"" + " ... OK")

print("Téléchargement terminé avec succès !")          

