# Projet Mathématiques et traitement du signal

Ce projet explore des données météorologiques journalières de la station de
Strasbourg-Entzheim à l'aide de Python, NumPy et Matplotlib. Les données sont
chargées comme des signaux temporels, puis différentes grandeurs peuvent être
visualisées sur une période donnée.

## Contenu du dépôt

```text
.
├── data/
│   └── strasbourg_entzheim.csv  # Données météorologiques journalières
├── notebooks/
│   └── main.ipynb               # Version interactive du projet
├── src/
│   └── main.py                  # Chargement des données et tracés
├── projet.pdf                   # Document du projet
└── requirement.txt              # Dépendances Python
```

## Données utilisées

Le fichier `data/strasbourg_entzheim.csv` contient des mesures journalières
du 1er janvier 1950 au 31 décembre 2024. Les colonnes exploitées par le
programme sont :

| Colonne  | Description             | Unité  |
| -------- | ----------------------- | ------- |
| `tavg` | Température moyenne    | °C     |
| `tmin` | Température minimale   | °C     |
| `tmax` | Température maximale   | °C     |
| `prcp` | Précipitations         | mm      |
| `snow` | Neige                   | mm      |
| `wdir` | Direction du vent       | ?       |
| `wspd` | Vitesse du vent         | km/h    |
| `wpgt` | Pic de rafale           | km/h    |
| `pres` | Pression atmosphérique | hPa     |
| `tsun` | Durée d'ensoleillement | minutes |

Les valeurs manquantes sont remplacées par `0` lors du chargement avec
`numpy.genfromtxt`.

## Fonctionnement

La classe `Data` de `src/main.py` :

1. charge le CSV ;
2. extrait chaque grandeur météorologique dans un tableau NumPy ;
3. fournit une méthode de visualisation pour chaque type de signal :

   - `plot_temp()` : températures minimale, moyenne et maximale ;
   - `plot_snow()` : neige ;
   - `plot_precipitation()` : précipitations ;
   - `plot_wind_direction()` : direction du vent ;
   - `plot_wind()` : vitesse du vent et pic de rafale ;
   - `plot_pressure()` : pression atmosphérique ;
   - `plot_temps_soleil()` : durée d'ensoleillement.

Les méthodes de tracé acceptent `start` et `end`. La longueur affichée est
calculée comme `abs(start - end)` ; par défaut, les 356 premiers échantillons
sont tracés.
