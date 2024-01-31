import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
from codeOwner import *


# Ignorer les avertissements pour une meilleure lisibilité
warnings.filterwarnings('ignore')

## Configuration de la page
st.set_page_config(page_title='Store', page_icon=':bar-chart:', layout='wide')
## https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/ --> lien pour obtenir  des emojis shortcode de streamlit

### Affichage du titre principal
st.title(':bar_chart: ANALYSE EXPLORATOIRE DES DONNEES')

## 
st.header(CodeOwner().contact())

## Un petit contenair pour le titre principal, avec un padding-top:
st.markdown('<style>div.block-container{padding-top:1rem}<style>', unsafe_allow_html=True)

### Téléchargement d'un fichier via l'interface utilisateur
file = st.file_uploader(":file_folder: Télécharger un fichier", type=(["csv", "txt", "xlsx", "xls"]))


### Gestion du fichier : vérification de la présence et lecture
if file is not None:
    filename = file.name
    ## Afficher le nom du fichier
    st.write(f":memo: Fichier chargé : {filename}")
    
    # lire le fichier avec pandas:
    df = pd.read_excel(filename)
else:
    os.chdir(r'D:\PROJECTS\DASHBOARD_WITH_streamlit')
    df = pd.read_excel("Superstore.xls")
    
### Création des colonnes pour la mise en page
col1, col2 = st.columns((2))

## conversion de date AU format datetime
df["Order Date"] = pd.to_datetime(df['Order Date'])

## Récupération de la date min et max:
startDate = df["Order Date"].min()
endDate = df["Order Date"].max()

## création des entrées des dates de travail du fichier:
with col1:
    inputStartDate = st.date_input("Date De début", startDate)
    date1 = pd.to_datetime(inputStartDate)
    
with col2:
    inputEndDate = st.date_input("Date de Fin", endDate)
    date2 = pd.to_datetime(inputEndDate)

# Filtrage du DataFrame en fonction des dates sélectionnées
df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

### création d'une sidebar pour les filtres
sidebar = st.sidebar.header("Filtrer les données")

## filtrer par region:
region = st.sidebar.multiselect("Filtrer par region", df['Region'].unique())

## vérification de sélection ou pas:
if not region:
    df2 = df.copy()
else:
    df2 = df[df['Region'].isin(region)]

### Filtrer par Etat:
etat =  st.sidebar.multiselect("Filtrer par Etat", df2['State'].unique())
if not etat:
    df3 = df2.copy()
else:
    df3 = df2[df2['State'].isin(etat)]
       
#### Filtrer par ville 
ville = st.sidebar.multiselect('Filtrer par ville', df3['City'].unique())

###  FILTRAGE DES DONNEES EN PRENANT COMPTE DES FILTRES UTILISATEURS: 
if not ville and not etat and not region:
    st.write ("Aucun filtre n'a été appliqué.")
    filtered_df = df
elif not etat and not ville:
    filtered_df = df[df['Region'].isin(region)]
elif not region and not ville:
   filtered_df = df[df['State'].isin(etat)]
elif etat and ville:
    filtered_df =df3[df['State'].isin(etat) & df3['City'].isin(ville)]
elif region and ville:
    filtered_df =df3[df['Region'].isin(region) & df3['City'].isin(ville)]
elif region and etat:
    filtered_df =df3[df['Region'].isin(region) & df3['State'].isin(etat)]
elif ville:
    filtered_df = df3[df3['City'].isin(ville)]
else:
    filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(etat) & df3['City'].isin(ville)]


#### Analyse des ventes par catégories/Récupérer les catégories  et traçage de courbe
category_df = filtered_df.groupby(by=['Category'], as_index=False)["Sales"].sum()

# Affichage du graphique à barres pour les ventes par catégories
with col1:
    st.subheader('Ventes par Catégories')
    ##création d'un barchart avec px
    fig = px.bar(category_df, x ="Category", y="Sales", text= ['${:,.2f}'.format(x) for x in category_df['Sales']],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height= 220)

### # Affichage du graphique en camembert pour les ventes par région:
with col2:
    st.subheader("Ventes par Region")
    fig = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
    #fig.update_traces(text= filtered_df["Region"], textposition="outsider")
    
    st.plotly_chart(fig, use_container_width=True)
    
### Section pour afficher les données de catégorie et région avec
### la possibilité de télécharger les fichiers CSV
cl1, cl2 = st.columns(2)
with cl1:
    with st.expander('Table de la somme des ventes par catégorie'):
        # Affichage des données de catégorie avec un fond dégradé
        st.write(category_df.style.background_gradient(cmap="Blues"))
        
         # Conversion du DataFrame en CSV et téléchargement du bouton
        csv = category_df.to_csv(index= False).encode('utf-8')
        st.download_button("Télécharger les données", data = csv, file_name="Category.csv",
                           help="Cliquer pour télécharger les données", mime='text/csv')

