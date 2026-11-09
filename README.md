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

| Colonne  | Description             | Unité |
| -------- | ----------------------- | ------ |
| `tavg` | Température moyenne    | °C    |
| `tmin` | Température minimale   | °C    |
| `tmax` | Température maximale   | °C    |
| `prcp` | Précipitations         | mm     |
| `snow` | Neige                   | mm     |
| `wdir` | Direction du vent       | °     |
| `wspd` | Vitesse du vent         | km/h   |
| `wpgt` | Pic de rafale           | km/h   |
| `pres` | Pression atmosphérique | hPa    |
| `tsun` | Durée d'ensoleillement | min    |

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

Les méthodes publiques de la classe `Signal` sont :

- `signal_data(donnée, start=0, end=365)`  
  Extrait une partie du signal, gère les valeurs manquantes et renvoie :
  - `amp` : amplitudes du spectre ;
  - `fft_freq` : fréquences associées ;
  - `unite` : unité du signal ;
  - `phase` : phase de la transformée de Fourier ;
  - `moyenne` : moyenne du signal ;
  - `x` : signal traité ;
  - `len_x` : longueur du signal.

- `plot_signal(donnée, start=0, end=365, save_plot=False)`  
  Affiche un ou plusieurs signaux temporels. `donnée` peut être une chaîne comme `"tavg"` ou un tableau NumPy. Le paramètre `start` / `end` définit la fenêtre à tracer. `save_plot=True` enregistre la figure dans le dossier `plot/`.

- `spectrum(donnée, start=0, end=365, unilateral=True, save_plot=False)`  
  Calcule et affiche le spectre d'un signal à l'aide de la FFT. `unilateral=True` affiche le spectre unilatéral, `False` affiche le spectre complet.

- `downsample(donnée, factor, start=0, end=365, plot=True, antialias=False, save_plot=False)`  
  Sous-échantillonne le signal avec un facteur donné (`factor`). Si `antialias=True`, un lissage glissant est appliqué avant la décimation pour réduire le repliement spectral. La méthode retourne le signal décimé.

- `spectrum_downsample(data, factor, start, end, antialias=False, save_plot=False)`  
  Compare le spectre du signal original et du signal sous-échantillonné. Utile pour observer les effets du repliement spectral et valider le choix de `factor`.

Les méthodes privées comme `__plot()` ou `__check_data()` ne sont pas destinées à être appelées directement ; elles servent au fonctionnement interne de la classe.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

## Remarques

Ce projet est une application pédagogique de traitement du signal appliqué aux
mesures météorologiques. Il s'appuie principalement sur `numpy`, `pandas` et
`matplotlib` pour la manipulation numérique et la visualisation.
