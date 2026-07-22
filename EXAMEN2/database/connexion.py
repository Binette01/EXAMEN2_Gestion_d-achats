import mysql.connector
from database.config import DB_CONFIG

class DatabaseConnection:
    """
    Gestionnaire de contexte pour les connexions à la base de données MySQL.
    Assure que la connexion est correctement ouverte et fermée,
    et gère les transactions (rollback en cas d'erreur).
    """
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Ouvre la connexion et le curseur en entrant dans le bloc 'with'."""
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            return self  # Retourne l'objet lui-même pour être utilisé après 'as'
        except mysql.connector.Error as err:
            print(f"Erreur de connexion à la base de données : {err}")
            # On propage l'erreur pour que le bloc 'with' ne s'exécute pas
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ferme la connexion en sortant du bloc 'with'.
        Effectue un rollback si une exception a été levée dans le bloc.
        """
        if exc_type:
            # Une exception a eu lieu, on annule la transaction
            print(f"Une erreur est survenue, rollback de la transaction : {exc_val}")
            if self.conn:
                self.conn.rollback()
        else:
            # Pas d'exception, on peut supposer que le commit a été fait manuellement si nécessaire
            pass
        
        # Fermeture du curseur et de la connexion dans tous les cas
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Ne pas supprimer l'exception, la laisser se propager si elle existe
        return False

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.rowcount > 0

    def fetchall(self): return self.cursor.fetchall()
    def fetchone(self): return self.cursor.fetchone()
    def commit(self): self.conn.commit()
    def rollback(self): self.conn.rollback()