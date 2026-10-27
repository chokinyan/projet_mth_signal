# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# %%
class Signal:
    """
    Classe Signal qui permet de charger et de visualiser les données météorologiques de Strasbourg Entzheim.
    """

    def __init__(self) -> None:

        self.__file_path = (
            Path(__file__).parents[1].resolve() / "data" / "strasbourg_entzheim.csv"
        ).resolve()

        self.__df = pd.read_csv(filepath_or_buffer=self.__file_path, sep=",")

        # température moyenne
        self.tavg = self.__df["tavg"].to_numpy()

        # température minimum
        self.tmin = self.__df["tmin"].to_numpy()

        # température maximum
        self.tmax = self.__df["tmax"].to_numpy()

        # taux de précipitation
        self.prcp = self.__df["prcp"].to_numpy()

        # taux de neige
        self.snow = self.__df["snow"].to_numpy()

        # direction du vent
        self.wdir = self.__df["wdir"].to_numpy()

        # vitesse du vent (en km/h)
        self.wspd = self.__df["wspd"].to_numpy()

        # pic de rafale (en km/h)
        self.wpgt = self.__df["wpgt"].to_numpy()

        # pression atmosphérique (en hPa)
        self.pres = self.__df["pres"].to_numpy()

        # durée d’ensoleillement (en minutes)
        self.tsun = self.__df["tsun"].to_numpy()

        self.__data = {
            "tavg": (self.tavg, "°C"),
            "tmin": (self.tmin, "°C"),
            "tmax": (self.tmax, "°C"),
            "prcp": (self.prcp, "mm"),
            "snow": (self.snow, "mm"),
            "wdir": (self.wdir, "°"),
            "wspd": (self.wspd, "km/h"),
            "wpgt": (self.wpgt, "km/h"),
            "pres": (self.pres, "hPa"),
            "tsun": (self.tsun, "min"),
        }

    def __check_data(self, donnée: str | tuple) -> None:
        """Vérifie si la donnée est valide

        Args:
            donnée (str | tuple): Nom de la donnée à vérifier.

        Raises:
            ValueError: Si la donnée n'est pas valide.
        """

        if isinstance(donnée, tuple):
            for d in donnée:
                if d not in self.__data:
                    raise ValueError(f"{d} n'est pas une donnée valide.")
        else:
            if donnée not in self.__data:
                raise ValueError(f"{donnée} n'est pas une donnée valide.")

    def plot_signal(self, donnée: str | tuple, start: int = 0, end: int = 365) -> None:
        """Génère le plot d'un ou plusieurs signal

        Args:
            donnée (str | tuple): Nom de la donnée ou tuple de noms de données à afficher.
            start (int, optional): Index de départ. Defaults to 0.
            end (int, optional): Index d'arrivée. Defaults to 365.

        Raises:
            ValueError: Si la donnée n'est pas valide.
        """

        données = donnée if isinstance(donnée, tuple) else (donnée,)

        self.__check_data(données)

        plt.figure(figsize=(10, 5))

        for d in données:
            valeurs, unité = self.__data[d]
            x = np.asarray(valeurs[start:end], dtype=float)

            plt.plot(x, label=f"{d} ({unité})")

        plt.title(" / ".join(données))

        plt.xlabel("Temps (jours)")
        plt.ylabel("Valeur")

        plt.grid()
        plt.legend()

        plt.show()

    def signal_data(
        self, donnée: str, start: int = 0, end: int = 365
    ) -> tuple[np.ndarray, np.ndarray, str, np.ndarray, float]:
        """Retourne les données d'un signal

        Args:
            donnée (str): Nom de la donnée à afficher.
            start (int, optional): Index de départ. Defaults to 0.
            end (int, optional): Index d'arrivée. Defaults to 365.

        Raises:
            ValueError: Si la donnée n'est pas valide.
        """
        self.__check_data(donnée)

        valeurs, unite = self.__data[donnée]

        x = np.asarray(valeurs[start:end], dtype=float)

        len_x = len(x)

        if np.isnan(
            x
        ).all():  # Check si les données contiennent que des valeurs manquantes
            raise ValueError(f"Les données de {donnée} contiennent aucune valeur.")

        if np.isnan(x).any():
            x = (
                pd.Series(x).interpolate(limit_direction="both").to_numpy()
            )  # On remplace les valeurs manquantes par interpolation linéaire ( on prend le plus proche voisin pour les valeurs manquantes au début et à la fin )

        amp = (
            np.abs(np.fft.rfft(x)) * 2 / len_x
        )  # On calcule l'amplitude de la transformée de Fourier et on la normalise

        fft_freq = np.fft.rfftfreq(len_x, d=1)

        phase = np.angle(
            np.fft.rfft(x)
        )  # On calcule la phase de la transformée de Fourier

        return (
            amp[1 : len(amp)],
            fft_freq[1 : len(amp)],
            unite,
            phase[1 : len(amp)],
            float(x.mean()),
        )  # On retourne l'amplitude, la fréquence, l'unité, la phase du signal et la valeur moyenne du signal

    def spectrum(self, donnée: str, start: int = 0, end: int = 365) -> None:
        """Génère le spectre d'un signal

        Args:
            donnée (str): Nom de la donnée à afficher.
            start (int, optional): Index de départ. Defaults to 0.
            end (int, optional): Index d'arrivée. Defaults to 365.

        Raises:
            ValueError: Si la donnée n'est pas valide.
        """

        amp, fft_freq, unite, _, _ = self.signal_data(donnée, start, end)

        plt.figure(figsize=(10, 5))

        plt.stem(fft_freq[: len(amp)], amp, markerfmt=" ", basefmt=" ")

        plt.title(f"Spectre de {donnée} ({unite})")

        plt.xlabel("Fréquence (cycles/jour)")
        plt.ylabel("Amplitude")

        plt.grid()
        plt.show()

    def reconstruct_signal(
        self,
        donnée: str,
        start: int = 0,
        end: int = 365,
        n_harmonics: int = 10,
        plot: bool = False,
    ) -> np.ndarray | None:
        """Reconstruit le signal à partir de ses n premières harmoniques

        Args:
            donnée (str): Nom de la donnée à reconstruire.
            start (int, optional): Index de départ. Defaults to 0.
            end (int, optional): Index d'arrivée. Defaults to 365.
            n_harmonics (int, optional): Nombre d'harmoniques à utiliser pour la reconstruction. Defaults to 10.

        Raises:
            ValueError: Si la donnée n'est pas valide.
        """

        amp, fft_freq, unite, phase, mean_value = self.signal_data(donnée, start, end)

        signal = np.zeros(
            len(amp) * 2, dtype=float
        )  # On initialise le signal à reconstruire

        n_harmonics = min(
            n_harmonics, len(amp)
        )  # On s'assure de ne pas dépasser le nombre d'harmoniques disponibles

        signal += mean_value  # On ajoute la valeur moyenne du signal

        t = np.arange(len(amp) * 2, dtype=float)

        for i in range(n_harmonics):
            signal += amp[i] * np.cos(2 * np.pi * fft_freq[i] * t + phase[i])

        if plot:
            plt.figure(figsize=(10, 5))
                        
                        
            plt.plot(
                self.__data[donnée][0][start:end],
                label=f"Signal original de {donnée} ({unite})",
                alpha=0.3,
                color='red'
            )
            
            plt.plot(signal, label=f"Signal reconstruit avec {n_harmonics} harmoniques",color='black')
            
            plt.title(f"Signal reconstruit de {donnée} ({unite})")
            plt.xlabel("Temps (jours)")
            plt.ylabel("Valeur")
            plt.grid()
            plt.legend()
            plt.show()

        else:
            return signal


# %%

if __name__ == "__main__":
    test = Signal()

    test.reconstruct_signal("tavg", start=0, end=500, n_harmonics=100, plot=True)
