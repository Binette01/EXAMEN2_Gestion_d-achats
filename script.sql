-- 1. Création de la base de données (si elle n'existe pas déjà)
CREATE DATABASE IF NOT EXISTS gestion_commandes_db;

-- 2. Sélection de la base de données
USE gestion_commandes_db;

-- 3. Création de la table 'fournisseur'
CREATE TABLE IF NOT EXISTS fournisseur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    raison_sociale VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telephone VARCHAR(20),
    adresse TEXT,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. Création de la table 'produit'
CREATE TABLE IF NOT EXISTS produit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reference VARCHAR(50) NOT NULL UNIQUE,
    designation VARCHAR(150) NOT NULL,
    prix_unitaire DECIMAL(10, 2) NOT NULL CHECK (prix_unitaire > 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. Création de la table 'commande'
CREATE TABLE IF NOT EXISTS commande (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(50) NOT NULL UNIQUE,
    date_commande DATETIME DEFAULT CURRENT_TIMESTAMP,
    fournisseur_id INT NOT NULL,
    montant_total DECIMAL(10, 2) DEFAULT 0.00,
    statut VARCHAR(50) NOT NULL DEFAULT 'EN_ATTENTE',
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id)
    -- On empêche la suppression d'un fournisseur s'il a des commandes
);

-- 6. Création de la table 'ligne_commande' (Détails du panier)
CREATE TABLE IF NOT EXISTS ligne_commande (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commande_id INT NOT NULL,
    produit_id INT NOT NULL,
    quantite INT NOT NULL CHECK (quantite > 0),
    prix_unitaire DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (commande_id) REFERENCES commande(id) ON DELETE CASCADE,
    FOREIGN KEY (produit_id) REFERENCES produit(id)
    -- ON DELETE CASCADE permet de supprimer les lignes si on supprime la commande
);
