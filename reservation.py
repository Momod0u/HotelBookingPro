"""
Module reservation
-------------------
Définit la classe Reservation, qui utilise la composition (elle contient
un Client et une Chambre) et implémente l'interface Facturable.
"""

import csv
import os
from datetime import datetime

from chambre import Chambre, Facturable
from client import Client


class Reservation(Facturable):
   

    FICHIER_CSV_DEFAUT = "reservations.csv"

    def __init__(self, client: Client, chambre: Chambre, nb_nuits: int, saison: str):
        self.client = client
        self.chambre = chambre
        self.nb_nuits = nb_nuits
        self.saison = saison
        self.date_reservation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._confirmee = False

    def confirmer(self) -> None:
        """
        Confirme la réservation : marque la chambre comme indisponible.
        """
        self.chambre.marquer_indisponible()
        self._confirmee = True
        print(
            f"Réservation confirmée : {self.client.nom} -> "
            f"Chambre n°{self.chambre.numero} ({self.chambre.type}) "
            f"pour {self.nb_nuits} nuit(s), saison {self.saison}."
        )

    def generer_facture(self) -> str:
        """
        Génère et retourne la facture sous forme de chaîne de caractères.
        """
        montant = self.chambre.calculer_prix(self.nb_nuits, self.saison)
        facture = (
            "----------------------------------------\n"
            "           FACTURE - HotelBookingPro\n"
            "----------------------------------------\n"
            f"Date          : {self.date_reservation}\n"
            f"Client        : {self.client.nom} ({self.client.email})\n"
            f"Chambre       : n°{self.chambre.numero} - {self.chambre.type}\n"
            f"Nb de nuits   : {self.nb_nuits}\n"
            f"Saison        : {self.saison}\n"
            f"Statut        : {'Confirmée' if self._confirmee else 'Non confirmée'}\n"
            "----------------------------------------\n"
            f"MONTANT TOTAL : {montant:.2f} €\n"
            "----------------------------------------"
        )
        return facture

    def sauvegarder(self, chemin_csv: str = None) -> None:
        """
        Écrit les informations de la réservation dans un fichier CSV.
        Ajoute une ligne à la suite si le fichier existe déjà.
        """
        chemin_csv = chemin_csv or self.FICHIER_CSV_DEFAUT
        fichier_existe = os.path.isfile(chemin_csv)

        with open(chemin_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not fichier_existe:
                writer.writerow([
                    "date_reservation", "client_id", "client_nom", "client_email",
                    "chambre_numero", "chambre_type", "nb_nuits", "saison",
                    "montant_total", "confirmee"
                ])
            montant = self.chambre.calculer_prix(self.nb_nuits, self.saison)
            writer.writerow([
                self.date_reservation,
                self.client.id,
                self.client.nom,
                self.client.email,
                self.chambre.numero,
                self.chambre.type,
                self.nb_nuits,
                self.saison,
                f"{montant:.2f}",
                self._confirmee,
            ])
        print(f"Réservation sauvegardée dans '{chemin_csv}'.")

    def __str__(self) -> str:
        return (
            f"Reservation(client={self.client.nom}, chambre={self.chambre.numero}, "
            f"nb_nuits={self.nb_nuits}, saison={self.saison})"
        )
