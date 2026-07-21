"""
Module exceptions
------------------
Ce module regroupe toutes les exceptions métier de HotelBookingPro.
"""


class ChambreNonDisponibleException(Exception):
    def __init__(self, message: str = "Cette chambre n'est pas disponible."):
        # On stocke le message pour y accéder via exception.message
        self.message = message
        # On transmet le message à la classe mère Exception
        super().__init__(self.message)

    def __str__(self) -> str:
        # Affichage clair lors d'un print() ou d'un traceback
        return f"[HotelBookingPro] Erreur réservation : {self.message}"