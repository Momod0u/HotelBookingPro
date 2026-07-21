
class Client:
   
    def __init__(self, id: int, nom: str, email: str):
        self.id = id
        self.nom = nom
        self.email = email

    def presentation(self) -> None:
        """Affiche les informations du client."""
        print(f"Client #{self.id} - {self.nom} ({self.email})")

    def __str__(self) -> str:
        return f"{self.nom} <{self.email}>"
