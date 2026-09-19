# Projet Chaîne de Markov - Simulation de propagation d'épidémie

Projet de processus stochastiques - Modélisation et simulation d'une épidémie sur une grille par une chaîne de Markov à temps continu.

Ce dépôt traite le **Sujet 3 : "Propagation d'une maladie par itinérance"**.

## Le projet

Simulation de la propagation d'une maladie contagieuse sur une grille 2D à partir d'un unique "patient 0", en modélisant les temps de contamination et de guérison comme des variables exponentielles (temps de séjour d'une chaîne de Markov à temps continu).

### Principe de la simulation

* Le **patient 0** effectue une marche aléatoire sur une grille (déplacement d'un pas dans une direction aléatoire parmi les 4 voisins)
* À chaque instant, on tire un **temps de contamination** (exponentiel, paramètre `mu`) et, pour chaque personne actuellement contaminée, un **temps de guérison** (exponentiel, paramètre `lambda`)
* La **prochaine action** (nouvelle contamination, guérison d'un patient, ou guérison du patient 0) est déterminée par le minimum de tous ces temps tirés — principe standard de simulation d'une chaîne de Markov à temps continu (méthode de Gillespie)
* Lorsqu'une contamination se produit, les 4 voisins de la position du patient 0 sont ajoutés aux personnes contaminées (sans doublon)
* La simulation s'arrête lorsque le patient 0 guérit **et** qu'un temps minimal (20 unités de temps) s'est écoulé ; les autres patients continuent ensuite d'être décontaminés progressivement jusqu'à extinction complète de l'épidémie

### Analyses réalisées

* **Simulation individuelle** : affichage de la configuration spatiale finale des patients contaminés à la guérison du patient 0, et évolution du nombre de contaminés au cours du temps
* **Temps moyen d'extinction** : estimation par simulation Monte-Carlo (1000 répétitions) du temps moyen avant extinction totale de l'épidémie
* **Étude de sensibilité** : évolution du temps moyen de décontamination en fonction du ratio `r = μ/λ` (contamination fixée puis guérison fixée), afin d'observer l'effet du rapport entre vitesse de contamination et vitesse de guérison sur la durée de l'épidémie

## Structure du projet

* `Projet_CDM.py` : script Python avec l'ensemble de la simulation et des analyses
* `Projet_Markov_2025_2026.pdf` : énoncé du mini-projet (3 sujets au choix, celui traité ici est le sujet 3)

## Lancer la simulation

1. Cloner le projet ou télécharger les fichiers
2. Installer les dépendances nécessaires

```
pip install numpy matplotlib
```

3. Lancer le script

```
python Projet_CDM.py
```

## Auteur

Clara GAMBARDELLO
Projet Chaînes de Markov (2025/2026)
