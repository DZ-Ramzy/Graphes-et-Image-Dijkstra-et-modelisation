# Projet Graphes et Images (Dijkstra et Modélisation)

## Description du Projet

Ce projet modélise une image sous forme de graphe, où chaque pixel est un sommet et les relations de voisinage sont des arêtes pondérées par la différence d'intensité entre pixels. L'objectif est de calculer le plus court chemin entre deux pixels sélectionnés grâce à l'algorithme de Dijkstra optimisé par une file de priorité, et de visualiser ce chemin sur l'image d'origine.

## Fonctionnalités

1. Chargement d'une image via une interface graphique.
2. Conversion de l'image en niveaux de gris pour simplifier les calculs.
3. Représentation des pixels sous forme de graphe pondéré.
4. Calcul du plus court chemin entre deux sommets à l’aide de l’algorithme de Dijkstra.
5. Visualisation du chemin calculé directement sur l'image d'origine.

## Prérequis

- Python 3.x
- Bibliothèques Python :
  - `opencv-python (cv2)`
  - `Pillow (PIL)`
  - `heapq` (intégré)
  - `tkinter` (intégré)

Pour installer les bibliothèques nécessaires, exécutez :
```bash
pip install opencv-python pillow
```

## Installation
1. Clonez le dépôt ou téléchargez le fichier `imageToGraphe.py`.
2. Assurez-vous que toutes les dépendances sont installées.
3. Lancez le script Python :
```bash
python imageToGraphe.py
```

## Utilisation
1. Ouvrez l'application et chargez une image (formats supportés : `.jpeg`, `.png`, `.jpeg`).
2. Entrez les indices des pixels de départ et d'arrivée sous forme de coordonnées.
3. Cliquez sur "Calculer le chemin" pour afficher le chemin le plus court sur l'image.

## Structure du Code
- `Graphe` : Représentation du graphe avec des sommets et des arêtes.
- `Sommet` : Représentation des pixels comme sommets avec une liste de voisins.
- `Arete` : Représentation des relations entre pixels avec des poids.
- `Image` : Gère la conversion d'image en graphe et implémente l’algorithme de Dijkstra.
- `Interface` : Interface utilisateur créée avec Tkinter pour une interaction simplifiée.




