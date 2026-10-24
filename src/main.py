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

    def plot_temp(self, start: int = 0, end: int = 356):
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

        plt.title("Signal journalier sur 365 jours")

        plt.xlabel("Échantillons (jours)")
        plt.ylabel("°C")

        plt.grid(True)

        plt.legend()

        plt.show()

    def plot_snow(self, start: int = 0, end: int = 356):
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
            color="black",
        )

        plt.title(f"Signal journalier sur {end - start} jours")

        plt.xlabel("Échantillons (jours)")
        plt.ylabel("mm")

        plt.grid(True)

        plt.legend()

        plt.show()

    def plot_precipitation(self, start: int = 0, end: int = 356):
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
            color="black",
        )

        plt.title(f"Signal journalier sur {end - start} jours")

        plt.xlabel("Échantillons (jours)")
        plt.ylabel("mm")

        plt.grid(True)

        plt.legend()

        plt.show()

    def plot_wind_direction(self, start: int = 0, end: int = 356):
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
            color="black",
        )

        plt.title(f"Signal journalier sur {end - start} jours")

        plt.xlabel("Échantillons (jours)")
        plt.ylabel("")

        plt.grid(True)

        plt.legend()

        plt.show()

    def plot_wind(self, start: int = 0, end: int = 356):
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

        plt.title(f"Signal journalier sur {end - start} jours")

        plt.xlabel("Échantillons (jours)")
        plt.ylabel("km/h")

        plt.grid(True)

        plt.legend()

        plt.show()

    def plot_pressure(self, start: int = 0, end: int = 356):
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
            color="black",
        )

        plt.title(f"Signal journalier sur {end - start} jours")

        plt.xlabel("Échantillons (jours)")
        plt.ylabel("hPa")

        plt.grid(True)

        plt.legend()

        plt.show()

    def plot_temps_soleil(self, start: int = 0, end: int = 356):
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
            color="black",
        )

        plt.title(f"Signal journalier sur {end - start} jours")

        plt.xlabel("Échantillons (jours)")
        plt.ylabel("minutes")

        plt.grid(True)

        plt.legend()

        plt.show()


# %%
Signaux = Data()

Signaux.plot_temp(0, 27010)
Signaux.plot_temp(0, 3650)
Signaux.plot_temp()