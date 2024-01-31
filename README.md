# interactiveDashboard
Projet d'Analyse Exploratoire des Données avec Streamlit
Ce projet vise à créer un tableau de bord interactif pour l'analyse exploratoire des données à l'aide de Streamlit. Le tableau de bord permet d'explorer et d'analyser les ventes d'un ensemble de données, avec des fonctionnalités telles que le filtrage par date, région, état et ville.

Fonctionnalités principales :
Téléchargement de Fichier : Les utilisateurs peuvent télécharger un fichier au format CSV, TXT, XLSX ou XLS via l'interface utilisateur.

Filtrage Dynamique : Le tableau de bord propose des filtres dynamiques par région, état et ville pour affiner les données selon les besoins de l'utilisateur.

Graphiques Interactifs :

Graphique à barres pour les ventes par catégories.
Graphique en camembert pour les ventes par région.
Graphique de ligne pour l'analyse des séries temporelles des ventes mensuelles.
Treemap pour visualiser hierarchiquement les ventes par région, catégorie et sous-catégorie.
Récapitulatif des Ventes : Un récapitulatif des ventes de sous-catégorie mensuelle est présenté sous forme de table avec un fond de couleur.

Graphiques de Segmentation : Deux graphiques en camembert présentent les segments de ventes.

Nuage de Points : Un nuage de points illustre la relation entre les ventes, les profits et la quantité.

Visualisation des Données : Une section permet de visualiser les données filtrées, avec la possibilité de télécharger les données en format CSV.

Comment exécuter le projet :
Installer les bibliothèques nécessaires en exécutant pip install streamlit plotly pandas.

Exécuter le script avec la commande streamlit run nom_du_script.py.

Ouvrir le navigateur et accéder à l'URL fournie par Streamlit.

Profitez de l'exploration interactive des données!
