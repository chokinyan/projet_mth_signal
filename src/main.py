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

            plt.plot(x, label=f"{d} ({unité})", color="#241052")

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

        f_max = np.max(fft_freq)

        print("Fréquence maximale du spectre :", f_max, "cycles/jour")

        plt.figure(figsize=(10, 5))

        plt.stem(fft_freq[: len(amp)], amp, markerfmt=" ", basefmt=" ")

        plt.title(f"Spectre de {donnée} ({unite})")

        plt.xlabel("Fréquence (cycles/jour)")
        plt.ylabel("Amplitude")

        plt.grid()
        plt.show()

        return f_max

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

        indices = np.argsort(amp)[-n_harmonics:]

        for i in indices:
            signal += amp[i] * np.cos(2 * np.pi * fft_freq[i] * t + phase[i])

        if plot:
            plt.figure(figsize=(10, 5))
                        
                        
            plt.plot(
                self.__data[donnée][0][start:end],
                label=f"Signal original de {donnée} ({unite})",
                alpha=0.3,
                color='#CF79DD'
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

    def downsample(self, donnée: str, factor: int, start: int = 0, end: int = 365, plot: bool = True, antialias: bool = False) -> np.ndarray:
        """Sous-échantillonne un signal d'un facteur `factor`.

        Args:
            donnée (str): Nom de la donnée.
            factor (int): Facteur de sous-échantillonnage (1 point conservé sur `factor`).
            start (int, optional): Index de départ.
            end (int, optional): Index d'arrivée.
            plot (bool, optional): Affiche le signal sous-échantillonné.
            antialias (bool, optional): Applique un filtre passe-bas (moyenne glissante)
                avant la décimation pour limiter le repliement spectral.

        Raises:
            ValueError: Si la donnée n'est pas valide ou si factor < 1.
        """
        self.__check_data(donnée)

        factor, start, end = int(factor), int(start), int(end)
        if factor < 1:
            raise ValueError("Le facteur doit être un entier >= 1.")
        
        fe = 1 / factor
        f_nyquist = fe / 2

        print(f"Fréquence d'échantillonnage : {fe:.4f} échantillons/jour")
        print(f"Fréquence de Nyquist : {f_nyquist:.4f} cycles/jour")

        valeurs, unite = self.__data[donnée]          # on garde l'unité
        original = np.asarray(valeurs[start:end], dtype=float)

        if np.isnan(original).all():
            raise ValueError(f"Les données de {donnée} contiennent aucune valeur.")

        # Même traitement des valeurs manquantes que dans signal_data
        x = pd.Series(original).interpolate(limit_direction="both").to_numpy()

        if antialias and factor > 1:
            noyau = np.ones(factor) / factor          # moyenne glissante
            x = np.convolve(x, noyau, mode="same")    # filtre passe-bas

        resultat = x[::factor]                        # décimation (avant le plot)

        if plot:
            t_resultat = np.arange(len(x))[::factor]  # vrais instants des points conservés

            plt.figure(figsize=(10, 5))
            plt.plot(original, label=f"Signal original de {donnée} ({unite})",
                    alpha=0.3, color="#CF79DD")
            plt.plot(t_resultat, resultat, color="black",
                    label=f"Signal sous-échantillonné (facteur {factor})")

            plt.title(f"Sous-échantillonnage de {donnée} ({unite})")
            plt.xlabel("Temps (jours)")
            plt.ylabel("Valeur")
            plt.grid()
            plt.legend()
            plt.show()

        return resultat

    def plot_filtered_down(self, data, factor, start, end, plot=True, antialias=False):
        valeurs, unite = self.__data[data]
        x = pd.Series(np.asarray(valeurs[start:end], dtype=float)).interpolate(limit_direction="both").to_numpy()
        y = self.downsample(data, factor, start, end, plot, antialias)
        # freq_original = np.fft.rfftfreq(len(x), d=1)
        # spectre_original = np.abs(np.fft.rfft(x)) * 2 / len(x)

        freq_filtre = np.fft.rfftfreq(len(y), d=factor)
        spectre_filtre = np.abs(np.fft.rfft(y)) * 2 / len(x)

        indice_max = np.argmax(spectre_filtre[1:]) + 1
        frequence_max = freq_filtre[indice_max]
        amplitude_max = spectre_filtre[indice_max]

        print(f"Fréquence du pic maximal : {frequence_max:.6f} cycles/jour")
        print(f"Amplitude maximale : {amplitude_max:.4f}")

        # plt.plot(freq_original[1:], spectre_original[1:], label="spectre original", color="#CF79DD")
        plt.plot(freq_filtre[1:], spectre_filtre[1:], label=f"spectre sous échantillonné (facteur={factor})", color="black")

        plt.title(f"Comparaison des spectres de {data} ({unite})")
        plt.xlabel("Fréquence (cycles/jour)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.legend()
        plt.show()
    
    def filter_signal(self, donnée: str, start: int = 0, end: int = 365, M: int = 10) -> np.ndarray:
        """Filtre le signal à partir de ses n premières harmoniques

        Args:
            donnée (str): Nom de la donnée à filtrer.
            start (int): Index de départ.
            end (int): Index d'arrivée.
            M (int): Paramètre de filtrage.
        Raises:
            ValueError: Si la donnée n'est pas valide.
        """

        self.__check_data(donnée)

        valeurs, _ = self.__data[donnée]

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

        fft_freq = np.fft.rfftfreq(len_x, d=1)

        h = np.zeros(len(fft_freq), dtype=complex)

        for i in range(len(fft_freq)):
            f = fft_freq[i]
            if f == 0:
                h[i] = 1
            else:
                h[i] = np.exp(-1j * np.pi * f*(M - 1)) * (
                    np.sin(np.pi * M * f) / (M * np.sin(np.pi * f))
                )

        X = np.fft.rfft(x)
        H = h
        Y = X * H

        y = np.fft.irfft(Y, n=len_x)

        plt.figure(figsize=(10, 5))
        plt.plot(x, label=f"Signal original de {donnée}", alpha=0.3, color="#CF79DD")
        plt.plot(y, label=f"Signal filtré de {donnée} avec M={M}", color="black")
        plt.title(f"Signal filtré de {donnée}")
        plt.xlabel("Temps (jours)")
        plt.ylabel("Valeur")
        plt.grid()
        plt.legend()
        plt.show()

        return y

    def plot_filtered_spectrum(self, data, start, end, M):
        valeurs, unite = self.__data[data]
        x = pd.Series(np.asarray(valeurs[start:end], dtype=float)).interpolate(limit_direction="both").to_numpy()
        y = self.filter_signal(data, start, end, M)
        freq = np.fft.rfftfreq(len(x), d=1)

        spectre_original = np.abs(np.fft.rfft(x)) * 2 / len(x)
        spectre_filtre = np.abs(np.fft.rfft(y)) * 2 / len(x)

        plt.plot(freq[1:], spectre_original[1:], label="Signal original", color="#CF79DD")
        plt.plot(freq[1:], spectre_filtre[1:], label=f"Signal filtré (M={M})", color="black")

        plt.title(f"Comparaison des spectres de {data} ({unite})")
        plt.xlabel("Fréquence (cycles/jour)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.legend()
        plt.show()


# %%

if __name__ == "__main__":
    test = Signal()

    test.plot_signal("pres", len(test.tavg)-365, len(test.tavg))

    test.plot_filtered_down("tavg", 30, 0, len(test.tavg))

# %%
