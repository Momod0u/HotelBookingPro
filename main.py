"""
main.py
-------
Démontre : création de chambres/clients, réservation, calcul de prix
selon la saison, gestion de la double réservation, génération de
facture, écriture/lecture dans reservations.csv.
"""

from hotel import Hotel
from client import Client
from chambre import ChambreStandard, ChambreLuxueuse
from exceptions import ChambreNonDisponibleException


def separateur(titre: str) -> None:
    print("\n" + "=" * 50)
    print(titre)
    print("=" * 50)


def main():
    separateur("1. Création de l'hôtel, des chambres et des clients")
    hotel = Hotel("Hôtel Teranga")

    # Création des chambres (parenthèse corrigée)
    chambre_70 = ChambreStandard(numero=70, prix_base=40.0)
    chambre_71 = ChambreStandard(numero=71, prix_base=45.0)
    chambre_72 = ChambreLuxueuse(numero=72, prix_base=50.0)

    # Ajout des chambres (noms de variables corrigés)
    hotel.ajouter_chambre(chambre_70)
    hotel.ajouter_chambre(chambre_71)
    hotel.ajouter_chambre(chambre_72)

    client_1 = Client(id=1, nom="Fatima Kane", email="fak@example.com")
    client_2 = Client(id=2, nom="Mamadou Ba", email="mba@example.com")

    hotel.ajouter_client(client_1)
    hotel.ajouter_client(client_2)

    client_1.presentation()
    client_2.presentation()

    separateur("2. Calcul de prix selon la saison")
    print(
        f"Chambre 70 (standard) - 3 nuits, saison basse : "
        f"{chambre_70.calculer_prix(3, 'basse')} €"
    )
    print(
        f"Chambre 70 (standard) - 3 nuits, saison haute : "
        f"{chambre_70.calculer_prix(3, 'haute')} €"
    )
    # Appel corrigé sur chambre_72 (luxueuse)
    print(
        f"Chambre 72 (luxueuse) - 2 nuits, saison haute : "
        f"{chambre_72.calculer_prix(2, 'haute')} €"
    )

    separateur("3. Réservation avec vérification de disponibilité")
    reservation_1 = hotel.reserver(client_1, chambre_70, nb_nuits=3, saison="haute")
    reservation_2 = hotel.reserver(client_2, chambre_71, nb_nuits=2, saison="basse")

    separateur("4. Génération de facture")
    print(reservation_1.generer_facture())
    print()
    print(reservation_2.generer_facture())

    separateur("5. Gestion d'erreur : tentative de double réservation")
    try:
        hotel.reserver(client_2, chambre_70, nb_nuits=1, saison="basse")
    except ChambreNonDisponibleException as e:
        print(f"Erreur capturée : {e}")

    separateur("6. Écriture des réservations dans reservations.csv")
    reservation_1.sauvegarder()
    reservation_2.sauvegarder()

    separateur("7. Lecture depuis reservations.csv")
    hotel.charger_reservations()

    separateur("8. État final de l'hôtel")
    print(hotel)
    print("Chambres disponibles :")
    for c in hotel.chambres_disponibles():
        print(f" - {c}")


if __name__ == "__main__":
    main()