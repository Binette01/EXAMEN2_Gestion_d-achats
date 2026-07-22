from daos import FournisseurDAO, ProduitDAO, CommandeDAO
from models.fournisseur import Fournisseur
from models.produit import Produit
from models.commande import Commande


class Menu:

    def __init__(self):
        self.f_dao = FournisseurDAO()
        self.p_dao = ProduitDAO()
        self.c_dao = CommandeDAO()

    def menu_principal(self):
        while True:
            print("\n" + "=" * 40)
            print("     APPLICATION GESTION DES ACHATS     ")
            print("=" * 40)
            print("1. Gestion des Fournisseurs")
            print("2. Gestion des Produits")
            print("3. Gestion des Commandes")
            print("4. Rapports & Statistiques")
            print("5. Quitter")
            choix = input("Faites votre choix : ")

            if choix == "1":
                self.menu_fournisseurs()
            elif choix == "2":
                self.menu_produits()
            elif choix == "3":
                self.menu_commandes()
            elif choix == "4":
                self.menu_statistiques()
            elif choix == "5":
                print("Au revoir !")
                break

    def menu_fournisseurs(self):
        while True:
            print("\n--- REPERTOIRE FOURNISSEURS ---")
            print("1. Ajouter un fournisseur")
            print("2. Lister tous les fournisseurs")
            print("3. Rechercher un fournisseur")
            print("4. Modifier un fournisseur")
            print("5. Supprimer un fournisseur")
            print("6. Retour")
            c = input("Choix : ")

            if c == "1":
                f = Fournisseur(
                    code=input("Code (ex: F001) : "),
                    raison_sociale=input("Raison Sociale : "),
                    email=input("Email : "),
                    telephone=input("Téléphone : "),
                    adresse=input("Adresse : ")
                )
                if self.f_dao.ajouter_fournisseur(f):
                    print("Fournisseur enregistré avec succès !")
                else:
                    print("Échec de l'enregistrement.")

            elif c == "2":
                fournisseurs = self.f_dao.lister_fournisseur()
                if fournisseurs:
                    for x in fournisseurs:
                        print(f"ID: {x.id} | [{x.code}] {x.raison_sociale} | Tel: {x.telephone}")
                else:
                    print("Aucun fournisseur trouvé.")

            elif c == "3":
                mot = input("Entrez le code ou le nom complet à rechercher : ")
                fournisseurs = self.f_dao.rechercher_fournisseur(mot)
                if fournisseurs:
                    for x in fournisseurs:
                        print(f"ID: {x.id} | Code: {x.code} | Nom: {x.raison_sociale} | Email: {x.email}")
                else:
                    print("Aucun fournisseur ne correspond à cette recherche.")

            elif c == "4":
                id_m = input("ID du fournisseur à modifier : ")
                f_exist = self.f_dao.get_by_id(id_m)
                if f_exist:
                    f_exist.code = input(f"Code [{f_exist.code}] : ") or f_exist.code
                    f_exist.raison_sociale = input(f"Nom [{f_exist.raison_sociale}] : ") or f_exist.raison_sociale
                    f_exist.email = input(f"Email [{f_exist.email}] : ") or f_exist.email
                    f_exist.telephone = input(f"Tel [{f_exist.telephone}] : ") or f_exist.telephone
                    f_exist.adresse = input(f"Adresse [{f_exist.adresse}] : ") or f_exist.adresse
                    if self.f_dao.modifier_fournisseur(f_exist):
                        print("Données mises à jour !")
                    else:
                        print("Échec de la modification.")
                else:
                    print("Fournisseur introuvable.")

            elif c == "5":
                id_s = input("ID du fournisseur à supprimer : ")
                if self.f_dao.supprimer_fournisseur(id_s):
                    print("Fournisseur supprimé de la base.")
                else:
                    print("Suppression impossible (Fournisseur inexistant ou lié à une commande).")

            elif c == "6":
                break

    def menu_produits(self):
        while True:
            print("\n--- CATALOGUE PRODUITS ---")
            print("1. Ajouter un produit")
            print("2. Lister les produits")
            print("3. Rechercher un produit")
            print("4. Alerte réapprovisionnement")
            print("5. Modifier un produit")
            print("6. Supprimer un produit")
            print("7. Retour")
            c = input("Choix : ")

            if c == "1":
                try:
                    reference = input("Référence (ex: REF001) : ")
                    designation = input("Désignation : ")
                    prix_unitaire = float(input("Prix unitaire : "))
                    stock = int(input("Stock initial : "))
                    p = Produit(reference=reference, designation=designation, prix_unitaire=prix_unitaire, stock=stock)

                    if self.p_dao.ajouter_produit(p):
                        print("Produit ajouté au catalogue !")
                    else:
                        print("Échec de l'ajout.")
                except ValueError:
                    print("Erreur : Le prix et le stock doivent être des nombres valides.")


            elif c == "2":
                produits = self.p_dao.lister_produit()
                if produits:
                    for x in produits:
                        print(
                            f"ID: {x.id} | Ref: {x.reference} | {x.designation} | Prix: {x.prix_unitaire} FCFA | Stock: {x.stock}")
                else:
                    print("Aucun produit dans le catalogue.")

            elif c == "3":
                mot = input("Mot-clé (référence ou désignation) : ")
                produits = self.p_dao.rechercher_produit(mot)
                if produits:
                    for x in produits:
                        print(f"ID: {x.id} | [{x.reference}] {x.designation} - Stock: {x.stock}")
                else:
                    print("Aucun produit trouvé.")

            elif c == "4":
                try:
                    seuil = int(input("Définir le seuil critique d'alerte : "))
                    produits = self.p_dao.lister_alertes_stock(seuil)
                    if produits:
                        for x in produits:
                            print(f"STOCK CRITIQUE -> ID {x.id} : {x.designation} (Reste : {x.stock})")
                    else:
                        print("Aucun produit n'est sous le seuil d'alerte.")
                except ValueError:
                    print("Erreur : Le seuil doit être un nombre entier.")

            elif c == "5":
                id_p = input("ID du produit à modifier : ")
                p = self.p_dao.get_by_id(id_p)
                if p:
                    p.reference = input(f"Ref [{p.reference}] : ") or p.reference
                    p.designation = input(f"Désignation [{p.designation}] : ") or p.designation

                    # Gérer la mise à jour du prix avec conversion et validation
                    prix_str = input(f"Prix [{p.prix_unitaire}] : ")
                    if prix_str:
                        try:
                            p.prix_unitaire = float(prix_str)
                        except ValueError:
                            print("Prix invalide, la valeur n'a pas été modifiée.")

                    # Gérer la mise à jour du stock avec conversion et validation
                    stock_str = input(f"Stock [{p.stock}] : ")
                    if stock_str:
                        try:
                            p.stock = int(stock_str)
                        except ValueError:
                            print("Stock invalide, la valeur n'a pas été modifiée.")

                    if self.p_dao.modifier_produit(p):
                        print("Produit modifié avec succès !")
                    else:
                        print("Échec de la modification.")
                else:
                    print("Produit introuvable.")

            elif c == "6":
                id_s = input("ID du produit à supprimer : ")
                if self.p_dao.supprimer_produit(id_s):
                    print("Produit retiré du catalogue.")
                else:
                    print("Suppression impossible (lié à des commandes ou ID invalide).")

            elif c == "7":
                break

    def menu_commandes(self):
        while True:
            print("\n--- REGISTRE DES COMMANDES ---")
            print("1. Passer une commande")
            print("2. Lister les commandes")
            print("3. Voir le détail d'une commande")
            print("4. Changer le statut d'une commande")
            print("5. Annuler une commande")
            print("6. Supprimer une commande")
            print("7. Retour")
            c = input("Choix : ")

            if c == "1":
                try:
                    num = input("Numéro de commande unique : ")
                    f_id = input("ID du fournisseur : ")
                    # Vérification de l'existence du fournisseur avant de continuer
                    if not self.f_dao.get_by_id(f_id):
                        print("Fournisseur introuvable. Opération annulée.")
                        continue

                    panier = []
                    while True:
                        p_id = input("ID du produit à acheter (ou appuyez sur Entrée pour finir) : ")
                        if not p_id:
                            break
                        
                        produit = self.p_dao.get_by_id(p_id)
                        if not produit:
                            print("Produit introuvable. Veuillez réessayer.")
                            continue

                        qte = int(input(f"Quantité demandée (stock disponible: {produit.stock}): "))
                        panier.append({'produit_id': p_id, 'quantite': qte})

                    if panier:
                        cmd = Commande(num, f_id)
                        if self.c_dao.ajouter_commande(cmd, panier):
                            print("Commande enregistrée et stocks mis à jour !")
                        else:
                            print("Échec de la commande (Vérifiez les stocks ou les ID).")
                    else:
                        print("Panier vide. Commande annulée.")
                except ValueError:
                    print("Erreur : La quantité doit être un nombre entier.")

            elif c == "2":
                commandes = self.c_dao.lister_commande()
                if commandes:
                    for cmd in commandes:
                        print(
                            f"ID: {cmd[0]} | N°: {cmd[1]} | Fournisseur: {cmd[5]} |"
                            f" Total: {cmd[3]} FCFA | Statut: {cmd[4]}")
                else:
                    print("Aucune commande enregistrée.")

            elif c == "3":
                id_c = input("ID de la commande à consulter : ")
                lignes = self.c_dao.lister_lignes_commande(id_c)
                if lignes:
                    print(f"\n--- Détails de la Commande ID {id_c} ---")
                    for l in lignes:
                        print(f" -> Article : {l[5]} | Qté : {l[3]} | PU : {l[4]} FCFA")
                else:
                    print("Aucun détail trouvé pour cette commande.")

            elif c == "4":
                id_c = input("ID de la commande : ")
                statut = input("Nouveau statut (VALIDEE, LIVREE) : ")
                if self.c_dao.modifier_statut(id_c, statut):
                    print("Statut mis à jour !")
                else:
                    print("Modification impossible (Le statut ne peut pas reculer).")

            elif c == "5":
                id_c = input("ID de la commande à annuler : ")
                if self.c_dao.annuler_commande(id_c):
                    print("Commande annulée et stocks restitués !")
                else:
                    print("Échec de l'annulation.")

            elif c == "6":
                id_c = input("ID de la commande à détruire : ")
                if self.c_dao.supprimer_commande(id_c):
                    print("Commande définitivement purgée.")
                else:
                    print("Échec de la suppression.")

            elif c == "7":
                break

    def menu_statistiques(self):
        print("\n" + "=" * 15 + " TABLEAU DE BORD " + "=" * 15)
        print(f"Chiffre d'Affaires Cumulé (Validées/Livrées) : {self.c_dao.obtenir_ca_total()} FCFA")
        print(f"Valeur Financière Globale du Stock : {self.c_dao.obtenir_valeur_stock()} FCFA")
        print("\nLES 5 ARTICLES LES PLUS COMMANDES :")
        top_produits = self.c_dao.obtenir_top_produits()
        if top_produits:
            for idx, item in enumerate(top_produits, 1):
                # item[0] = designation, item[1] = total_quantite
                print(f" {idx}. {item[0]} (Quantité totale achetée : {item[1]})")
        else:
            print("Aucune donnée disponible pour le moment.")
        print("=" * 47)

        