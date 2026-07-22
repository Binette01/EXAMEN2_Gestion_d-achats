from models.commande import Commande
from database.connexion import DatabaseConnection
from daos.base_dao import BaseDAO


class CommandeDAO(BaseDAO):

    def ajouter_commande(self, cmd, lignes_panier):
        """
        Enregistre une nouvelle commande et ses lignes de détail dans la base de données.
        Cette opération est transactionnelle : si une étape échoue, tout est annulé (rollback).
        Elle décrémente également le stock des produits commandés.

        Args:
            cmd (Commande): L'objet Commande à créer (sans l'ID, le montant et le statut).
            lignes_panier (list): Une liste de dictionnaires, chacun représentant un produit
                                  et sa quantité. Ex: [{'produit_id': 1, 'quantite': 3}]

        Returns:
            bool: True si la commande a été ajoutée avec succès, False sinon.
        """
        try:
            with DatabaseConnection() as db:
                sql_cmd = ("INSERT INTO commande(numero, fournisseur_id, montant_total, statut)"
                           " VALUES (%s, %s, 0, 'EN_ATTENTE')")
                db.execute(sql_cmd, (cmd.numero, cmd.fournisseur_id))
                # Récupération de l'ID auto-généré pour la nouvelle commande (spécifique à MySQL)
                sql_id = "SELECT LAST_INSERT_ID()"
                db.execute(sql_id)
                res_id = db.fetchone()
                id_cmd_genere = res_id[0]

                montant_global = 0.0

                # Parcours du panier d'achat
                for item in lignes_panier:
                    sql_p = "SELECT prix_unitaire, stock FROM produit WHERE id = %s FOR UPDATE" # Verrouillage pour la transaction
                    db.execute(sql_p, (item['produit_id'],))
                    prod = db.fetchone()

                    # Vérification de la disponibilité du stock
                    if not prod or prod[1] < item['quantite']:
                        raise Exception(f"Stock insuffisant pour l'ID produit {item['produit_id']}")

                    sous_total = float(prod[0]) * int(item['quantite'])
                    montant_global += sous_total

                    # Enregistrement dans la table d'association ligne_commande
                    sql_l = ("INSERT INTO ligne_commande(commande_id, produit_id, quantite,"
                             " prix_unitaire) VALUES (%s, %s, %s, %s)")
                    db.execute(sql_l, (id_cmd_genere, item['produit_id'],
                                       item['quantite'], prod[0]))

                    # Déduction immédiate du stock disponible
                    sql_stock = "UPDATE produit SET stock = stock - %s WHERE id = %s"
                    db.execute(sql_stock, (item['quantite'], item['produit_id']))

                # Mise à jour finale du montant total calculé globalement
                sql_update = "UPDATE commande SET montant_total = %s WHERE id = %s"
                db.execute(sql_update, (montant_global, id_cmd_genere))

                db.commit() # Valide l'ensemble de la transaction
            return True
        except Exception as e:
            # Le __exit__ du contexte va automatiquement faire un rollback et fermer la connexion
            print(f"\nErreur de transaction lors de l'ajout de la commande : {e}")
            return False

    def lister_commande(self):
        """
        Récupère la liste de toutes les commandes avec le nom du fournisseur.

        Returns:
            list[tuple]: Une liste de tuples contenant les informations des commandes.
                         Retourne une liste vide en cas d'erreur.
        """
        try:
            with DatabaseConnection() as db:
                sql = ("SELECT c.id, c.numero, c.fournisseur_id, c.montant_total, c.statut, "
                       "f.raison_sociale FROM commande c JOIN fournisseur f ON c.fournisseur_id = f.id")
                db.execute(sql)
                return db.fetchall()
        except Exception as e:
            print(f"Erreur lors de la liste des commandes : {e}")
            return []

    def get_by_id(self, id_c):
        """
        Récupère une commande spécifique par son ID.

        Args:
            id_c (any): L'ID de la commande à récupérer.

        Returns:
            Commande | None: L'objet Commande s'il est trouvé, sinon None.
        """
        try:
            with DatabaseConnection() as db:
                sql = ("SELECT id, numero, fournisseur_id, montant_total, statut,"
                       " date_commande, date_creation FROM commande WHERE id = %s")
                db.execute(sql, (id_c,))
                l = db.fetchone()
                if l:
                    return Commande(l[1], l[2], l[3], l[4], l[0], l[5], l[6])
                return None
        except Exception as e:
            print(f"Erreur lors de la récupération de la commande par ID : {e}")
            return None

    def lister_lignes_commande(self, id_c):
        """
        Récupère toutes les lignes de détail pour une commande donnée.

        Args:
            id_c (any): L'ID de la commande.

        Returns:
            list[tuple]: Une liste de tuples contenant les détails de chaque ligne de commande.
        """
        try:
            with DatabaseConnection() as db:
                sql = ("SELECT lc.id, lc.commande_id, lc.produit_id, lc.quantite, lc.prix_unitaire,"
                       " p.designation FROM ligne_commande lc JOIN produit p ON lc.produit_id = p.id WHERE lc.commande_id = %s")
                db.execute(sql, (id_c,))
                return db.fetchall()
        except Exception as e:
            print(f"Erreur lors de la récupération des lignes de commande : {e}")
            return []

    def modifier_statut(self, id_c, nouveau_statut):
        """
        Modifie le statut d'une commande.
        Applique une logique pour empêcher de "revenir en arrière" dans le statut
        (ex: de 'LIVREE' à 'VALIDEE').

        Args:
            id_c (any): L'ID de la commande à modifier.
            nouveau_statut (str): Le nouveau statut à appliquer ('VALIDEE', 'LIVREE', etc.).

        Returns:
            bool: True si la modification a réussi, False sinon.
        """
        try:
            with DatabaseConnection() as db:
                # Récupérer le statut actuel à l'intérieur de la transaction pour éviter les race conditions
                sql_get = "SELECT statut FROM commande WHERE id = %s"
                db.execute(sql_get, (id_c,))
                res = db.fetchone()
                if not res:
                    print("\nCommande introuvable.")
                    return False
                statut_actuel = res[0]

                # L'annulation doit passer par la méthode dédiée `annuler_commande` pour restituer le stock
                if nouveau_statut.upper() == 'ANNULEE':
                    print("\nOpération non permise. Utilisez l'option 'Annuler une commande'.")
                    return False

                # Contrainte de flux fonctionnel : on ne peut pas revenir à un statut précédent.
                poids = {"EN_ATTENTE": 1, "VALIDEE": 2, "LIVREE": 3}
                poids_nouveau = poids.get(nouveau_statut.upper())
                poids_actuel = poids.get(statut_actuel)
                if not poids_nouveau or (poids_actuel and poids_nouveau < poids_actuel):
                    print("\nErreur : Le statut d'une commande ne peut pas reculer ou est invalide !")
                    return False

                sql_update = "UPDATE commande SET statut = %s WHERE id = %s"
                db.execute(sql_update, (nouveau_statut.upper(), id_c))
                db.commit()
                return True
        except Exception as e:
            print(f"Erreur lors de la modification du statut : {e}")
            return False

    def annuler_commande(self, id_c):
        """
        Annule une commande.
        Cette opération est transactionnelle : elle restitue les stocks des produits
        et met le statut de la commande à 'ANNULEE'.

        Args:
            id_c (any): L'ID de la commande à annuler.

        Returns:
            bool: True si l'annulation a réussi, False sinon.
        """
        try:
            with DatabaseConnection() as db:
                # Vérifier le statut de la commande avant d'annuler
                sql_check = "SELECT statut FROM commande WHERE id = %s FOR UPDATE"
                db.execute(sql_check, (id_c,))
                res = db.fetchone()
                if not res:
                    print("Commande introuvable.")
                    return False
                if res[0] in ('ANNULEE', 'LIVREE'):
                    print(f"Impossible d'annuler une commande qui est déjà '{res[0]}'.")
                    return False

                # Récupérer les lignes de commande pour restituer le stock
                sql_lignes = "SELECT produit_id, quantite FROM ligne_commande WHERE commande_id = %s"
                db.execute(sql_lignes, (id_c,))
                lignes = db.fetchall()

                for produit_id, quantite in lignes:
                    sql_r = "UPDATE produit SET stock = stock + %s WHERE id = %s"
                    db.execute(sql_r, (quantite, produit_id))

                # Restitution du stock pour chaque article de la commande annulée
                sql_c = "UPDATE commande SET statut = 'ANNULEE' WHERE id = %s"
                db.execute(sql_c, (id_c,))
                db.commit()
                return True
        except Exception as e:
            print(f"Erreur lors de l'annulation de la commande : {e}")
            return False

    def supprimer_commande(self, id_c):
        """
        Supprime définitivement une commande et ses lignes de détail de la base de données.
        C'est une suppression physique (hard delete).

        Args:
            id_c (any): L'ID de la commande à supprimer.

        Returns:
            bool: True si la suppression a réussi, False sinon.
        """
        try:
            with DatabaseConnection() as db:
                # La suppression des lignes de commande est gérée par `ON DELETE CASCADE`
                # dans la définition de la table, il suffit donc de supprimer la commande.
                sql = "DELETE FROM commande WHERE id = %s"
                if db.execute(sql, (id_c,)):
                    db.commit()
                    return True
                return False # L'ID n'existait pas, aucune ligne supprimée.
        except Exception as e:
            print(f"Erreur lors de la suppression de la commande : {e}")
            return False

    def obtenir_valeur_stock(self):
        """
        Calcule la valeur financière totale du stock de tous les produits.

        Returns:
            float: La valeur totale du stock.
        """
        try:
            with DatabaseConnection() as db:
                sql = "SELECT SUM(prix_unitaire * stock) FROM produit"
                db.execute(sql)
                res = db.fetchone()
                return float(res[0]) if res and res[0] else 0.0
        except Exception as e:
            print(f"Erreur lors du calcul de la valeur du stock : {e}")
            return 0.0

    def obtenir_ca_total(self):
        """
        Calcule le chiffre d'affaires total en additionnant le montant
        de toutes les commandes 'VALIDEE' ou 'LIVREE'.

        Returns:
            float: Le chiffre d'affaires total.
        """
        try:
            with DatabaseConnection() as db:
                sql = ("SELECT SUM(montant_total) FROM commande WHERE statut = 'VALIDEE'"
                       " OR statut = 'LIVREE'")
                db.execute(sql)
                res = db.fetchone()
                return float(res[0]) if res and res[0] else 0.0
        except Exception as e:
            print(f"Erreur lors du calcul du chiffre d'affaires : {e}")
            return 0.0

    def obtenir_top_produits(self):
        """
        Récupère les 5 produits les plus commandés en termes de quantité totale.

        Returns:
            list[tuple]: Une liste de tuples (designation, total_vendu).
        """
        try:
            with DatabaseConnection() as db:
                sql = """
                SELECT p.designation, SUM(lc.quantite) as total_vendu 
                FROM ligne_commande lc 
                JOIN produit p ON lc.produit_id = p.id 
                GROUP BY p.id, p.designation 
                ORDER BY total_vendu DESC LIMIT 5
                """
                db.execute(sql)
                return db.fetchall()
        except Exception as e:
            print(f"Erreur lors de la récupération du top produits : {e}")
            return []

    def get_all(self):
        """Alias pour lister_commande, pour compatibilité avec BaseDAO."""
        return self.lister_commande()

    def delete_by_id(self, id_c):
        """Implémentation obligatoire requise par BaseDAO."""
        return self.supprimer_commande(id_c)