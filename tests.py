"""
tests.py
--------
Tests unitaires (bonus) validant les cas normaux et les cas d'erreur
du projet HotelBookingPro.
Lancer avec : python3 -m unittest tests.py -v
"""

import os
import unittest

from hotel import Hotel
from client import Client
from chambre import ChambreStandard, ChambreLuxueuse
from reservation import Reservation
from exceptions import ChambreNonDisponibleException


class TestChambre(unittest.TestCase):

    def test_prix_standard_saison_basse(self):
        chambre = ChambreStandard(numero=1, prix_base=50.0)
        self.assertEqual(chambre.calculer_prix(2, "basse"), 100.0)

    def test_prix_standard_saison_haute(self):
        chambre = ChambreStandard(numero=1, prix_base=50.0)
        # 50 * 1.20 * 2 nuits = 120.0
        self.assertEqual(chambre.calculer_prix(2, "haute"), 120.0)

    def test_prix_luxueuse(self):
        chambre = ChambreLuxueuse(numero=2, prix_base=70.0)
        # (70 + 50) * 3 nuits = 360.0
        self.assertEqual(chambre.calculer_prix(3, "basse"), 360.0)

    def test_chambre_luxueuse_services_inclus(self):
        chambre = ChambreLuxueuse(numero=2, prix_base=70.0)
        self.assertTrue(chambre.spa_inclus)
        self.assertTrue(chambre.petit_dejeuner)

    def test_disponibilite_par_defaut(self):
        chambre = ChambreStandard(numero=3, prix_base=40.0)
        self.assertTrue(chambre.est_disponible())
        chambre.marquer_indisponible()
        self.assertFalse(chambre.est_disponible())
        chambre.marquer_disponible()
        self.assertTrue(chambre.est_disponible())


class TestReservationEtHotel(unittest.TestCase):

    def setUp(self):
        self.hotel = Hotel("Hotel Test")
        self.chambre = ChambreStandard(numero=10, prix_base=25.0)
        self.client = Client(id=1, nom="Test Client", email="test@example.com")
        self.hotel.ajouter_chambre(self.chambre)
        self.hotel.ajouter_client(self.client)
        self.fichier_test = "reservations_test.csv"

    def tearDown(self):
        if os.path.isfile(self.fichier_test):
            os.remove(self.fichier_test)

    def test_reservation_reussie(self):
        reservation = self.hotel.reserver(self.client, self.chambre, 2, "basse")
        self.assertIsInstance(reservation, Reservation)
        self.assertFalse(self.chambre.est_disponible())
        self.assertIn(reservation, self.hotel.reservations)

    def test_double_reservation_leve_exception(self):
        self.hotel.reserver(self.client, self.chambre, 2, "basse")
        with self.assertRaises(ChambreNonDisponibleException):
            self.hotel.reserver(self.client, self.chambre, 1, "basse")

    def test_generer_facture_contient_montant(self):
        reservation = self.hotel.reserver(self.client, self.chambre, 2, "basse")
        facture = reservation.generer_facture()
        self.assertIn("MONTANT TOTAL", facture)
        self.assertIn(self.client.nom, facture)

    def test_sauvegarder_et_charger_csv(self):
        reservation = self.hotel.reserver(self.client, self.chambre, 2, "basse")
        reservation.sauvegarder(self.fichier_test)
        self.assertTrue(os.path.isfile(self.fichier_test))
        with open(self.fichier_test, encoding="utf-8") as f:
            contenu = f.read()
        self.assertIn(self.client.nom, contenu)


if __name__ == "__main__":
    unittest.main()