# Deuxième colonne
with cl2:
    with st.expander('Table de la somme des ventes par Region'):
        # Groupement des données par région avec une somme des ventes
        region = filtered_df.groupby(by="Region", as_index=False)["Sales"].sum()
         # Affichage des données de région avec un fond dégradé
        st.write(region.style.background_gradient(cmap="Oranges"))
        
        # Conversion du DataFrame en CSV et téléchargement du bouton
        csv = region.to_csv(index= False).encode('utf-8')  
        st.download_button("Télécharger les données", data = csv, file_name="Region.csv",
                            help="Cliquer pour télécharger les données", mime='text/csv')

#### # Section pour l'analyse des séries temporelles
filtered_df['month_year'] = filtered_df['Order Date'].dt.to_period('M')
st.subheader('Analyse des séries temporelles')

# Création du DataFrame pour le graphique de ligne des ventes mensuelles
total_sales_by_Month_year = filtered_df.groupby(filtered_df['month_year'].dt.strftime("%Y :%b"))['Sales'].sum()
linechart = pd.DataFrame(total_sales_by_Month_year).reset_index()

# Trçage du graphique fig2  pour les ventes mensuelles:
fig2 = px.line(linechart, x="month_year", y="Sales", labels={"Ventes": "Montant"}, height=500,
               width=1000, template="gridon")
st.plotly_chart(fig2, use_container_width=True)

#### # Section pour visualiser et télécharger les données de la série temporelle
with st.expander('Regarder les données de la série temporelle'):
    
    # Affichage des données transposées avec un fond dégradé
    st.write(linechart.T.style.background_gradient(cmap="Red")) # Transposition
    csv = linechart.to_csv(index=False).encode('utf-8')
    st.download_button("Télécharger les données", data=csv, file_name='SeriesTemporelles.csv', mime='text/csv')
 
    
## # Section pour créer un treemap basé sur la région, la catégorie et les sous-catégories
st.subheader("Vu Hiérarchique des VENTES")
fig3 = px.treemap(filtered_df, path=["Region", "Category", "Sub-Category"], values="Sales", hover_data=["Sales"], 
                  color="Sales")
fig3.update_layout(width=700, height=600)
st.plotly_chart(fig3, use_container_width=True)


 ###Section pour créer deux graphiques en camembert représentant les segments de ventes
chart1, chart2 = st.columns(2)
chart1, chart2 = st.columns(2)

## fonction permettant de tracer les graphiques
def draw_twoPie():
    with chart1:
        st.subheader("Segement par Ventes")
        figure = px.pie(filtered_df, values="Sales", names="Segment", template="plotly_dark")
        figure.update_traces(text=filtered_df['Segment'], textposition='inside')
        st.plotly_chart(figure, use_container_width=True)

    with chart2:
        st.subheader("Segement par Ventes")
        figure = px.pie(filtered_df, values="Sales", names="Category", template="gridon")
        figure.update_traces(text=filtered_df['Category'], textposition='inside')
        st.plotly_chart(figure, use_container_width=True)
draw_twoPie()     ### On appelle la fonction  

   
###### Section pour créer un récapitulatif des ventes de la sous-catégorie mensuelle avec une table et un fond de couleur
import plotly.figure_factory as ff
st.subheader(':point_down: Récapitulatif des ventes de la sous-catégorie mensuelle')

def create_table():
    with st.expander('TAble de Récap'):
        # Création d'une table avec les dix premières lignes du DataFrame
        df_sample = df.head(10)[["Region", "State", "Category", "Sales", "Profit", "Quantity"]]
        fig = ff.create_table(df_sample, colorscale="spectral")
        st.plotly_chart(fig, use_container_width=True)
        
        # On ajoute un titre pour la vente des sous-catégories par mois
        st.markdown('Vente des Sous Catégories par Mois')
        filtered_df['month'] = filtered_df["Order Date"].dt.month_name()
        
        sub_category_year = pd.pivot_table(data=filtered_df, values="Sales", 
                                           index=["Sub-Category"],
                                        columns="month")
        st.write(sub_category_year.style.background_gradient(cmap='Blues'))
create_table() ### On appelle la fonction

### # Fonction pour créer un nuage de points représentant la relation entre les ventes, les profits et la quantité 
def create_scatter():
    # Create a scatter plot of the data with different markers for each category
    data1 = px.scatter(filtered_df, x="Sales", y="Profit", size="Quantity")
    data1["layout"].update(title="Relation entre les ventes et les profits", titlefont=dict(size=25),
                           xaxis=dict(title="Vente", titlefont=dict(size=20)), yaxis=dict(title="Profit", titlefont=dict(size=20)))
    return st.plotly_chart(data1, use_container_width=True)
create_scatter()

#### visualiser toutes les données  les
def viewData():
    with st.expander('Toutes les données'):
        st.write(filtered_df.iloc[:500, 1:30:2].style.background_gradient(cmap='Blues'))
viewData()

def downloadDataSet():
    csv = df.to_csv(index=False).encode('utf-8')
    bouton = st.download_button("Télécharger toutes les données", data=csv, file_name='Data.csv', mime="text/csv")
    return bouton
downloadDataSet()

