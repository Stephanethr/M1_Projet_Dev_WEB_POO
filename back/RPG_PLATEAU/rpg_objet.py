from enum import Enum

class Raretes(Enum):
    # Races humaines
    COMMUN = "Commun"
    RARE = "Rare"
    LEGENDAIRE = "Légendaire"

class Objet:
    def __init__(self, nom, type_objet, rarete, effet):
        """
        Représente un objet équipé par un Avatar.
        - nom : Nom de l'objet.
        - type_objet : Type d'objet (e.g., "Armure", "Arme").
        - rareté : Représente la puissance de l'objet avec un type énuméré
        - effet : Dictionnaire contenant les bonus permanents. Exemple: {"force": 5, "endurance": 3}.
        """
        self.nom = nom
        self.type_objet = type_objet
        self.rarete = rarete
        self.effet = effet

    def obtenir_rarete(self) -> Raretes:
        return self.rarete

    def __str__(self):
        return f"{self.nom} ({self.type_objet}) - Effet: {self.effet}"


class Equipement(Objet):
    def __init__(self, nom, type_objet, rarete, effet, equipe=False):
        """
        Représente un équipement qui peut être équipé/déséquipé par un Avatar.
        Hérite de la classe Objet.
        L'effet ne s'applique que lorsque l'équipement est équipé.
        """
        super().__init__(nom, type_objet, rarete, effet)
        self.equipe = equipe
    
    def est_equipe(self):
        """Retourne True si l'équipement est équipé"""
        return self.equipe
    
    def __str__(self):
        status = "équipé" if self.equipe else "non équipé"
        return f"{super().__str__()} - Status: {status}"


class Consommable(Objet):
    def __init__(self, nom, type_objet, rarete, effet, quantite=1):
        """
        Représente un objet consommable avec une quantité limitée.
        Hérite de la classe Objet.
        - quantite : Nombre d'utilisations disponibles.
        """
        super().__init__(nom, type_objet, rarete, effet)
        self.quantite = quantite
    
    def ajouter(self, nombre=1):
        """Ajoute des unités au consommable"""
        self.quantite += nombre
        return f"{nombre} {self.nom}(s) ont été ajoutés."
    
    def get_quantite(self):
        """Retourne la quantité restante"""
        return self.quantite
    
    def __str__(self):
        return f"{super().__str__()} - Quantité restante: {self.quantite}"