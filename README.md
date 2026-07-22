# 📦 Système de Gestion des Commandes Fournisseurs

## 📝 Présentation du Projet
Ce projet a été réalisé dans le cadre du module de **Programmation Orientée Objet (POO) et Bases de Données** en **Licence 2 Informatique de Gestion (IAGE)**.

L'objectif est de développer une application console (CLI) en Python permettant à une entreprise sénégalaise de distribution de matériel informatique d'informatiser la gestion de ses achats auprès de ses fournisseurs. L'application remplace un suivi manuel sur papier afin de réduire les erreurs, optimiser la gestion des stocks et offrir une meilleure visibilité sur les flux d'approvisionnement.

---

## 🛠️ Architecture Technique & Design Patterns
L'application respecte une séparation stricte des responsabilités (architecture en couches) et s'appuie sur plusieurs concepts avancés de la POO :

* **Pattern Singleton :** Implémenté dans la classe de connexion pour garantir qu'une seule et unique instance de connexion à la base de données MySQL reste active à travers toute l'application.
* **Pattern DAO (Data Access Object) :** Utilisation d'une classe abstraite `BaseDAO` pour centraliser les opérations CRUD génériques. Les interactions SQL sont totalement isolées de la logique métier et de l'interface utilisateur.
* **Sécurité & Robustesse :** Utilisation exclusive de **requêtes SQL paramétrées** pour faire barrière aux injections SQL, et encapsulation des zones sensibles dans des blocs `try/except`.
* **Encapsulation :** Toutes les entités métiers possèdent des attributs privés accessibles uniquement via des propriétés (`@property` Getters/Setters).

---

## 📁 Structure du Projet
Le projet est découpé en packages Python distincts pour assurer une excellente maintenabilité :

```text
📂 gestion_commandes_fournisseurs/
│
├── 📂 database/
│   ├── __init__.py
│   ├── config.py          # Configuration des accès MySQL (Hôte, port, user, base)
│   └── connexion.py       # Singleton de connexion à la base de données
│
├── 📂 models/
│   ├── __init__.py
│   ├── fournisseur.py     # Modèle de l'entité Fournisseur
│   ├── produit.py         # Modèle de l'entité Produit
│   └── commande.py        # Modèle de l'entité Commande
│
├── 📂 daos/
│   ├── __init__.py
│   ├── base_dao.py        # Classe abstraite contenant le contrat CRUD
│   ├── fournisseur_dao.py # Gestion des requêtes SQL pour les fournisseurs
│   ├── produit_dao.py     # Gestion des requêtes SQL pour les produits
│   └── commande_dao.py    # Gestion des transactions et stocks des commandes
│
├── .gitignore             # Fichiers à exclure du versionnage Git
├── README.md              # Documentation du projet
└── main.py                # Point d'entrée de l'application (Menu interactif)