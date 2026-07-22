class Fournisseur:

    def __init__(self, code, raison_sociale, email=None, telephone=None,
                 adresse=None, id=None, date_creation=None):
        self.id = id
        self.code = code
        self.raison_sociale = raison_sociale
        self.email = email
        self.telephone = telephone
        self.adresse = adresse
        self.date_creation = date_creation