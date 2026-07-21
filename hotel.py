"""
Module hotel
------------
Définit la classe Hotel, qui agrège des Chambre, des Client et des
Reservation.
"""

import csv
import os
from typing import List

from chambre import Chambre
from client import Client
from reservation import Reservation
from exceptions import ChambreNonDisponibleException


class Hotel:
   

    def __init__(self, nom: str = "HotelBookingPro"):
        self.nom = nom
        self.chambres: List[Chambre] = []
        self.clients: List[Client] = []
        self.reservations: List[Reservation] = []

    def ajouter_client(self, client: Client) -> None:
        """Ajoute un client à la liste des clients de l'hôtel."""
        self.clients.append(client)
        print(f"Client ajouté : {client}")

    def ajouter_chambre(self, chambre: Chambre) -> None:
        """Ajoute une chambre à la liste des chambres de l'hôtel."""
        self.chambres.append(chambre)
        print(f"Chambre ajoutée : {chambre}")

    def reserver(self, client: Client, chambre: Chambre, nb_nuits: int, saison: str) -> Reservation:
        """
        Effectue une réservation pour un client sur une chambre donnée.

        Lève ChambreNonDisponibleException si la chambre est déjà occupée.
        """
        if not chambre.est_disponible():
            raise ChambreNonDisponibleException(
                f"La chambre n°{chambre.numero} ({chambre.type}) est déjà occupée."
            )

        reservation = Reservation(client, chambre, nb_nuits, saison)
        reservation.confirmer()
        self.reservations.append(reservation)
        return reservation

    def charger_reservations(self, chemin_csv: str = "reservations.csv") -> None:
        """
        Lit les réservations enregistrées dans un fichier CSV et les
        affiche (chargement à titre informatif / historique).
        """
        if not os.path.isfile(chemin_csv):
            print(f"Aucun fichier '{chemin_csv}' trouvé.")
            return

        with open(chemin_csv, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            print(f"--- Historique des réservations ({chemin_csv}) ---")
            for ligne in reader:
                print(
                    f"{ligne['date_reservation']} | {ligne['client_nom']} | "
                    f"Chambre n°{ligne['chambre_numero']} ({ligne['chambre_type']}) | "
                    f"{ligne['nb_nuits']} nuit(s) | {ligne['saison']} | "
                    f"{ligne['montant_total']} € | confirmée={ligne['confirmee']}"
                )

    def chambres_disponibles(self) -> List[Chambre]:
        """Retourne la liste des chambres actuellement disponibles."""
        return [c for c in self.chambres if c.est_disponible()]

    def __str__(self) -> str:
        return (
            f"Hotel({self.nom}) - {len(self.chambres)} chambre(s), "
            f"{len(self.clients)} client(s), {len(self.reservations)} réservation(s)"
        )
