from models.produit import Produit
from database.connexion import DatabaseConnection
from daos.base_dao import BaseDAO

class ProduitDAO(BaseDAO):

    def ajouter_produit(self, p: Produit) -> bool:
        """
        Ajoute un nouveau produit à la base de données.

        Args:
            p (Produit): L'objet Produit à ajouter.

        Returns:
            bool: True si l'ajout a réussi, False sinon.
        """
        try:
            with DatabaseConnection() as db:
                sql = """
                INSERT INTO produit(reference, designation, prix_unitaire, stock)
                VALUES (%s, %s, %s, %s)
                """
                params = (p.reference, p.designation, p.prix_unitaire, p.stock)
                db.execute(sql, params)
                db.commit()
                return True
        except Exception as e:
            print(f"Erreur lors de l'ajout du produit : {e}")
            return False

    def lister_produit(self):
        """
        Récupère la liste de tous les produits de la base de données.

        Returns:
            list[Produit]: Une liste d'objets Produit.
        """
        try:
            with DatabaseConnection() as db:
                sql = ("SELECT id, reference, designation, prix_unitaire, stock,"
                       " date_creation FROM produit")
                db.execute(sql)
                rows = db.fetchall()
                return [Produit(r[1], r[2], r[3], r[4], id=r[0], date_creation=r[5]) for r in rows]
        except Exception as e:
            print(f"Erreur lors de la liste des produits : {e}")
            return []

    def get_by_id(self, id_p):
        """
        Récupère un produit spécifique par son ID.

        Args:
            id_p (any): L'ID du produit à récupérer.

        Returns:
            Produit | None: L'objet Produit s'il est trouvé, sinon None.
        """
        try:
            with DatabaseConnection() as db:
                sql = ("SELECT id, reference, designation, prix_unitaire, stock,"
                       " date_creation FROM produit WHERE id = %s")
                db.execute(sql, (id_p,))
                row = db.fetchone()
                if row:
                    return Produit(row[1], row[2], row[3], row[4], id=row[0], date_creation=row[5])
                return None
        except Exception as e:
            print(f"Erreur lors de la récupération du produit par ID : {e}")
            return None

    def modifier_produit(self, p: Produit) -> bool:
        """
        Met à jour les informations d'un produit existant.

        Args:
            p (Produit): L'objet Produit avec les données mises à jour.

        Returns:
            bool: True si la modification a réussi, False sinon.
        """
        try:
            with DatabaseConnection() as db:
                sql = """
                UPDATE produit
                SET reference=%s, designation=%s, prix_unitaire=%s, stock=%s
                WHERE id = %s
                """
                params = (p.reference, p.designation, p.prix_unitaire, p.stock, p.id)
                db.execute(sql, params)
                db.commit()
                return True
        except Exception as e:
            print(f"Erreur lors de la modification du produit : {e}")
            return False

    def supprimer_produit(self, id_p: str) -> bool:
        """
        Supprime un produit par son ID.
        La suppression échouera si le produit est lié à des lignes de commande
        (contrainte de clé étrangère ON DELETE RESTRICT).

        Args:
            id_p (str): L'ID du produit à supprimer.

        Returns:
            bool: True si la suppression a réussi, False sinon.
        """
        try:
            with DatabaseConnection() as db:
                sql = "DELETE FROM produit WHERE id = %s"
                db.execute(sql, (id_p,))
                db.commit()
                return True
        except Exception as e:
            print(f"Erreur lors de la suppression du produit : {e}")
            print("Suppression impossible (le produit est peut-être lié à une commande).")
            return False

    def rechercher_produit(self, mot_cle: str) -> list[Produit]:
        try:
            with DatabaseConnection() as db:
                sql = ("SELECT id, reference, designation, prix_unitaire, stock, date_creation"
                       " FROM produit WHERE designation LIKE %s OR reference = %s")
                params = (f"%{mot_cle}%", mot_cle)
                db.execute(sql, params)
                rows = db.fetchall()
                return [Produit(r[1], r[2], r[3], r[4], id=r[0], date_creation=r[5]) for r in rows]
        except Exception as e:
            print(f"Erreur lors de la recherche de produit : {e}")
            return []

    def lister_alertes_stock(self, seuil: int) -> list[Produit]:
        try:
            with DatabaseConnection() as db:
                sql = ("SELECT id, reference, designation, prix_unitaire, stock, "
                       "date_creation FROM produit WHERE stock < %s")
                db.execute(sql, (seuil,))
                rows = db.fetchall()
                return [Produit(r[1], r[2], r[3], r[4], id=r[0], date_creation=r[5]) for r in rows]
        except Exception as e:
            print(f"Erreur lors de la liste des alertes stock : {e}")
            return []

    def get_all(self):
        return self.lister_produit()

    def delete_by_id(self, id_p):
        return self.supprimer_produit(id_p)