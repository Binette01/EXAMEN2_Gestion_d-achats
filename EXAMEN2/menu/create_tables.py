from database.config import TYPE_BD
from database.connexion import DatabaseConnection


def create_tables():
    """Création des tables fournisseur, produit, commande, ligne_commande"""

    db = DatabaseConnection()

    if not db.connect():
        print("Connexion échouée")
        return False

    try:
        # ===================== TABLE FOURNISSEUR =====================
        sql_fournisseur = """
        CREATE TABLE IF NOT EXISTS fournisseur (
            id SERIAL PRIMARY KEY,
            code VARCHAR(50) UNIQUE NOT NULL,
            raison_sociale VARCHAR(150) NOT NULL,
            email VARCHAR(150),
            telephone VARCHAR(30),
            adresse TEXT,
            date_creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """ if TYPE_BD == "postgres" else """
        CREATE TABLE IF NOT EXISTS fournisseur (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(50) UNIQUE NOT NULL,
            raison_sociale VARCHAR(150) NOT NULL,
            email VARCHAR(100),
            telephone VARCHAR(50),
            adresse TEXT,
            date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        CREATE INDEX idx_fournisseur_code ON fournisseur(code);
        """

        # ===================== TABLE PRODUIT =====================
        sql_produit = """
        CREATE TABLE IF NOT EXISTS produit (
            id SERIAL PRIMARY KEY,
            reference VARCHAR(50) UNIQUE NOT NULL,
            designation VARCHAR(150) NOT NULL,
            prix_unitaire DECIMAL(10,2) NOT NULL CHECK (prix_unitaire > 0),
            stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
            date_creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """ if TYPE_BD == "postgres" else """
        CREATE TABLE IF NOT EXISTS produit (
            id INT AUTO_INCREMENT PRIMARY KEY,
            reference VARCHAR(50) UNIQUE NOT NULL,
            designation VARCHAR(150) NOT NULL,
            prix_unitaire DECIMAL(10, 2) NOT NULL CHECK (prix_unitaire > 0),
            stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
            date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        CREATE INDEX idx_produit_reference ON produit(reference);
        -- Le script fourni n'inclut pas idx_produit_stock ici, mais il est dans __init__.py
        -- CREATE INDEX idx_produit_stock ON produit(stock);
        """

        # ===================== TABLE COMMANDE =====================
        sql_commande = """
        CREATE TABLE IF NOT EXISTS commande (
            id SERIAL PRIMARY KEY,
            numero VARCHAR(50) UNIQUE NOT NULL,
            fournisseur_id INTEGER REFERENCES fournisseur(id) ON DELETE RESTRICT,
            montant_total DECIMAL(10,2) DEFAULT 0.00,
            statut VARCHAR(50) DEFAULT 'EN_ATTENTE' CHECK (statut IN ('EN_ATTENTE', 'VALIDEE', 'LIVREE', 'ANNULEE')),
            date_commande TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            date_creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """ if TYPE_BD == "postgres" else """
        CREATE TABLE IF NOT EXISTS commande (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero VARCHAR(50) UNIQUE NOT NULL,
            date_commande DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            fournisseur_id INT NOT NULL,
            montant_total DECIMAL(10, 2) DEFAULT 0.00,
            statut VARCHAR(50) DEFAULT 'EN_ATTENTE' CHECK (statut IN ('EN_ATTENTE', 'VALIDEE', 'LIVREE', 'ANNULEE')),
            date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id) ON DELETE RESTRICT ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        CREATE INDEX idx_commande_numero ON commande(numero);
        CREATE INDEX idx_commande_fournisseur ON commande(fournisseur_id);
        CREATE INDEX idx_commande_statut ON commande(statut);
        -- Le script fourni n'inclut pas idx_commande_date ici, mais il est dans __init__.py
        -- CREATE INDEX idx_commande_date ON commande(date_commande);
        """

        # ===================== TABLE LIGNE COMMANDE =====================
        sql_ligne_commande = """
        CREATE TABLE IF NOT EXISTS ligne_commande (
            id SERIAL PRIMARY KEY,
            commande_id INTEGER REFERENCES commande(id) ON DELETE CASCADE,
            produit_id INTEGER NOT NULL REFERENCES produit(id) ON DELETE RESTRICT,
            quantite INTEGER NOT NULL CHECK (quantite > 0),
            prix_unitaire DECIMAL(10,2) NOT NULL,
            date_creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """ if TYPE_BD == "postgres" else """
        CREATE TABLE IF NOT EXISTS ligne_commande (
            id INT AUTO_INCREMENT PRIMARY KEY,
            commande_id INT NOT NULL,
            produit_id INT NOT NULL,
            quantite INT NOT NULL CHECK (quantite > 0),
            prix_unitaire DECIMAL(10, 2) NOT NULL,
            date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (commande_id) REFERENCES commande(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (produit_id) REFERENCES produit(id) ON DELETE RESTRICT ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        CREATE INDEX idx_ligne_commande_commande ON ligne_commande(commande_id);
        CREATE INDEX idx_ligne_commande_produit ON ligne_commande(produit_id);
        """

        # ===================== EXECUTION =====================
        tables = [
            ("fournisseur", sql_fournisseur),
            ("produit", sql_produit),
            ("commande", sql_commande),
            ("ligne_commande", sql_ligne_commande)
        ]

        for name, sql in tables:
            print(f"→ Création table {name} ...")

            if not db.execute(sql):
                raise Exception(f"Erreur création table {name}")

        db.commit()
        print("\nToutes les tables ont été créées avec succès !")
        return True

    except Exception as e:
        print(f"Erreur globale : {e}")
        db.rollback()
        return False

    finally:
        db.disconnect()


if __name__ == "__main__":
    create_tables()