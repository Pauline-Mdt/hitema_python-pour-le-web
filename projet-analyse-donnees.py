# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

"""
# Projet analyse de données

## Consignes:
Votre analyse sous forme de Jupyter Notebook déposé sur votre git en PUBLIC devra contenir:
* Une problématique pertinente (c-à-d ou il est possible de répondre avec des données)
* Au moins 1 diagramme avec données continues, type nuage de point ou histogramme
* Au moins 2 diagrammes avec des données discrètes
* Au moins 3 graphiques avec des données catégoriques
* 1 boîte à moustaches avec filtrage des données aberrantes sur le dataset (si il y en a)
* 1 heat map avec matrice de corrélation (si pertinent)
* Des commentaires clairs et pertinents pour chaque graphiques

## Problématique:

**Est-ce que le genre et/ou l'âge influent sur les performances de l'athlète ?**

### Import des données

Depuis le fichier 2019-games-athletes.csv
"""

games2019_athletes = pd.read_csv('./2019-games-athletes.csv')

"""### Analyse des composantes et nettoyage des données"""

if st.checkbox('Monter le jeu de données initial'):
    games2019_athletes

"""Le jeu de données étudié contient un échantillon de 394 individus présentés en fonction de 18 propriétés."""

games2019_athletes.info()

"""En observant les composantes du jeu de données, on remarque que :
* Les principales caractéristiques que l'on va pouvoir étudier pour essayer de répondre à la problématique sont l'âge et le genre des athlètes. On peut également s'intéresser aux caractéristiques physiques que sont le poids et la taille.

* Certaines valeur réapparaissent plusieurs fois et sont communes à plusieurs athlètes. Elles permettent de les regrouper et d'établir des catégories notamment selon le pays d'origine, le statut, le genre, et la division. Parmi ces catégories, ce sont le genre et la division qui nous intéressent pour nous aider à apporter une réponse.
"""

gender = games2019_athletes.gender.unique()
division = games2019_athletes.division.unique()
# st.text('Genre = {}\n\nDivision = {}'.format(gender, division))

option = st.selectbox(
    'Afficher les valeurs et leur répartition de la propriété:',
    ('','gender', 'division')
)

if option == 'gender':
    'Genre = ', format(gender)
elif option == 'division':
    'Division = ', format(division)
else:
    '-- Choississez une option pour afficher la liste des valeurs d\'une propriété et leur répartition --'

if option != '':
    sb.histplot(data=games2019_athletes, y=option)
    st.pyplot(plt.gcf())

"""Pour la suite on gardera uniquement les composantes citées précédemment."""

games2019_athletes_filtered = games2019_athletes.loc[:, ['division', 'age', 'gender', 'height', 'weight', 'overallscore']]

"""
On voit aussi dans la liste des genres la présence d'une valeur 'X' en très grand nombre.

Afin d'avoir une cohérence, on attribue un genre aux individus pour qui il n'est pas défini (ayant pour valeur 'X') selon les divisions dans lesquels ils se trouvent.
"""

games2019_athletes_filtered.loc[games2019_athletes_filtered.division.str.contains('Men', case=True), 'gender'] = 'M'
games2019_athletes_filtered.loc[games2019_athletes_filtered.division.str.contains('Women', case=True), 'gender'] = 'W'

"""Et on remplace les valeurs des genres par 0 pour Men et 1 pour Women afin de faciliter leur prise en compte dans les statistiques et de travailler plus facilement avec."""

games2019_athletes_filtered['gender'] = games2019_athletes_filtered['gender'].replace(['M','W'],[0,1])

if st.checkbox('Monter le jeu de données filtré et modifié'):
    games2019_athletes_filtered

games2019_athletes_filtered.info()

"""On va donc travailler avec un jeu de données qui présente 6 propriétés pour le même nombre d'individus.

### Analyse des données

1.   Corrélation entre les différentes propriétés
"""

