# Projet Mathématiques et traitement du signal

Ce dépôt étudie des séries temporelles météorologiques issues de la station de
Strasbourg-Entzheim. L'objectif est d'analyser et de visualiser différents
signaux (température, précipitations, neige, vent, pression, ensoleillement),
puis d'étudier leur spectre et leur sous-échantillonnage.

## Structure du projet

```text
.
├── data/
│   └── strasbourg_entzheim.csv        # Données météorologiques journalières
├── notebooks/
│   └── main.ipynb                     # Version interactive du projet
├── plot/                              # Graphiques générés automatiquement
├── src/
│   └── main.py                        # Implémentation du traitement des signaux
├── .gitignore
├── projet.pdf                         # Rapport / document du projet
├── requirement.txt                    # Dépendances Python
└── README.md
```

## Données utilisées

Le fichier `data/strasbourg_entzheim.csv` contient des mesures quotidiennes de
la station de Strasbourg-Entzheim, sur une période couvrant la plupart du XXe et
XXIe siècle (en pratique du 1er janvier 1950 au 31 décembre 2024 selon les
données fournies).

Les variables exploitées par le code sont :

| Colonne | Description | Unité |
| ------- | ----------- | ----- |
| `tavg` | Température moyenne | °C |
| `tmin` | Température minimale | °C |
| `tmax` | Température maximale | °C |
| `prcp` | Précipitations | mm |
| `snow` | Neige | mm |
| `wdir` | Direction du vent | ° |
| `wspd` | Vitesse du vent | km/h |
| `wpgt` | Pic de rafale | km/h |
| `pres` | Pression atmosphérique | hPa |
| `tsun` | Durée d'ensoleillement | min |

Les valeurs manquantes sont gérées dans le code par interpolation linéaire avant
les calculs FFT et les tracés.

## Fonctionnalités du code

Le fichier `src/main.py` contient la classe `Signal`, qui permet de :

- charger les données depuis le CSV ;
- extraire chaque série météorologique dans un tableau NumPy ;
- afficher un ou plusieurs signaux temporels ;
- calculer les caractéristiques statistiques d'un signal ;
- produire le spectre fréquentiel d'un signal via une transformée de Fourier ;
- sous-échantillonner un signal et analyser le répliement spectral ;
- sauvegarder les figures dans le dossier `plot/` si demandé.

Les méthodes principales sont :

- `signal_data(...)` : renvoie amplitude, fréquence, phase, moyenne et signal filtré ;
- `plot_signal(...)` : trace un signal temporel ou plusieurs signaux comparés ;
- `spectrum(...)` : affiche le spectre d'un signal ;
- `downsample(...)` : applique un sous-échantillonnage avec option d'anti-repliement ;
- `plot_filtered_down(...)` : compare le spectre du signal original et du signal décimé.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

## Utilisation

Exemple d'utilisation dans Python :

```python
from src.main import Signal

s = Signal()

# Tracé du signal de température moyenne
s.plot_signal("tavg", start=0, end=365)

# Spectre de la température moyenne
s.spectrum("tavg", start=0, end=365)

# Sous-échantillonnage avec facteur 4
s.downsample("tavg", factor=4, start=0, end=365, plot=True)
```

Les figures peuvent être sauvegardées dans le dossier `plot/` en passant
`save_plot=True` ou `save=True` selon la méthode utilisée.

## Remarques

Ce projet est une application pédagogique de traitement du signal appliqué aux
mesures météorologiques. Il s'appuie principalement sur `numpy`, `pandas` et
`matplotlib` pour la manipulation numérique et la visualisation.
