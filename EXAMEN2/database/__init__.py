# init_db.py
import mysql.connector
from mysql.connector import Error


def initialiser_base_de_donnees():
    # 1. Connexion initiale sans spécifier de base de données pour pouvoir la créer
    config_initiale = {
        "host": "localhost",
        "user": "root",
        "password": "",  # Mettez votre mot de passe si nécessaire
        "port": 3306  # Modifiez par 3307 si XAMPP utilise le port 3307
    }

    nom_base_de_donnees = "gestion_commandes"

    try:
        conn = mysql.connector.connect(**config_initiale)
        cursor = conn.cursor()

        # Création de la base de données
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nom_base_de_donnees} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"  Base de données '{nom_base_de_donnees}' vérifiée/créée avec succès.")

        # Reconnexion directe sur la nouvelle base de données
        # cursor.execute(f"USE {nom_base_de_donnees};") # Pas nécessaire si on se reconnecte avec la BD

        # 2. Création des tables
        tables = {
            "fournisseur": """
                           CREATE TABLE IF NOT EXISTS fournisseur
                           (
                               id INT AUTO_INCREMENT PRIMARY KEY,
                               code VARCHAR(50) NOT NULL UNIQUE,
                               raison_sociale VARCHAR(150) NOT NULL,
                               email VARCHAR(100),
                               telephone VARCHAR(50),
                               adresse TEXT,
                               date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                           ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                           CREATE INDEX idx_fournisseur_code ON fournisseur(code);
                           """,
            "produit": """
                       CREATE TABLE IF NOT EXISTS produit
                       (
                           id INT AUTO_INCREMENT PRIMARY KEY,
                           reference VARCHAR(50) NOT NULL UNIQUE,
                           designation VARCHAR(150) NOT NULL,
                           prix_unitaire DECIMAL(10, 2) NOT NULL CHECK (prix_unitaire > 0),
                           stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
                           date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                       ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                       CREATE INDEX idx_produit_reference ON produit(reference);
                       CREATE INDEX idx_produit_stock ON produit(stock);
                       """,
            "commande": """
                        CREATE TABLE IF NOT EXISTS commande
                        (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            numero VARCHAR(50) NOT NULL UNIQUE,
                            date_commande DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            fournisseur_id INT NOT NULL,
                            montant_total DECIMAL
                            (10, 2) DEFAULT 0.00,
                            statut VARCHAR(50) DEFAULT 'EN_ATTENTE' CHECK (statut IN ('EN_ATTENTE', 'VALIDEE', 'LIVREE', 'ANNULEE')),
                            date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id) ON DELETE RESTRICT ON UPDATE CASCADE
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                        CREATE INDEX idx_commande_numero ON commande(numero);
                        CREATE INDEX idx_commande_fournisseur ON commande(fournisseur_id);
                        CREATE INDEX idx_commande_statut ON commande(statut);
                        CREATE INDEX idx_commande_date ON commande(date_commande);
                        """,
            "ligne_commande": """
                             CREATE TABLE IF NOT EXISTS ligne_commande (
                                 id INT AUTO_INCREMENT PRIMARY KEY,
                                 commande_id INT NOT NULL,
                                 produit_id INT NOT NULL,
                                 quantite INT NOT NULL CHECK (quantite > 0),
                                 prix_unitaire DECIMAL(10, 2) NOT NULL,
                                 date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                 FOREIGN KEY (commande_id) REFERENCES commande(id) ON DELETE CASCADE ON UPDATE CASCADE,
                                 FOREIGN KEY (produit_id) REFERENCES produit(id) ON DELETE RESTRICT ON UPDATE CASCADE
                             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                             CREATE INDEX idx_ligne_commande_commande ON ligne_commande(commande_id);
                             CREATE INDEX idx_ligne_commande_produit ON ligne_commande(produit_id);
                             """
        }

        for nom_table, requete in tables.items():
            # Exécuter la requête de création de table
            cursor.execute(requete)
            print(f" Table '{nom_table}' vérifiée/créée avec succès.")

        conn.commit()
        cursor.close()
        conn.close()
        print("\nInitialisation complète réussie ! Vous pouvez maintenant lancer main.py.")

    except Error as e:
        print(f"Erreur lors de l'initialisation : {e}")


if __name__ == "__main__":
    initialiser_base_de_donnees()