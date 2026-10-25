# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# %%
class Data:
    """
    Classe des data et gestions des data
    """

    def __init__(self) -> None:

        self.__file_path = (
            Path(__file__).parent / ".." / "data" / "strasbourg_entzheim.csv"
        ).resolve()

        self.__data = np.genfromtxt(
            self.__file_path,
            delimiter=",",
            skip_header=1,
            usecols=range(1, 11),
            filling_values=0,
        )

        # température moyenne
        self.tavg = self.__data[:, 0]
        # température minimum
        self.tmin = self.__data[:, 1]
        # température maximum
        self.tmax = self.__data[:, 2]
        # taux de précipitation
        self.prcp = self.__data[:, 3]
        # taux de neige
        self.snow = self.__data[:, 4]
        # direction du vent
        self.wdir = self.__data[:, 5]
        # vitesse du vent (en km/h)
        self.wspd = self.__data[:, 6]
        # pic de rafale (en km/h)
        self.wpgt = self.__data[:, 7]
        # pression atmosphérique (en hPa)
        self.pres = self.__data[:, 8]
        # durée d’ensoleillement (en minutes)
        self.tsun = self.__data[:, 9]

    def calculer_moyenne_mediane(self, data):
        return np.nanmean(data), np.nanmedian(data)

    def afficher_stats(self, data, nom, unite, periode, start, end):
        # Affiche moyenne et médiane d'une variable sur une période.
        moy, med = self.calculer_moyenne_mediane(data[start:end])
        print(f"{nom} ({periode}) : la moyenne est de : {moy} {unite} et la médiane : {med} {unite}")

    def finaliser(self, titre, ylabel, start, end, periode):
        titre_complet = f"{titre} – {periode}" if periode else titre

        plt.title(titre_complet)
        plt.xlabel(f"Jours depuis le début de la période ({end - start} jours)")
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.4)
        plt.legend()
        plt.tight_layout()

        try:
            plt.gcf().canvas.manager.set_window_title(titre_complet)
        except AttributeError:
            pass

    def plot_temp(self, start: int = 0, end: int = 356, periode: str = ""):
        """
        Crée les plots pour les échantillons des températures

        Args:
            start (int, optional): Jours de début. Defaults to 0.
            end (int, optional): Jours de fin. Defaults to 356.
        """

        plt.figure(figsize=(10, 4))

        plt.plot(
            self.tmax[start:end],
            label="Tmax (Max)",
            color="tab:red",
            linestyle="--",
            alpha=0.8,
        )

        plt.plot(
            self.tavg[start:end],
            label="Tavg (Moyenne)",
            color="black",
            linewidth=1.5,
        )

        plt.plot(
            self.tmin[start:end],
            label="Tmin (Min)",
            color="tab:blue",
            linestyle="--",
            alpha=0.8,
        )

        self.finaliser(
            "Températures journalières à Strasbourg-Entzheim",
            "Température (°C)",
            start,
            end,
            periode,
        )

    def plot_snow(self, start: int = 0, end: int = 356, periode: str = ""):
        """
        Crée les plots pour les échantillons de neige

        Args:
            start (int, optional): Jours de début. Defaults to 0.
            end (int, optional): Jours de fin. Defaults to 356.
        """

        plt.figure(figsize=(10, 4))

        plt.plot(
            self.snow[start:end],
            label="Snow",
            color="tab:blue",
        )

        self.finaliser(
            "Hauteur de neige quotidienne à Strasbourg-Entzheim",
            "Neige (mm)",
            start,
            end,
            periode,
        )

    def plot_precipitation(self, start: int = 0, end: int = 356, periode: str = ""):
        """
        Crée les plots pour les échantillons des précipitions

        Args:
            start (int, optional): Jours de début. Defaults to 0.
            end (int, optional): Jours de fin. Defaults to 356.
        """

        plt.figure(figsize=(10, 4))

        plt.plot(
            self.prcp[start:end],
            label="Précipitation",
            color="tab:blue",
        )

        self.finaliser(
            "Précipitations quotidiennes à Strasbourg-Entzheim",
            "Précipitations (mm)",
            start,
            end,
            periode,
        )

    def plot_wind_direction(self, start: int = 0, end: int = 356, periode: str = ""):
        """
        Crée les plots pour les échantillons de direction du vent

        Args:
            start (int, optional): Jours de début. Defaults to 0.
            end (int, optional): Jours de fin. Defaults to 356.
        """

        plt.figure(figsize=(10, 4))

        plt.plot(
            self.wdir[start:end],
            label="Précipitation",
            color="tab:blue",
        )

        self.finaliser(
            "Direction moyenne du vent à Strasbourg-Entzheim",
            "Direction (°) – 0°=Nord, 90°=Est, 180°=Sud, 270°=Ouest",
            start,
            end,
            periode,
        )

    def plot_wind(self, start: int = 0, end: int = 356, periode: str = ""):
        """
        Crée les plots pour les échantillons de vitesse du vent

        Args:
            start (int, optional): Jours de début. Defaults to 0.
            end (int, optional): Jours de fin. Defaults to 356.
        """

        plt.figure(figsize=(10, 4))

        plt.plot(
            self.wspd[start:end],
            label="Wspd",
            color="black",
        )

        plt.plot(
            self.wpgt[start:end],
            label="Wpgt",
            color="tab:blue",
        )

        self.finaliser(
            "Vitesse du vent et rafales à Strasbourg-Entzheim",
            "Vitesse (km/h)",
            start,
            end,
            periode,
        )

    def plot_pressure(self, start: int = 0, end: int = 356, periode: str = ""):
        """
        Crée les plots pour les échantillons de pression atmosphérique

        Args:
            start (int, optional): Jours de début. Defaults to 0.
            end (int, optional): Jours de fin. Defaults to 356.
        """

        plt.figure(figsize=(10, 4))

        plt.plot(
            self.pres[start:end],
            label="Précipitation",
            color="tab:blue",
        )

        self.finaliser(
            "Pression atmosphérique quotidienne à Strasbourg-Entzheim",
            "Pression (hPa)",
            start,
            end,
            periode,
        )

    def plot_temps_soleil(self, start: int = 0, end: int = 356, periode: str = ""):
        """
        Crée les plots pour les échantillons de durée d’ensoleillement

        Args:
            start (int, optional): Jours de début. Defaults to 0.
            end (int, optional): Jours de fin. Defaults to 356.
        """

        plt.figure(figsize=(10, 4))

        plt.plot(
            self.tsun[start:end],
            label="Précipitation",
            color="tab:red",
        )

        self.finaliser(
            "Durée d'ensoleillement quotidienne à Strasbourg-Entzheim",
            "Ensoleillement (minutes)",
            start,
            end,
            periode,
        )


# %%
Signaux = Data()

periodes = {
    "Période complète": (0, len(Signaux.tavg)),
    "1950-1960": (0, 3650),
    "2014-2024": (23360, len(Signaux.tavg)),
    "Année 2024": (len(Signaux.tavg) - 365, len(Signaux.tavg)),
}

variables = {
    # "TEMPÉRATURES": (Signaux.plot_temp, Signaux.tavg, "°C"),
    # "PRÉCIPITATIONS": (Signaux.plot_precipitation, Signaux.prcp, "mm"),
    # "ENSOLEILLEMENT": (Signaux.plot_temps_soleil, Signaux.tsun, "min"),
    # "NEIGE": (Signaux.plot_snow, Signaux.snow, "mm"),
    # "VENT": (Signaux.plot_wind, Signaux.wspd, "km/h"),
    "PRESSION": (Signaux.plot_pressure, Signaux.pres, "hPa"),
}

for nom, (fonction, donnees, unite) in variables.items():
    print(f"\n// {nom} //")
    for periode, (start, end) in periodes.items():
        fonction(start, end, periode)
        Signaux.afficher_stats(donnees, nom, unite, periode, start, end)

plt.show()