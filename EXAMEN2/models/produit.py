class Produit:
    def __init__(self, reference, designation, prix_unitaire, stock=0,
                 id=None, date_creation=None):
        self.id = id
        self.reference = reference
        self.designation = designation
        self.prix_unitaire = prix_unitaire
        self.stock = stock
        self.date_creation = date_creation