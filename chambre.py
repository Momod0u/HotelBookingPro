"""
Définit les chambres de l'hôtel : abstraite, standard et luxueuse.
"""

from abc import ABC, abstractmethod


class Facturable(ABC):
    """Contrat : toute classe qui hérite doit générer une facture."""

    @abstractmethod
    def generer_facture(self) -> str:
        raise NotImplementedError


class Chambre(ABC):
    """Classe abstraite — modèle de base pour toutes les chambres."""

    def __init__(self, numero: int, type_chambre: str, prix_base: float):
        self._numero = numero
        self._type = type_chambre
        self._prix_base = prix_base
        self._est_disponible = True  # disponible par défaut

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def type(self) -> str:
        return self._type

    @property
    def prix_base(self) -> float:
        return self._prix_base

    def est_disponible(self) -> bool:
        return self._est_disponible

    def marquer_indisponible(self) -> None:
        self._est_disponible = False

    def marquer_disponible(self) -> None:
        self._est_disponible = True

    @abstractmethod
    def calculer_prix(self, nb_nuits: int, saison: str) -> float:
        """Chaque sous-classe calcule son propre prix."""
        raise NotImplementedError

    def __str__(self) -> str:
        statut = "disponible" if self._est_disponible else "occupée"
        return f"Chambre n°{self._numero} ({self._type}) - {self._prix_base}€/nuit - {statut}"


class ServiceSpa:
    """Services additionnels inclus dans une chambre luxueuse."""

    def __init__(self, spa_inclus: bool = True, petit_dejeuner: bool = True):
        self.spa_inclus = spa_inclus
        self.petit_dejeuner = petit_dejeuner

    def description_services(self) -> str:
        services = []
        if self.spa_inclus:
            services.append("Spa inclus")
        if self.petit_dejeuner:
            services.append("Petit-dejeuner inclus")
        return ", ".join(services) if services else "Aucun service"


class ChambreStandard(Chambre):
    """Chambre standard avec supplément de +20% en saison haute."""

    SUPPLEMENT_HAUTE_SAISON = 0.20

    def __init__(self, numero: int, prix_base: float):
        super().__init__(numero, "Standard", prix_base)

    def calculer_prix(self, nb_nuits: int, saison: str) -> float:
        prix_nuit = self._prix_base
        if saison.lower() == "haute":
            prix_nuit *= (1 + self.SUPPLEMENT_HAUTE_SAISON)
        return round(prix_nuit * nb_nuits, 2)


class ChambreLuxueuse(Chambre, ServiceSpa):
    """Chambre luxueuse avec spa, petit-déjeuner et +50€/nuit fixe."""

    SUPPLEMENT_FIXE_PAR_NUIT = 50.0

    def __init__(self, numero: int, prix_base: float):
        # Héritage multiple — on appelle les deux parents explicitement
        Chambre.__init__(self, numero, "Luxueuse", prix_base)
        ServiceSpa.__init__(self, spa_inclus=True, petit_dejeuner=True)

    def calculer_prix(self, nb_nuits: int, saison: str) -> float:
        prix_nuit = self._prix_base + self.SUPPLEMENT_FIXE_PAR_NUIT
        return round(prix_nuit * nb_nuits, 2)

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | {self.description_services()}"