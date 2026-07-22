from daos.base_dao import BaseDAO
from database.connexion import DatabaseConnection
from models.fournisseur import Fournisseur


class FournisseurDAO(BaseDAO):
    """DAO pour la table 'fournisseur' (MySQL)."""

    def ajouter_fournisseur(self, f: Fournisseur) -> bool:
        """
        Ajoute un nouveau fournisseur à la base de données.

        Args:
            f (Fournisseur): L'objet Fournisseur à ajouter.

        Returns:
            bool: True si l'ajout a réussi, False sinon.
        """
        try:
            with DatabaseConnection() as db:
                sql = """
                INSERT INTO fournisseur(code, raison_sociale, email, telephone, adresse)
                VALUES (%s, %s, %s, %s, %s)
                """
                params = (f.code, f.raison_sociale, f.email, f.telephone, f.adresse)
                db.execute(sql, params)
                db.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout du fournisseur : {e}")
            return False

    def lister_fournisseur(self):
        """
        Récupère la liste de tous les fournisseurs de la base de données.

        Returns:
            list[Fournisseur]: Une liste d'objets Fournisseur.
                               Retourne une liste vide en cas d'erreur.
        """
        try:
            with DatabaseConnection() as db:
                sql = "SELECT id, code, raison_sociale, email, telephone, adresse FROM fournisseur"
                db.execute(sql)
                rows = db.fetchall()
                fournisseurs = []
                for r in rows:
                    fournisseurs.append(Fournisseur(code=r[1], raison_sociale=r[2], email=r[3], telephone=r[4], adresse=r[5], id=r[0]))
                return fournisseurs
        except Exception as e:
            print(f"Erreur lors de la liste des fournisseurs : {e}")
            return []

    def rechercher_fournisseur(self, mot_cle: str):
        """
        Recherche des fournisseurs par code ou par raison sociale.

        Args:
            mot_cle (str): Le code exact ou une partie de la raison sociale à rechercher.

        Returns:
            list[Fournisseur]: Une liste de fournisseurs correspondant aux critères.
        """
        try:
            with DatabaseConnection() as db:
                sql = ("SELECT id, code, raison_sociale, email, telephone, adresse "
                       "FROM fournisseur WHERE raison_sociale LIKE %s OR code = %s")
                db.execute(sql, (f"%{mot_cle}%", mot_cle))
                rows = db.fetchall()
                fournisseurs = []
                for r in rows:
                    fournisseurs.append(Fournisseur(code=r[1], raison_sociale=r[2], email=r[3], telephone=r[4], adresse=r[5], id=r[0]))
                return fournisseurs
        except Exception as e:
            print(f"Erreur lors de la recherche de fournisseur : {e}")
            return []

    def modifier_fournisseur(self, f: Fournisseur) -> bool:
        """
        Met à jour les informations d'un fournisseur existant.

        Args:
            f (Fournisseur): L'objet Fournisseur avec les données mises à jour.
                             L'ID du fournisseur doit être valide.
        Returns:
            bool: True si la modification a réussi, False sinon.
        """
        try:
            with DatabaseConnection() as db:
                sql = """
                UPDATE fournisseur
                SET code=%s, raison_sociale=%s, email=%s, telephone=%s, adresse=%s
                WHERE id=%s
                """
                params = (f.code, f.raison_sociale, f.email, f.telephone, f.adresse, f.id)
                db.execute(sql, params)
                db.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la modification du fournisseur : {e}")
            return False

    def supprimer_fournisseur(self, id_f: str) -> bool:
        """
        Supprime un fournisseur de la base de données par son ID.
        La suppression échouera si le fournisseur est lié à des commandes
        existantes (contrainte de clé étrangère ON DELETE RESTRICT).

        Args:
            id_f (str): L'ID du fournisseur à supprimer.

        Returns:
            bool: True si la suppression a réussi, False sinon.
        """
        try:
            with DatabaseConnection() as db:
                # Si le fournisseur est lié à une commande, MySQL refusera (ON DELETE RESTRICT)
                # et lèvera une exception, qui sera interceptée.
                sql = "DELETE FROM fournisseur WHERE id = %s"
                db.execute(sql, (id_f,))
                db.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression du fournisseur : {e}")
            return False

    # Compat BaseDAO / API menu
    def get_all(self):
        """Alias pour lister_fournisseur, pour compatibilité avec BaseDAO."""
        return self.lister_fournisseur()

    def get_by_id(self, id_entite):
        """
        Récupère un fournisseur spécifique par son ID.

        Args:
            id_entite (any): L'ID du fournisseur à récupérer.

        Returns:
            Fournisseur | None: L'objet Fournisseur s'il est trouvé, sinon None.
        """
        try:
            with DatabaseConnection() as db:
                sql = "SELECT id, code, raison_sociale, email, telephone, adresse FROM fournisseur WHERE id = %s"
                db.execute(sql, (id_entite,))
                row = db.fetchone()
                if not row:
                    return None
                return Fournisseur(code=row[1], raison_sociale=row[2], email=row[3], telephone=row[4], adresse=row[5], id=row[0])
        except Exception as e:
            print(f"Erreur lors de la récupération du fournisseur par ID : {e}")
            return None

    def delete_by_id(self, id_entite):
        """Alias pour supprimer_fournisseur, pour compatibilité avec BaseDAO."""
        return self.supprimer_fournisseur(id_entite)
