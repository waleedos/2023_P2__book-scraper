# Scrapper un site web : https://books.toscrape.com/

## Préambule
Projet réalisé dans le cadre de la formation Développeur d'Applications Python d'OpenClassrooms.
Ce programme permet de scrapper et récupérer les données des fiches produits d'un site de vente de livres. Le programme va récupérer l'ensemble des catégories de livres et pour chacune d'entre elles, effectuer les opérations suivantes :
Parcourir les pages produits des livres, puis en extraire les données pour les enregistrer dans un fichier CSV (Tous les livres de toutes les catégories), et Extraire les images des produits.
Si les répertoires dans lesquels nous stockons les images et les CSV sont inexistants, il les crées.

Note : Ce code est optimisé pour un seul site. Il faudra donc l'adapter à vos besoins si vous souhaitez l'utiliser sur un autre site marchand.

## Scénario
Vous êtes analyste marketing chez Books Online, une importante librairie en ligne spécialisée dans les livres d'occasion. Dans le cadre de vos fonctions, vous essayez de suivre manuellement les prix des livres d'occasion sur les sites web de vos concurrents, mais cela représente trop de travail et vous n'arrivez pas à y faire face : il y a trop de livres et trop de librairies en ligne ! Vous et votre équipe avez décidé d'automatiser cette tâche laborieuse via un programme (un scraper) développé en Python, capable d'extraire les informations tarifaires d'autres librairies en ligne.

Notre mission est donc de développer une version bêta de ce système pour suivre les prix des livres chez [Books to Scrape](https://books.toscrape.com/), un revendeur de livres en ligne. En pratique, dans cette version bêta, votre programme n'effectuera pas une véritable surveillance en temps réel des prix sur la durée. Il s'agira simplement d'une application exécutable à la demande visant à récupérer les prix au moment de son exécution.


## Compétences évaluées
* Gérer les données à l'aide du processus ETL
* Utiliser le contrôle de version avec Git et GitHub
* Appliquer les bases de la programmation en Python


## Prerequisites
* python 3
* Requests
* CSV
* BeautifulSoup 4
* os


## Instructions générales

### Clonage ou téléchargement
Clonez cette repositoire    : https://github.com/waleedos/2023_P2__book-scraper
Ou bien 
Télécharger le zip          : https://github.com/waleedos/2023_P2__book-scraper/archive/refs/heads/main.zip

### Création d'un nouvel environnement virtuel :
Une fois dézippé, et quand vous etes dans votre environnement, mettez vous dans ce dossier sur la racine

Ouvrez un terminal et créez votre environnement virtuel à l'aide de la commande suivante : 
```
python -m venv env
```
### Activation de votre nouvel environnement virtuel :
Activer votre nouvel environnement virtuel à l'aide de la commande suivante :
```
source env/bin/activate
```
### Mise à jour de votre environnement :
Remplire et installer les modules prerequis à partir de du fichier "requirements.txt" par la commande suivante:
```
pip install -r requirements.txt
```
## Fonctionnement :
Mettez vous a la racine du repertoire "le-scrypt" avec la commande suivante :
```
cd le-scrypt
```

Démarrez le scrypt avec la commande :
```
python main.py
```
Ou bien
```
python3 main.py
```
## Mes suggestions pour l’amélioration de ce Script : 
Utiliser une bibliothèque de scraping dédiée, telle que Scrapy, pour faciliter grandement  la collecte des données, car elle est conçue spécifiquement pour cette tâche et offre des fonctionnalités avancées telles que la gestion des proxies, le traitement en parallèle des pages, la gestion de la pagination, etc. 

Mettre tout le catalogue de tout le site internet dans un seul fichier .CSV tout en ajoutant une colonne par connaître les catégories, cela rendra la lecture et l’analyse des données beaucoup plus facile.

Ajouter des fonctions de validation  telles que la vérification de la structure des données, la validation des champs, etc, pour s'assurer que les données collectées sont correctes et éviter les erreurs : Il est important de valider les données collectées pour éviter les erreurs dans le traitement des données.

Ajouter une gestion d'erreurs plus robuste pour éviter les plantages du programme en cas d'erreur : Le scraping peut être assez imprévisible, donc il est important d'avoir une gestion d'erreurs solide pour éviter que le programme plante en cas d'erreur. Les erreurs courantes peuvent inclure une connexion interrompue, un serveur indisponible, une page indisponible, etc.

Utiliser des fonctions de log qui permettent de suivre les activités du programme, telles que les requêtes HTTP, les réponses, les erreurs, etc,  pour faciliter le débogage : Cela peut aider à identifier les problèmes plus rapidement.

Éviter les boucles imbriquées pour améliorer la lisibilité et les performances du code : Les boucles imbriquées peuvent rendre le code difficile à lire et à maintenir, en particulier pour les projets plus importants. Il est important de limiter l'utilisation de boucles imbriquées pour améliorer la lisibilité et les performances du code.

Utiliser des outils d'analyse de code tels que pylint pour détecter les erreurs et les problèmes de style : Les outils d'analyse de code peuvent aider à détecter les erreurs et les problèmes de style dans le code. Pylint est un outil populaire pour Python qui peut détecter les erreurs de syntaxe, les erreurs de style, les erreurs de logique, etc.

Optimiser le code pour améliorer les performances, par exemple en utilisant des techniques de traitement par lots pour éviter de surcharger les serveurs cibles : Le scraping peut être une tâche gourmande en ressources, donc il est important d'optimiser le code pour améliorer les performances et éviter de surcharger les serveurs cibles. Les techniques de traitement par lots peuvent aider à réduire la charge sur les serveurs en collectant les données en blocs plutôt que page par page.

### Powered by EL-WALID EL-KHABOU