# HotelBookingPro

Projet POO Avancé — Système Avancé de Réservation Hôtelière  
Enseignant : Ibrahima SY (GitHub : syibrahima31)

## Description

`HotelBookingPro` est une application en ligne de commande permettant de gérer un hôtel : chambres (standard / luxueuse), clients, réservations, calcul de prix selon la saison, génération de factures et persistance des réservations dans un fichier CSV.

## Architecture

| Fichier | Contenu |
|---|---|
| `exceptions.py` | `ChambreNonDisponibleException` |
| `chambre.py` | `Facturable` (interface), `Chambre` (ABC), `ServiceSpa`, `ChambreStandard`, `ChambreLuxueuse` |
| `client.py` | `Client` |
| `reservation.py` | `Reservation` (composition + `Facturable`) |
| `hotel.py` | `Hotel` (agrégation de `Chambre`, `Client`, `Reservation`) |
| `main.py` | Script principal de démonstration |
| `tests.py` | Tests unitaires (bonus) |

### Concepts POO illustrés

- **Abstraction** : `Chambre` est une classe abstraite (`ABC`) avec la méthode abstraite `calculer_prix()`.
- **Héritage multiple** : `ChambreLuxueuse` hérite à la fois de `Chambre` et de `ServiceSpa`.
- **Encapsulation** : attributs protégés (`_numero`, `_type`, `_prix_base`, `_est_disponible`) accessibles via des méthodes/propriétés.
- **Interface** : `Facturable` (classe abstraite pure) implémentée par `Reservation`.
- **Exceptions personnalisées** : `ChambreNonDisponibleException`.
- **Persistance fichier** : `Reservation.sauvegarder()` (écriture CSV) et `Hotel.charger_reservations()` (lecture CSV).