class Commande:
    def __init__(self, numero, fournisseur_id, montant_total=0.0,
                 statut='EN_ATTENTE', id=None, date_commande=None, date_creation=None):
        self.id = id
        self.numero = numero
        self.fournisseur_id = fournisseur_id
        self.montant_total = montant_total
        self.statut = statut
        self.date_commande = date_commande
        self.date_creation = date_creation