import mysql.connector
from database.config import DB_CONFIG


def insert_test_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        # Insertion Fournisseur
        cursor.execute(
            "INSERT IGNORE INTO fournisseur (id, code, raison_sociale, email, telephone, adresse)"
            " VALUES (1, 'F001', 'Sénégal Distrib Informatique', 'contact@senedistrib.sn', '338241515', 'Dakar, Colobane')")

        # Insertion Produits
        cursor.execute(
            "INSERT IGNORE INTO produit (id, reference, designation, prix_unitaire, stock) "
            "VALUES (1, 'REF001', 'Lenovo ThinkPad X1', 650000.00, 20)")
        cursor.execute(
            "INSERT IGNORE INTO produit (id, reference, designation, prix_unitaire, stock)"
            " VALUES (2, 'REF002', 'Switch Cisco 24 Ports', 180000.00, 8)")

        conn.commit()
        print("Données de test injectées de manière propre et cohérente.")
    except Exception as e:
        print(f"Erreur d'insertion : {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    insert_test_data()