matrice_games = games2019_athletes_filtered.corr()
plt.figure(figsize= (9,6))
sb.heatmap(data=matrice_games, annot=True)
st.pyplot(plt.gcf())

"""La heatmap permet de mettre en évidence que la plus forte corélation se fait entre l'âge et le score. Le genre présente une corélation beaucoup moins élevée mais toujours plus importante que la taille et le poids qui sont quasiment nulle voir négative.

2.   L'âge
"""

plt.figure(figsize= (18,6))
sb.histplot(data=games2019_athletes_filtered, x="age")
st.pyplot(plt.gcf())

"""La distribution des athlètes par âge montre clairement que le nombre de participants diminue fortement au delà de 35-40 ans."""

sb.relplot(data=games2019_athletes_filtered, x="age", y="overallscore", height=6)
st.pyplot(plt.gcf())
#sb.lmplot(data=games2019_athletes_filtered, x="age", y="overallscore", height=6)

"""On voit que les données sont très disparates, ce qui correspond à la faible corélation de la heatmap bien qu'elle était la plus élevée, et elles ne permettent pas de définir de façon fiable une relation entre l'âge et les performances."""

#games2019_athletes.groupby('division').size()

sb.catplot(data=games2019_athletes_filtered, x="division", y="overallscore", kind="box", height=6, aspect=2)
st.pyplot(plt.gcf())

"""Il est intéressant de regarder les performances selon les divisions qui sont classées par tranche d'âge. On constate facilement que les statistiques des performances sont plus elevés pour toutes les divisions de plus de 35ans."""

plt.figure(figsize= (18,6))
sb.histplot(data=games2019_athletes_filtered, x="division")
st.pyplot(plt.gcf())

"""Cependant il est important de garder en tête la distribution des athlètes par division qui montre un faible nombre d'athlètes dans les divisions au delà de 35 ans (moins de 20 individus chacune). Encore une fois, on ne peut pas affirmer qu'il y a un lien entre les catégories d'âge et les performances avec si peu de données."""

#sb.lmplot(data=games2019_athletes_filtered, x="age", y="overallscore", hue="gender", height=6)

"""3.   Le genre"""

plt.figure(figsize= (18,6))
sb.histplot(data=games2019_athletes_filtered, x="gender")
st.pyplot(plt.gcf())

"""La distribution des athlètes par genre montre en revanche une répartition presque identique entre les athlètes hommes et femme."""

sb.catplot(data=games2019_athletes_filtered, x="gender", y="overallscore", kind="box", height=6)
st.pyplot(plt.gcf())

"""On remarque que les statistiques des performances sont fortement similaires selon le genre des athlètes, qu'il s'agit des résultats de 50% d'entre eux ou de la médiane."""

games2019_athletes_filtered.groupby('gender').overallscore.describe()

sb.catplot(data=games2019_athletes_filtered, x="gender", y="overallscore", kind="bar", height=6)
st.pyplot(plt.gcf())

"""Dans la continuité du graphique précédent, on constate que les moyennes sont similaires et les écart-types équivalents malgré la distinction du genre. Il n'est donc pas possible d'affirmer ici que le genre a une influence sur les performances des athlètes.

## Conclusion :

Bien que les éléments étudiés permettent de montrer une tendance sur l'équilibre des performances entre les hommes et les femmes, ce n'est pas aussi évident en ce qui concerne la relation entre l'âge et la performance des athlètes quelque soit leur genre.

Il faut aussi souligner qu'un échantillon de 394 individus reste insuffisant pour établir de réelles statistiques. Il serait donc préférable de refaire une étude avec un jeu de données contenant un nombre beaucoup plus élevé d'individus.

Le présent jeu de données ne permet donc pas de répondre à la problématique de façon satisfaisante.

*Fact*

Les charges Rx des athlètes ont été augmentées il y a deux ans, car celles des femmes n'étaient plus assez élevées lors des compétitions.

Les charges sont passées de :
* 17,5kg à 22,5kg pour les femmes
* 22,5kg à 30kg pour les hommes
"""

